"""The whole family on one address, as it will be online (21 Nov 2026, her layout: Jemma’s Journals is the parent).

    pythonw tools/serve_all.py           http://localhost:8050   (started at login; tools/open_site.pyw starts it if needed)

    /            the home page (site/)          /family/   the shared code every site loads (site/family/)
    /library/    library/site      saves go on to the Library’s own server (8020)
    /sim-world/  sim-world/site
    /pokedex/    pokedex/site      saves go on to the Pokédex’s own server (8030)
    /travels/    travels/site      saves go on to the Travels server (8041)

Only this computer can reach it (127.0.0.1), and only by the names localhost / 127.0.0.1 (a page elsewhere pointing its own name
at this computer gets nothing: round 3 review). Each app’s own server keeps doing the saving, with its own checks; this one shows
the pages and passes save requests (…/api/…) on. It starts any app server that isn’t running. Dark mode (jj-mode) carries across
the sites here, and home’s Open links work, because it is all one address.
"""
import http.server, os, socket, socketserver, subprocess, sys, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[sys.argv.index('--port') + 1]) if '--port' in sys.argv else 8050
APPS = {   # address → (folder, the app's own save server port or None, the script that runs it)
    'library': ('library/site', 8020, 'library/tools/serve.py'),
    'sim-world': ('sim-world/site', None, None),
    'pokedex': ('pokedex/site', 8030, 'pokedex/tools/serve.py'),
    'travels': ('travels/site', 8041, 'travels/tools/serve.py'),
}
PASS_HEADERS = ('Content-Type', 'X-Pokedex', 'X-Travels', 'X-Library', 'Accept')   # each app's own "only the site itself" header
NOT_FOUND = os.path.join(ROOT, 'site', '404.html')
# Dark mode for every window on her PC: the app windows each have their own Chrome profile (their own taskbar buttons),
# so their localStorage isn't shared. The family server keeps her choice here and writes it into every page it sends
# (<html data-jj-server-mode="dark">), which /family/mode.js reads before the page draws; family.js saves changes back.
MODE_FILE = os.path.join(ROOT, 'logs', 'family-mode.txt')


def saved_mode():
    try:
        m = open(MODE_FILE, encoding='utf-8').read().strip()
        return m if m in ('dark', 'light') else 'light'
    except OSError:
        return 'light'


def answering(port):
    try:
        with socket.create_connection(('127.0.0.1', port), timeout=0.5):
            return True
    except OSError:
        return False


def start_app_servers():
    """Start each app's own save server if it isn't running (detached, so it keeps running on its own)."""
    pyw = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
    exe = pyw if os.path.exists(pyw) else sys.executable
    for name, (_, port, script) in APPS.items():
        if port and script and not answering(port) and os.path.exists(os.path.join(ROOT, script)):
            flags = 0x00000008 | 0x00000200 if os.name == 'nt' else 0   # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
            subprocess.Popen([exe, os.path.join(ROOT, script)], cwd=os.path.join(ROOT, name), creationflags=flags,
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)


