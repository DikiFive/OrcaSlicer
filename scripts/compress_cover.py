#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compress a cover image to a target size by:
- optional downscaling (longest side)
- PNG palette quantization with N colors

Goal: produce small PNGs (~20KB) while retaining legibility.

Example:
  python scripts/compress_cover.py \
    --input resources/profiles/LONGER/LONGER\ LK10_cover.png \
    --output resources/profiles/LONGER/LONGER\ LK10_cover.png \
    --max-side 600 --colors 48 --target-kb 25
"""
import argparse
import os
from PIL import Image


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--max-side', type=int, default=600, help='Max pixels for the longest side before saving (ignored when --square-size is used)')
    p.add_argument('--colors', type=int, default=48, help='Palette colors for PNG quantization (ignored when --no-quantize)')
    p.add_argument('--target-kb', type=int, default=25, help='Target maximum file size in KB')
    p.add_argument('--square-size', type=int, help='Force output to a square canvas of this size (px). Image is fit and centered on transparent background')
    p.add_argument('--min-side', type=int, default=256, help='Minimum side length (px) when iteratively downscaling to meet target size')
    p.add_argument('--no-quantize', action='store_true', help='Do not palette-quantize, keep truecolor PNG (RGBA). Size will be controlled by downscaling only')
    return p.parse_args()


def compress(input_path: str, output_path: str, max_side: int, colors: int, target_kb: int, square_size: int | None = None, no_quantize: bool = False, min_side: int = 256):
    im = Image.open(input_path).convert('RGBA')
    w, h = im.size
    # Optionally force to square canvas
    if square_size:
        # scale to fit inside square, but NEVER upscale (preserve sharpness)
        scale = min(1.0, min(square_size / w, square_size / h))
        nw, nh = int(round(w * scale)), int(round(h * scale))
        im_scaled = im.resize((nw, nh), Image.LANCZOS)
        canvas = Image.new('RGBA', (square_size, square_size), (0, 0, 0, 0))
        ox = (square_size - nw) // 2
        oy = (square_size - nh) // 2
        canvas.paste(im_scaled, (ox, oy))
        im = canvas
        nw, nh = im.size
        max_work_side = square_size
    else:
        # Downscale maintaining aspect ratio if needed
        longest = max(w, h)
        if longest > max_side:
            scale = max_side / float(longest)
            nw, nh = int(w * scale), int(h * scale)
            im = im.resize((nw, nh), Image.LANCZOS)
        else:
            nw, nh = w, h
        max_work_side = max_side

    def save_and_size(img, cols):
        if no_quantize:
            # Save truecolor PNG with max compression
            img.save(output_path, format='PNG', optimize=True, compress_level=9)
            return os.path.getsize(output_path)
        # Quantize to palette
        pal = img.convert('P', palette=Image.ADAPTIVE, colors=max(2, cols))
        pal.save(output_path, format='PNG', optimize=True)
        return os.path.getsize(output_path)

    size = save_and_size(im, colors)
    # Iteratively reduce if above target
    cur_colors = colors
    cur_side = max_work_side
    while size > target_kb * 1024 and ( (not no_quantize and cur_colors > 8) or cur_side > min_side ):
        if (not no_quantize) and cur_colors > 8:
            cur_colors = max(8, int(cur_colors * 0.8))
        elif cur_side > min_side:
            # reduce side in ~10% steps with a floor of min_side px
            cur_side = max(min_side, int(cur_side * 0.9))
        # Recompute image if side changed
        if not square_size and max(w, h) > cur_side:
            sc = cur_side / float(max(w, h))
            im2 = im.resize((int(nw * sc), int(nh * sc)), Image.LANCZOS)
        elif square_size and max_work_side > cur_side:
            # Recreate a smaller square canvas
            sc = cur_side / float(max_work_side)
            n2 = int(round(square_size * sc))
            im2 = im.resize((n2, n2), Image.LANCZOS)
        else:
            im2 = im
        size = save_and_size(im2, cur_colors)
    return (w, h), (nw, nh), cur_colors, size


def main():
    args = parse_args()
    before, after, cols, size = compress(args.input, args.output, args.max_side, args.colors, args.target_kb, args.square_size, args.no_quantize, args.min_side)
    print(f"Compressed {args.input}: {before[0]}x{before[1]} -> {after[0]}x{after[1]}, colors={cols}, size={size/1024:.1f}KB -> {args.output}")


if __name__ == '__main__':
    main()
