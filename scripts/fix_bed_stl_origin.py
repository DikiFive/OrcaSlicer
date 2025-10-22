#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recenter a bed STL so that its XY center is at (0,0) for OrcaSlicer.
Also supports explicit translation/rotation if needed.

Usage examples:
  - Center by bed size (width, depth):
      python scripts/fix_bed_stl_origin.py --input resources/profiles/LONGER/longer_lk10_buildplate_model.stl \
          --center 225 225 --inplace

  - Explicit translate (dx, dy, dz):
      python scripts/fix_bed_stl_origin.py --input ... --translate 10 -5 0 --output out.stl

Notes:
  - Handles binary STL reliably. If ASCII STL is detected, it will attempt a simple parse/replace for 'vertex' lines.
  - Rotation is optional (degrees around Z axis), applied before translation.
"""
import argparse
import math
import os
import struct
import sys


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True, help='Path to STL file')
    p.add_argument('--output', help='Output STL path; if omitted with --inplace, input will be overwritten')
    p.add_argument('--inplace', action='store_true', help='Overwrite input file')
    p.add_argument('--center', nargs=2, type=float, metavar=('WIDTH','DEPTH'), help='Center model by subtracting (W/2, D/2) from (X,Y)')
    p.add_argument('--align', choices=['lowerleft','bottomcenter','backcenter'], help='Auto-align using model bounding box: lowerleft moves (minX,minY)->(0,0); bottomcenter moves minY->0 and centerX->WIDTH/2; backcenter moves maxY->DEPTH and centerX->WIDTH/2 (bottom/back modes require --center WIDTH DEPTH)')
    p.add_argument('--translate', nargs=3, type=float, metavar=('DX','DY','DZ'), help='Translate by (dx,dy,dz) after centering/rotation')
    p.add_argument('--rotate_z', type=float, default=0.0, help='Rotate around Z axis in degrees (applied before translation)')
    return p.parse_args()


def is_binary_stl(data: bytes) -> bool:
    if len(data) < 84:
        return False
    tri_count = struct.unpack('<I', data[80:84])[0]
    expected = 84 + 50 * tri_count
    return expected == len(data)


def apply_transform_to_triangle(record: bytearray, cos_z: float, sin_z: float, tx: float, ty: float, tz: float):
    # record layout: normal(12 bytes) + 3 vertices (36 bytes) + attr(2 bytes)
    # We only transform vertices
    # v offset start after normal: 12 bytes
    off = 12
    for _ in range(3):
        x, y, z = struct.unpack('<fff', record[off:off+12])
        # rotate around Z
        xr = x * cos_z - y * sin_z
        yr = x * sin_z + y * cos_z
        zr = z
        # translate
        x2 = xr + tx
        y2 = yr + ty
        z2 = zr + tz
        record[off:off+12] = struct.pack('<fff', x2, y2, z2)
        off += 12
    # normals left unchanged; attribute left unchanged


def compute_bbox_binary(data: bytes):
    tri_count = struct.unpack('<I', data[80:84])[0]
    base = 84
    minx = miny = minz = float('inf')
    maxx = maxy = maxz = float('-inf')
    for i in range(tri_count):
        rec_start = base + i * 50
        # skip normal (12 bytes)
        off = rec_start + 12
        for _ in range(3):
            x, y, z = struct.unpack('<fff', data[off:off+12])
            minx = min(minx, x); miny = min(miny, y); minz = min(minz, z)
            maxx = max(maxx, x); maxy = max(maxy, y); maxz = max(maxz, z)
            off += 12
    return (minx, miny, minz, maxx, maxy, maxz)


def process_binary(data: bytes, tx: float, ty: float, tz: float, rot_deg: float) -> bytes:
    out = bytearray(data)
    tri_count = struct.unpack('<I', data[80:84])[0]
    cos_z = math.cos(math.radians(rot_deg))
    sin_z = math.sin(math.radians(rot_deg))
    # iterate over triangles
    base = 84
    for i in range(tri_count):
        rec_start = base + i * 50
        rec = out[rec_start:rec_start+50]
        apply_transform_to_triangle(rec, cos_z, sin_z, tx, ty, tz)
        out[rec_start:rec_start+50] = rec
    return bytes(out)


def try_process_ascii(text: str, tx: float, ty: float, tz: float, rot_deg: float) -> str:
    # very simple parser for lines starting with 'vertex x y z'
    cos_z = math.cos(math.radians(rot_deg))
    sin_z = math.sin(math.radians(rot_deg))
    def trans_line(line: str) -> str:
        parts = line.strip().split()
        if len(parts) == 4 and parts[0] == 'vertex':
            try:
                x = float(parts[1]); y = float(parts[2]); z = float(parts[3])
            except ValueError:
                return line
            xr = x * cos_z - y * sin_z
            yr = x * sin_z + y * cos_z
            zr = z
            x2 = xr + tx; y2 = yr + ty; z2 = zr + tz
            return f"    vertex {x2:.6f} {y2:.6f} {z2:.6f}\n"
        return line
    return ''.join(trans_line(ln) for ln in text.splitlines(keepends=True))


def main():
    args = parse_args()
    if not os.path.exists(args.input):
        print(f"Input not found: {args.input}", file=sys.stderr)
        sys.exit(2)

    tx = ty = tz = 0.0
    want_w = want_d = None
    if args.center:
        want_w, want_d = args.center
        tx -= want_w / 2.0
        ty -= want_d / 2.0
    if args.translate:
        dx, dy, dz = args.translate
        tx += dx; ty += dy; tz += dz

    with open(args.input, 'rb') as f:
        data = f.read()

    if is_binary_stl(data):
        # pre-compute bbox for align modes
        if args.align:
            minx, miny, minz, maxx, maxy, maxz = compute_bbox_binary(data)
            print(f"Original bbox: min=({minx:.3f},{miny:.3f},{minz:.3f}) max=({maxx:.3f},{maxy:.3f},{maxz:.3f})")
            if args.align == 'lowerleft':
                tx += -minx; ty += -miny
            elif args.align == 'bottomcenter':
                if want_w is None:
                    print('bottomcenter requires --center WIDTH DEPTH to provide bed width', file=sys.stderr)
                    sys.exit(2)
                cx = (minx + maxx) / 2.0
                tx += (want_w / 2.0) - cx
                ty += -miny
            elif args.align == 'backcenter':
                if want_w is None or want_d is None:
                    print('backcenter requires --center WIDTH DEPTH to provide bed size', file=sys.stderr)
                    sys.exit(2)
                cx = (minx + maxx) / 2.0
                tx += (want_w / 2.0) - cx
                ty += want_d - maxy
        out_data = process_binary(data, tx, ty, tz, args.rotate_z)
        out_path = args.output or (args.input if args.inplace else None)
        if not out_path:
            print('--output is required if not using --inplace', file=sys.stderr)
            sys.exit(2)
        with open(out_path, 'wb') as f:
            f.write(out_data)
        print(f"Wrote binary STL: {out_path}")
    else:
        # try ASCII
        try:
            text = data.decode('utf-8', errors='strict')
        except UnicodeDecodeError:
            text = data.decode('latin-1', errors='ignore')
        # NOTE: ASCII mode does not adjust bbox for align; most bed models are binary.
        out_text = try_process_ascii(text, tx, ty, tz, args.rotate_z)
        out_path = args.output or (args.input if args.inplace else None)
        if not out_path:
            print('--output is required if not using --inplace', file=sys.stderr)
            sys.exit(2)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(out_text)
        print(f"Wrote ASCII STL: {out_path}")


if __name__ == '__main__':
    main()
