"""Put the whole family together exactly as it will be published online, and (optionally) serve it to try it out.

    python tools/build_site.py            builds _site/ (git-ignored)
    python tools/build_site.py --serve    builds, then serves _site/ at http://localhost:8060 like a plain web host
    python tools/build_site.py --base /jemmas-journals/
                                          builds for an address below the root (GitHub Pages' project address,
                                          https://jemmathornton.github.io/jemmas-journals/): the pages' root links
                                          ("/", "/family/", "/sim-world/" ...) are rewritten to start with the base.
                                          Used by .github/workflows/publish.yml (28 Nov).

Her question, 22 Nov: "can you test it without rename?" Online there is no save server and nothing on her PC: just
these files. So this copies home (site/) to the top and each app's site/ folder under its name, and serves them with
a plain static server, no forwarding, no dark-mode help from the family server. What works here works online; the
Library and Pokédex show view-only, Travels' Write page says it needs her PC. The same build is what a publish
workflow would upload later (research/improvements-22-nov.md).

Only files git tracks are copied (git ls-files, in the parent for site/ and in each app for its site/; round 5 review),
so git-ignored and new untracked files never get published; tracked files are copied as they are now. Left out:
site/tools/ (the icon drawing canvas).
"""
import http.server, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '_site')
APPS = {'library': 'library/site', 'sim-world': 'sim-world/site', 'pokedex': 'pokedex/site', 'travels': 'travels/site'}
LEAVE_OUT = ('tools/', 'family/README.md')   # inside home's site/: the icon drawing canvas (site/tools/draw-icon.html) and the shared code's notes are not part of the site


def tracked(repo, folder='site'):
    """The files git tracks under repo/folder, as paths inside folder."""
    r = subprocess.run(['git', '-c', 'core.quotepath=off', 'ls-files', '-z', '--', folder + '/'], cwd=repo,
                       capture_output=True, check=True)
    return [p[len(folder) + 1:] for p in r.stdout.decode('utf-8').split('\0') if p.startswith(folder + '/')]


def copy(repo, dst, leave_out=()):
    """Copy the tracked files of repo/site into dst."""
    n = 0
    for rel in tracked(repo):
        if rel.startswith(leave_out):
            continue
        src = os.path.join(repo, 'site', *rel.split('/'))
        if not os.path.isfile(src):   # tracked but deleted in the working folder (or a submodule entry)
            continue
        out = os.path.join(dst, *rel.split('/'))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copy2(src, out)
        n += 1
    return n


REWRITE_EXT = ('.html', '.js', '.css')
REWRITE_SKIP = ('/js/ocr/',)   # vendored OCR code: its "/" strings are paths inside the OCR engine, not links


def root_links(base):
    """The pattern and replacement that move the pages' root links under base (e.g. "/jemmas-journals/")."""
    tops = sorted({'family', 'img', 'fonts', 'favicon.ico', *APPS})
    pat = re.compile(r"""(["'(])/(""" + '|'.join(re.escape(t) for t in tops) + r""")(?=[/"')?#])|(href=["'])/(["'])""")

    def sub(m):
        if m.group(3):
            return m.group(3) + base + m.group(4)
        return m.group(1) + base + m.group(2)
    return pat, sub


def rebase(base):
    """Rewrite root links in the built pages, scripts and styles so the family works below the root of an address."""
    if base == '/':
        return 0
    pat, sub = root_links(base)
    n = 0
    for d, _, fs in os.walk(OUT):
        for f in fs:
            path = os.path.join(d, f)
            if not f.endswith(REWRITE_EXT) or any(x in path.replace(os.sep, '/') for x in REWRITE_SKIP):
                continue
            with open(path, encoding='utf-8') as fh:
                text = fh.read()
            new = pat.sub(sub, text)
            if new != text:
                with open(path, 'w', encoding='utf-8', newline='') as fh:
                    fh.write(new)
                n += 1
    return n


def build(base='/'):
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    copy(ROOT, OUT, LEAVE_OUT)
    for name, folder in APPS.items():
        if not os.path.isdir(os.path.join(ROOT, folder)):   # wired in by tools/new_site.py but the folder has gone
            print(f'skipped {name}: {folder} not found (a site from tools/new_site.py deleted by hand? its --remove takes the wiring out)')
            continue
        copy(os.path.join(ROOT, os.path.dirname(folder)), os.path.join(OUT, name))
    if base != '/':
        print(f'root links moved under {base} in {rebase(base)} files')
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


def base_arg(argv):
    """--base X: always starts and ends with "/" ("" or "/" means the root)."""
    if '--base' not in argv:
        return '/'
    b = argv[argv.index('--base') + 1].strip('/')
    return '/' + b + '/' if b else '/'


if __name__ == '__main__':
    build(base_arg(sys.argv))
    if '--serve' in sys.argv:
        print('Online-style copy at http://localhost:8060/  (Ctrl+C to stop)', flush=True)
        os.chdir(OUT)
        http.server.ThreadingHTTPServer(('127.0.0.1', 8060), Quiet).serve_forever()
