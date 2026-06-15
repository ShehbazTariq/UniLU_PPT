#!/usr/bin/env python3
"""Flood-fill the solid (usually black/white) background of a logo or QR card
to transparency, so it sits cleanly on the navy slides.

ImageMagick is not assumed to be installed; this uses Pillow only.

Usage:
    python clean_bg.py INPUT [OUTPUT] [--thresh N] [--fill transparent|navy]

    INPUT            image to clean (jpg/png)
    OUTPUT           default: <input-stem>_clean.png
    --thresh N       colour-distance threshold for the flood fill (default 70)
    --fill MODE      'transparent' (default) or 'navy' (#1d2c44)

The fill starts from the four corners plus the top/bottom midpoints, so only
the connected outer background is replaced. Inner content (QR modules, a dark
photo, the envelope glyph, etc.) is left untouched because it is not connected
to the border.

Examples:
    python clean_bg.py Assets/QR_Linkedin.jpg
    python clean_bg.py Assets/Email.png Assets/Email_clean.png --thresh 80
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw

NAVY = (29, 44, 68, 255)  # #1d2c44


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output", nargs="?")
    ap.add_argument("--thresh", type=int, default=70)
    ap.add_argument("--fill", choices=["transparent", "navy"], default="transparent")
    args = ap.parse_args()

    src = Path(args.input)
    dst = Path(args.output) if args.output else src.with_name(src.stem + "_clean.png")

    im = Image.open(src).convert("RGBA")
    w, h = im.size
    value = (0, 0, 0, 0) if args.fill == "transparent" else NAVY

    seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1)]
    for seed in seeds:
        ImageDraw.floodfill(im, seed, value, thresh=args.thresh)

    im.save(dst)
    print(f"wrote {dst} ({im.size[0]}x{im.size[1]})")


if __name__ == "__main__":
    main()
