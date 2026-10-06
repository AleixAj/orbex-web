# -*- coding: utf-8 -*-
"""Rebuilds the .webp files of the landing page from the originals.

The originals (PNG/JPG) live in `_source/originals/` with the same folder
layout as `assets/`. That folder is in .gitignore and in .netlifyignore, so it
is neither versioned nor deployed: it is the SOURCE, not the asset.

    python scratchpad/webpify.py           rebuild everything
    python scratchpad/webpify.py --dry     only say what it would do
    python scratchpad/webpify.py screenshots   only the patterns containing
                                               that word

Every image is built at the size it is PAINTED at, with the width at 2x the
real CSS size. That is where 94 % of the saving is: the ten boss portraits
arrived as 1152x2048 PNGs (34 MB between them) to be painted about 210 px wide.

Needs Pillow:  pip install pillow
"""
import os
import sys
import glob
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_source", "originals", "assets")

# (pattern inside assets/, max width, quality)
JOBS = [
    ("images/bosses/*.png",        576, 80),   # card about 230 px CSS
    ("images/zones/*.png",         256, 85),   # crest about 150 px CSS
    ("images/orbs/*.png",          160, 88),   # 38-54 px CSS (and the canvas demo)
    ("images/avatars/*.png",       128, 85),   # 38 px CSS
    ("images/icons/*.png",         160, 88),
    ("images/orbex-title.png",    1120, 90),   # hero, 560 px CSS at most
    ("images/screenshots/*.[jp][pn]g", 1280, 80),  # the lightbox shows it full size
    ("images/bg/espacio.jpg",     1600, 78),   # hero background
]

# Screenshots also get a thumbnail: the gallery card is about 275 px wide, so
# serving it the 1280 one cost 1.5 MB instead of 525 KB.
THUMB = ("images/screenshots/*.[jp][pn]g", 720, 78)


def convert(src, dst, maxw, quality, dry):
    im = Image.open(src)
    w, h = im.size
    if w > maxw:
        h = round(h * maxw / w)
        w = maxw
        im = im.resize((w, h), Image.LANCZOS)
    if im.mode == "P":
        im = im.convert("RGBA")
    if not dry:
        d = os.path.dirname(dst)
        if d and not os.path.isdir(d):
            os.makedirs(d)
        im.save(dst, "WEBP", quality=quality, method=6)
    return w, h, os.path.getsize(dst) if os.path.exists(dst) else 0


def main(dry=False, only=""):
    if not os.path.isdir(SRC):
        sys.exit("Cannot find %s.\nThat is where the originals go, with the "
                 "same folder layout as assets/." % SRC)

    before = after = 0
    for pattern, maxw, q in JOBS:
        if only and only not in pattern:
            continue
        for src in sorted(glob.glob(os.path.join(SRC, pattern))):
            rel = os.path.relpath(src, SRC).replace("\\", "/")
            dst = os.path.join(ROOT, "assets", os.path.splitext(rel)[0] + ".webp")
            w, h, nsz = convert(src, dst, maxw, q, dry)
            before += os.path.getsize(src)
            after += nsz
            print("  %-40s %6dK -> %5dK  %dx%d"
                  % (rel, os.path.getsize(src) // 1024, nsz // 1024, w, h))

    pattern, maxw, q = THUMB
    if not only or only in pattern:
        for src in sorted(glob.glob(os.path.join(SRC, pattern))):
            rel = os.path.relpath(src, SRC).replace("\\", "/")
            dst = os.path.join(ROOT, "assets", os.path.splitext(rel)[0] + "-thumb.webp")
            w, h, nsz = convert(src, dst, maxw, q, dry)
            after += nsz
            print("  %-40s          %5dK  %dx%d (gallery thumbnail)"
                  % (rel, nsz // 1024, w, h))

    if before:
        print("\n  originals %.1f MB -> webp %.2f MB  (%.1f%% less)"
              % (before / 1048576.0, after / 1048576.0,
                 100 - after * 100.0 / before))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(dry="--dry" in sys.argv, only=args[0] if args else "")
