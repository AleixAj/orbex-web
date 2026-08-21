# -*- coding: utf-8 -*-
"""Servidor local para desarrollo.

    python scratchpad/serve.py           http://localhost:8000
    python scratchpad/serve.py 8080      otro puerto

Es `python -m http.server` con dos cosas encima:

- **`Cache-Control: no-store`**. El servidor pelado manda `Last-Modified` y el
  navegador se queda con el HTML cacheado: editas `index.html`, recargas y no
  ves nada. Es lo que obliga a andar recargando con `?v=2`.
- **Tipos MIME correctos** para `.webp` y `.woff2`. Sin ellos las fuentes se
  sirven como `application/octet-stream` y Chrome las rechaza en silencio: la
  pagina cae a la fuente del sistema y parece un problema del CSS.

No sirve para nada mas: en produccion las cabeceras las ponen `_headers`,
`netlify.toml` o `vercel.json`, que si cachean de verdad.
"""
import os
import sys
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Handler(SimpleHTTPRequestHandler):
    extensions_map = dict(SimpleHTTPRequestHandler.extensions_map)
    extensions_map.update({
        '.webp':  'image/webp',
        '.woff2': 'font/woff2',
        '.json':  'application/json',
    })

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        SimpleHTTPRequestHandler.end_headers(self)

    def log_message(self, fmt, *args):
        # Solo lo que falla: el log de cada .webp tapa lo unico que interesa.
        if args and str(args[1]).startswith(('4', '5')):
            sys.stderr.write("  %s %s\n" % (args[1], args[0]))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    handler = functools.partial(Handler, directory=ROOT)
    srv = ThreadingHTTPServer(('127.0.0.1', port), handler)
    print("Orbex - servidor local")
    print("  landing     http://localhost:%d/" % port)
    print("  privacidad  http://localhost:%d/privacy/" % port)
    print("  (sin cache: recarga normal y ves el cambio)   Ctrl+C para parar")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nparado")


if __name__ == '__main__':
    main()
