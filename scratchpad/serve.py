# -*- coding: utf-8 -*-
"""Local development server.

    python scratchpad/serve.py           http://localhost:8000
    python scratchpad/serve.py 8080      another port

It is `python -m http.server` with two things on top:

- **`Cache-Control: no-store`**. The plain server sends `Last-Modified` and the
  browser keeps the cached HTML: you edit `index.html`, reload and see nothing.
  That is what forces people to reload with `?v=2`.
- **Correct MIME types** for `.webp` and `.woff2`. Without them the fonts are
  served as `application/octet-stream` and Chrome rejects them silently: the
  page falls back to the system font and it looks like a CSS problem.

It does nothing else. In production the headers come from `_headers`,
`netlify.toml` or `vercel.json`, which do cache for real.
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
        # Only what fails: one log line per .webp buries the one thing we care about.
        if args and str(args[1]).startswith(('4', '5')):
            sys.stderr.write("  %s %s\n" % (args[1], args[0]))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    handler = functools.partial(Handler, directory=ROOT)
    srv = ThreadingHTTPServer(('127.0.0.1', port), handler)
    print("Orbex - local server")
    print("  landing   http://localhost:%d/" % port)
    print("  privacy   http://localhost:%d/privacy/" % port)
    print("  (no cache: a normal reload shows the change)   Ctrl+C to stop")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == '__main__':
    main()
