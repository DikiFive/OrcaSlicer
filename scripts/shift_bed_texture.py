#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shift a bed texture PNG by a given (dx, dy) in millimeters, generating a new PNG.
Assumes the texture maps exactly to the printable bed area of size (BED_W, BED_H) mm.

Examples:
  python scripts/shift_bed_texture.py \
    --input resources/profiles/LONGER/longer_lk10_buildplate_texture.png \
    --bed 225 225 --shift-mm 0 -2 \
    --output resources/profiles/LONGER/longer_lk10_buildplate_texture_shifted.png

Notes:
- Positive dy moves the artwork toward the FRONT (lower Y), negative dy moves toward the BACK (higher Y),
  matching printer bed coordinates (origin at front-left).
- The script wraps around transparent background; by default it expands canvas and fills with fully transparent pixels.
"""
import argparse
from PIL import Image

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True, help='Input PNG path')
    p.add_argument('--output', required=True, help='Output PNG path')
    p.add_argument('--bed', nargs=2, type=float, metavar=('BED_W','BED_H'), required=True, help='Bed size in mm (width, height)')
    p.add_argument('--shift-mm', nargs=2, type=float, metavar=('DX_MM','DY_MM'), default=(0.0, 0.0), help='Shift in mm: +X right, +Y front')
    p.add_argument('--wrap', action='store_true', help='Wrap pixels around instead of padding with transparency')
    return p.parse_args()


def shift_image(im: Image.Image, dx_px: int, dy_px: int, wrap: bool) -> Image.Image:
    w, h = im.size
    if wrap:
        # roll image content
        dx = dx_px % w
        dy = dy_px % h
        part1 = im.crop((0, 0, w - dx, h - dy))
        part2 = im.crop((w - dx, 0, w, h - dy))
        part3 = im.crop((0, h - dy, w - dx, h))
        part4 = im.crop((w - dx, h - dy, w, h))
        out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        out.paste(part4, (0, 0))
        out.paste(part3, (0, 0 + dy))
        out.paste(part2, (0 + dx, 0))
        out.paste(part1, (0 + dx, 0 + dy))
        return out
    else:
        out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        out.paste(im, (dx_px, dy_px))
        return out


def main():
    args = parse_args()
    im = Image.open(args.input).convert('RGBA')
    w, h = im.size
    bed_w, bed_h = args.bed
    px_per_mm_x = w / bed_w
    px_per_mm_y = h / bed_h
    dx_mm, dy_mm = args.shift_mm
    # +Y is front in Orca; in image coordinates +y is downwards, which matches moving toward front
    dx_px = int(round(dx_mm * px_per_mm_x))
    dy_px = int(round(dy_mm * px_per_mm_y))
    out = shift_image(im, dx_px, dy_px, args.wrap)
    out.save(args.output)
    print(f"Input: {w}x{h}px, bed: {bed_w}x{bed_h}mm, shift: {dx_mm},{dy_mm}mm -> {dx_px},{dy_px}px\nSaved: {args.output}")

if __name__ == '__main__':
    main()
