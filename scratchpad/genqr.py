# -*- coding: utf-8 -*-
"""Genera el QR de la seccion de descarga a partir de la URL de la ficha.

Se hace offline (nada de servicios de QR de terceros: son un enlace mas que
puede caer o cambiar de destino, y el QR se imprime en sitios donde no se
puede corregir). Salida: assets/images/qr-google-play.png, 444x444.

    pip install segno
    python scratchpad/genqr.py

Colores: los mismos del marco crema de la tarjeta, para que no cante un
blanco puro sobre el fondo de la seccion. El contraste sigue muy por encima
de lo que necesita un lector.

Borde de 2 modulos en vez de los 4 del estandar: la tarjeta que lo envuelve
ya aporta 12 px del mismo crema, asi que la zona tranquila real es mayor.
"""
import segno

URL = 'https://play.google.com/store/apps/details?id=com.aleix.orbex'
OUT = 'assets/images/qr-google-play.png'

qr = segno.make(URL, error='m')          # version 4 (33x33), correccion M
qr.save(OUT, scale=12, border=2, dark='#2a1c0c', light='#fff8ec')
print('%s  ->  %s (version %s, EC %s)' % (URL, OUT, qr.version, qr.error))
