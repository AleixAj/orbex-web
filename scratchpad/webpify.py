# -*- coding: utf-8 -*-
"""Regenera los .webp de la landing desde los originales.

Los originales (PNG/JPG) viven en `_source/originals/` con la misma jerarquia
de carpetas que `assets/`. Esa carpeta esta en .gitignore y en .netlifyignore,
asi que no se versiona ni se despliega: son la FUENTE, no el asset.

    python scratchpad/webpify.py           regenera todo
    python scratchpad/webpify.py --dry     solo dice que haria
    python scratchpad/webpify.py screenshots   solo los patrones que
                                               contengan esa palabra

Cada imagen se genera al tamano en que se PINTA, con el ancho a 2x del tamano
CSS real. Ahi esta el 94 % del ahorro: los diez retratos de jefe llegaban en
PNG de 1152x2048 (34 MB entre los diez) para pintarse a ~210 px de ancho.

Requiere Pillow:  pip install pillow
"""
import os
import sys
import glob
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_source", "originals", "assets")

# (patron dentro de assets/, ancho maximo, calidad)
JOBS = [
    ("images/bosses/*.png",        576, 80),   # tarjeta ~230 px CSS
    ("images/zones/*.png",         256, 85),   # escudo ~150 px CSS
    ("images/orbs/*.png",          160, 88),   # 38-54 px CSS (y la demo del canvas)
    ("images/avatars/*.png",       128, 85),   # 38 px CSS
    ("images/icons/*.png",         160, 88),
    ("images/orbex-title.png",    1120, 90),   # hero, max 560 px CSS
    ("images/screenshots/*.[jp][pn]g", 1280, 80),  # el lightbox la ensena a tamano real
    ("images/bg/espacio.jpg",     1600, 78),   # fondo del hero
]

# Las capturas ademas llevan miniatura: la tarjeta de la galeria mide ~275 px,
# asi que servirle la de 1280 costaba 1,5 MB en vez de 525 KB.
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
        sys.exit("No encuentro %s.\nAhi van los originales, con la misma "
                 "jerarquia de carpetas que assets/." % SRC)

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
        print("  %-40s          %5dK  %dx%d (miniatura de galeria)"
              % (rel, nsz // 1024, w, h))

    if before:
        print("\n  originales %.1f MB -> webp %.2f MB  (%.1f%% menos)"
              % (before / 1048576.0, after / 1048576.0,
                 100 - after * 100.0 / before))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(dry="--dry" in sys.argv, only=args[0] if args else "")