class Handler(http.server.SimpleHTTPRequestHandler):
    def split(self):
        """(app name or None, path inside it) for this request."""
        path = getattr(self, 'path', '/').split('?', 1)[0]
        parts = path.lstrip('/').split('/', 1)
        if parts[0] in APPS:
            return parts[0], '/' + (parts[1] if len(parts) > 1 else '')
        return None, path

    def host_ok(self):
        if '\x00' in urllib.parse.unquote(getattr(self, 'path', '')):   # a NUL in the address dropped the connection (round 4)
            return False
        return (self.headers.get('Host') or '').lower() in (f'localhost:{PORT}', f'127.0.0.1:{PORT}')

    def translate_path(self, path):
        app, inner = self.split()
        self.directory = os.path.join(ROOT, APPS[app][0]) if app else os.path.join(ROOT, 'site')
        return super().translate_path(inner if app else path)

    def list_directory(self, path):   # no folder listings
        self.send_error(404)
        return None

    def send_error(self, code, message=None, explain=None):
        if code == 404 and os.path.exists(NOT_FOUND) and getattr(self, 'command', '') in ('GET', 'HEAD'):
            return self.send_page(NOT_FOUND, 404)
        super().send_error(code, message, explain)

    def do_GET(self):
        if not self.host_ok():
            return super().send_error(403)
        app, inner = self.split()
        if app and self.path.split('?', 1)[0] == '/' + app:   # /pokedex → /pokedex/ so the page's own links work
            query = ('?' + self.path.split('?', 1)[1]) if '?' in self.path else ''
            self.send_response(301); self.send_header('Location', '/' + app + '/' + query); self.end_headers(); return
        if app and inner.startswith('/api/'):
            return self.forward(app, inner)
        if self.path.split('?', 1)[0] == '/family/mode':
            return self.reply_text(saved_mode())
        local = self.translate_path(self.path)
        if os.path.isdir(local) and self.path.split('?', 1)[0].endswith('/'):
            local = os.path.join(local, 'index.html')
        if local.endswith('.html') and os.path.isfile(local):
            return self.send_page(local, 200)
        return super().do_GET()

    def send_page(self, local, status):
        """An HTML page, with her dark-mode choice written into the <html> tag."""
        html = open(local, 'rb').read()
        tag = b' data-jj-server-mode="' + saved_mode().encode() + b'"'
        i = html.lower().find(b'<html')
        html = html[:i + 5] + tag + html[i + 5:] if i >= 0 else html
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(html)))
        self.end_headers()
        if self.command == 'GET':
            self.wfile.write(html)

    def reply_text(self, text, status=200):
        data = text.encode()
        self.send_response(status)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_HEAD(self):
        if not self.host_ok():
            return super().send_error(403)
        return super().do_HEAD()

    def do_POST(self):
        if not self.host_ok():
            return super().send_error(403)
        app, inner = self.split()
        if app and inner.startswith('/api/'):
            return self.forward(app, inner)
        if self.path == '/family/mode' and self.headers.get('X-Family') == '1':   # family.js saves her choice
            m = self.rfile.read(min(int(self.headers.get('Content-Length') or 0), 16)).decode('utf-8', 'replace').strip()
            if m not in ('dark', 'light'):
                return self.reply_text('bad mode', 400)
            os.makedirs(os.path.dirname(MODE_FILE), exist_ok=True)
            with open(MODE_FILE + '.tmp', 'w', encoding='utf-8') as f:
                f.write(m)
            os.replace(MODE_FILE + '.tmp', MODE_FILE)   # written whole, never half
            return self.reply_text(m)
        super().send_error(405)

    def forward(self, app, inner):
        port = APPS[app][1]
        if not port:
            return self.send_error(404)
        query = ('?' + self.path.split('?', 1)[1]) if '?' in self.path else ''
        try:
            size = int(self.headers.get('Content-Length') or 0)
        except ValueError:
            return super().send_error(400)
        if size < 0 or size > 64 * 1024 * 1024:   # posts with photos are big, but not this big
            return super().send_error(413)
        body = self.rfile.read(size) if self.command == 'POST' else None
        # 127.0.0.1, not localhost: on Windows "localhost" tries ::1 first and waits about 2 s per address (round 3 review)
        req = urllib.request.Request(f'http://127.0.0.1:{port}{inner}{query}', data=body, method=self.command)
        for h in PASS_HEADERS:
            if self.headers.get(h):
                req.add_header(h, self.headers[h])
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                status, headers, data = r.status, r.headers, r.read()
        except urllib.error.HTTPError as e:
            status, headers, data = e.code, e.headers, e.read()
        except OSError:
            start_app_servers()   # it may have stopped: start it for next time
            return super().send_error(503, f'The {app} server (port {port}) is not running')
        self.send_response(status)
        for h in ('Content-Type', 'Cache-Control'):
            if headers.get(h):
                self.send_header(h, headers[h])
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def end_headers(self):
        if hasattr(self, 'path') and not self.split()[1].startswith('/api/'):
            self.send_header('Cache-Control', 'no-cache')   # always the latest files while working on them
        super().end_headers()

    def log_message(self, *args):
        pass


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    request_queue_size = 128   # every picture is its own connection; the default 5 refused some under load (round 4 review)
    allow_reuse_address = False   # a second copy must fail to start, not share the port


if __name__ == '__main__':
    if answering(PORT):
        sys.exit(0)   # already running
    start_app_servers()
    print(f'Jemma’s Journals and every app at http://localhost:{PORT}/  (Ctrl+C to stop)', flush=True)
    Server(('127.0.0.1', PORT), Handler).serve_forever()
