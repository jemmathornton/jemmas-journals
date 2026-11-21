"""The whole family on one address, as it will be online (21 Nov 2026, her layout: Jemma’s Journals is the parent).

    python tools/serve_all.py            http://localhost:8050

    /            the home page (site/)
    /library/    library/site      saves go on to the Library’s own server (8020)
    /sim-world/  sim-world/site
    /pokedex/    pokedex/site      saves go on to the Pokédex’s own server (8030)
    /travels/    travels/site      saves go on to the Travels server (8041)

Only this computer can reach it (127.0.0.1). Each app’s own server keeps running as before and still does the saving:
this one only shows the pages and passes save requests (…/api/…) on, so the apps’ own safety checks still apply.
Dark mode (jj-mode) carries across the sites here, and home’s Open links work, because it is all one address.
"""
import http.server, os, socketserver, sys, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[sys.argv.index('--port') + 1]) if '--port' in sys.argv else 8050
APPS = {   # address → (folder, the app's own save server or None)
    'library': ('library/site', 8020),
    'sim-world': ('sim-world/site', None),
    'pokedex': ('pokedex/site', 8030),
    'travels': ('travels/site', 8041),
}
PASS_HEADERS = ('Content-Type', 'X-Pokedex', 'X-Travels', 'X-Library', 'Accept')   # each app's own "only the site itself" header


class Handler(http.server.SimpleHTTPRequestHandler):
    def split(self):
        """(app name or None, path inside it) for this request."""
        path = self.path.split('?', 1)[0]
        parts = path.lstrip('/').split('/', 1)
        if parts[0] in APPS:
            return parts[0], '/' + (parts[1] if len(parts) > 1 else '')
        return None, path

    def translate_path(self, path):
        app, inner = self.split()
        base = os.path.join(ROOT, APPS[app][0]) if app else os.path.join(ROOT, 'site')
        self.directory = base
        return super().translate_path(inner if app else path)

    def do_GET(self):
        app, inner = self.split()
        if app and self.path.split('?', 1)[0] == '/' + app:   # /pokedex → /pokedex/ so the page's own links work
            self.send_response(301); self.send_header('Location', '/' + app + '/'); self.end_headers(); return
        if app and inner.startswith('/api/'):
            return self.forward(app, inner)
        return super().do_GET()

    def do_POST(self):
        app, inner = self.split()
        if app and inner.startswith('/api/'):
            return self.forward(app, inner)
        self.send_error(405)

    def forward(self, app, inner):
        port = APPS[app][1]
        if not port:
            return self.send_error(404)
        query = ('?' + self.path.split('?', 1)[1]) if '?' in self.path else ''
        body = self.rfile.read(int(self.headers.get('Content-Length') or 0)) if self.command == 'POST' else None
        req = urllib.request.Request(f'http://localhost:{port}{inner}{query}', data=body, method=self.command)
        for h in PASS_HEADERS:
            if self.headers.get(h):
                req.add_header(h, self.headers[h])
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                status, headers, data = r.status, r.headers, r.read()
        except urllib.error.HTTPError as e:
            status, headers, data = e.code, e.headers, e.read()
        except OSError:
            return self.send_error(503, f'The {app} server (port {port}) is not running')
        self.send_response(status)
        for h in ('Content-Type', 'Cache-Control'):
            if headers.get(h):
                self.send_header(h, headers[h])
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def end_headers(self):
        if not self.split()[1].startswith('/api/'):
            self.send_header('Cache-Control', 'no-cache')   # always the latest files while working on them
        super().end_headers()

    def log_message(self, *args):
        pass


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == '__main__':
    print(f'Jemma’s Journals and every app at http://localhost:{PORT}/  (Ctrl+C to stop)', flush=True)
    Server(('127.0.0.1', PORT), Handler).serve_forever()
