# -*- coding: utf-8 -*-
"""Builds the QR of the download section from the store URL.

It runs offline on purpose. No third party QR service: that would be one more
link that can go down or change where it points, and a QR ends up printed in
places where it cannot be fixed. Output: assets/images/qr-google-play.png,
444x444.

    pip install segno
    python scratchpad/genqr.py

Colours are the cream and brown of the card around it, so it does not sit as a
hard white square on the section background. The contrast is still far above
what a reader needs.

A 2 module border instead of the 4 the standard asks for: the card around it
already adds 12 px of the same cream, so the real quiet zone is bigger.
"""
import segno

URL = 'https://play.google.com/store/apps/details?id=com.aleix.orbex'
OUT = 'assets/images/qr-google-play.png'

qr = segno.make(URL, error='m')          # version 4 (33x33), error correction M
qr.save(OUT, scale=12, border=2, dark='#2a1c0c', light='#fff8ec')
print('%s  ->  %s (version %s, EC %s)' % (URL, OUT, qr.version, qr.error))
