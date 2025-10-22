#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-crop PNG/JPG images to remove uniform borders (transparent or solid color),
with an optional margin to keep a small padding.

Usage:
  python scripts/autocrop_image.py --input <in.png> --output <out.png> --margin 12

Notes:
  - If the image has an alpha channel, transparent border is trimmed.
  - Otherwise, the top-left pixel color is used as background and removed within tolerance.
"""
import argparse
from PIL import Image, ImageChops


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--margin', type=int, default=12, help='Padding in pixels to retain around cropped content')
    p.add_argument('--tolerance', type=int, default=6, help='Color difference tolerance for non-alpha backgrounds')
    return p.parse_args()


def autocrop(im: Image.Image, margin: int, tolerance: int) -> Image.Image:
    # Prefer alpha-based trim if available
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        alpha = im.convert('RGBA').split()[-1]
        bbox = alpha.getbbox()
        if not bbox:
            return im
        left, top, right, bottom = bbox
    else:
        # Solid color trim based on top-left pixel with tolerance
        bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
        diff = ImageChops.difference(im, bg)
        # amplify differences
        for _ in range(3):
            diff = ImageChops.add(diff, diff)
        bbox = diff.getbbox()
        if not bbox:
            return im
        left, top, right, bottom = bbox

    # apply margin
    left = max(0, left - margin)
    top = max(0, top - margin)
    right = min(im.width, right + margin)
    bottom = min(im.height, bottom + margin)
    return im.crop((left, top, right, bottom))


def main():
    args = parse_args()
    im = Image.open(args.input)
    out = autocrop(im, args.margin, args.tolerance)
    out.save(args.output)
    print(f"Cropped {args.input} -> {args.output} ({im.size} -> {out.size})")


if __name__ == '__main__':
    main()
