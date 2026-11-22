"""Put the whole family together exactly as it will be published online, and (optionally) serve it to try it out.

    python tools/build_site.py            builds _site/ (git-ignored)
    python tools/build_site.py --serve    builds, then serves _site/ at http://localhost:8060 like a plain web host

Her question, 22 Nov: "can you test it without rename?" Online there is no save server and nothing on her PC: just
these files. So this copies home (site/) to the top and each app's site/ folder under its name, and serves them with
a plain static server, no forwarding, no dark-mode help from the family server. What works here works online; the
Library and Pokédex show view-only, Travels' Write page says it needs her PC. The same build is what a publish
workflow would upload later (research/improvements-22-nov.md).
"""
import http.server, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '_site')
APPS = {'library': 'library/site', 'sim-world': 'sim-world/site', 'pokedex': 'pokedex/site', 'travels': 'travels/site'}
SKIP = {'__pycache__', '.DS_Store', 'Thumbs.db'}


def copy(src, dst):
    shutil.copytree(src, dst, ignore=lambda d, names: [n for n in names if n in SKIP or n.endswith('.pyc')])


def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    copy(os.path.join(ROOT, 'site'), OUT)
    for name, folder in APPS.items():
        if not os.path.isdir(os.path.join(ROOT, folder)):   # wired in by tools/new_site.py but the folder has gone
            print(f'skipped {name}: {folder} not found (a site from tools/new_site.py deleted by hand? its --remove takes the wiring out)')
            continue
        copy(os.path.join(ROOT, folder), os.path.join(OUT, name))
    size = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(OUT) for f in fs)
    count = sum(len(fs) for _, _, fs in os.walk(OUT))
    print(f'_site/: {count} files, {size / 1e6:.0f} MB (GitHub Pages allows 1,000 MB)')


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send_error(self, code, message=None, explain=None):   # a plain host shows its 404.html for missing pages
        page = os.path.join(OUT, '404.html')
        if code == 404 and os.path.exists(page) and self.command == 'GET':
            body = open(page, 'rb').read()
            self.send_response(404); self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body); return
        super().send_error(code, message, explain)


if __name__ == '__main__':
    build()
    if '--serve' in sys.argv:
        print('Online-style copy at http://localhost:8060/  (Ctrl+C to stop)', flush=True)
        os.chdir(OUT)
        http.server.ThreadingHTTPServer(('127.0.0.1', 8060), Quiet).serve_forever()
