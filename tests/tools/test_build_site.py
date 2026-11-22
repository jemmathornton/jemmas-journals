"""tools/build_site.py: the online-style copy has every site, and every file a page or stylesheet asks for is in it.

Builds into a temp folder (never _site/, which the 8060 preview may be serving), or uses JJ_BUILD_DIR if
tools/check_all.py already built one. About a minute: it copies every site (several hundred MB).
"""
import os, re, shutil, sys, tempfile, unittest
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from support import ROOT, load  # noqa: E402

APPS = ('library', 'sim-world', 'pokedex', 'travels')


class Refs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for k in ('src', 'href', 'data-dark', 'poster'):
            if a.get(k) and not (tag == 'a' and k == 'href'):   # links to pages are checked by the family suite
                self.refs.append((tag, a[k]))
        if a.get('srcset'):
            self.refs += [(tag, part.strip().split(' ')[0]) for part in a['srcset'].split(',') if part.strip()]
        if tag == 'meta' and a.get('property') in ('og:image',) and a.get('content', '').startswith('/'):
            self.refs.append((tag, a['content']))


def local(ref):
    return not re.match(r'^(#|%23|[a-z][a-z0-9+.-]*:|//)', ref, re.I) and '${' not in ref


class BuildSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bs = load(os.path.join('tools', 'build_site.py'))
        given = os.environ.get('JJ_BUILD_DIR')
        if given and os.path.exists(os.path.join(given, 'index.html')):
            cls.out, cls.own = given, False
        else:
            cls.out, cls.own = os.path.join(tempfile.mkdtemp(prefix='jj-build-'), '_site'), True
            cls.bs.OUT = cls.out
            cls.bs.build()

    @classmethod
    def tearDownClass(cls):
        if cls.own:
            shutil.rmtree(os.path.dirname(cls.out), ignore_errors=True)

    def resolve(self, page, ref):
        path = unquote(urlsplit(ref).path)
        if path.startswith('/'):
            return os.path.join(self.out, path.lstrip('/'))
        return os.path.normpath(os.path.join(os.path.dirname(page), path))

    def test_every_site_is_there(self):
        for rel in ['index.html', '404.html', 'robots.txt', 'favicon.ico', 'family/mode.js', 'family/family.js', 'family/family.css']:
            self.assertTrue(os.path.isfile(os.path.join(self.out, rel)), rel)
        for app in APPS:
            self.assertTrue(os.path.isfile(os.path.join(self.out, app, 'index.html')), app)

    def test_every_file_the_pages_ask_for_is_there(self):
        missing = []
        for d, _, files in os.walk(self.out):
            for f in files:
                if not f.endswith('.html'):
                    continue
                page = os.path.join(d, f)
                p = Refs()
                p.feed(open(page, encoding='utf-8', errors='replace').read())
                for tag, ref in p.refs:
                    if local(ref) and not os.path.exists(self.resolve(page, ref)):
                        missing.append(f'{os.path.relpath(page, self.out)}: <{tag}> {ref}')
        self.assertEqual(missing, [])

    def test_every_file_the_stylesheets_ask_for_is_there(self):
        missing = []
        for d, _, files in os.walk(self.out):
            for f in files:
                if not f.endswith('.css'):
                    continue
                sheet = os.path.join(d, f)
                for ref in re.findall(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)', open(sheet, encoding='utf-8', errors='replace').read()):
                    if local(ref) and not ref.startswith('data:') and not os.path.exists(self.resolve(sheet, ref)):
                        missing.append(f'{os.path.relpath(sheet, self.out)}: {ref}')
        self.assertEqual(missing, [])

    def test_the_apps_scripts_ask_only_for_files_that_are_there(self):
        """Pictures and data named literally in each app's scripts (e.g. "img/maps/x.webp"): a broken name shows online too."""
        missing = []
        for app in ('', *APPS):
            base = os.path.join(self.out, app)
            for d, _, files in os.walk(os.path.join(base, 'js') if app else base):
                if app == '' and os.path.relpath(d, base).split(os.sep)[0] in APPS:
                    continue
                for f in files:
                    if not f.endswith('.js'):
                        continue
                    src = open(os.path.join(d, f), encoding='utf-8', errors='replace').read()
                    for ref in set(re.findall(r'["\'`]((?:img|fonts|photos|data)/[A-Za-z0-9_./-]+\.(?:webp|jpg|jpeg|png|svg|woff2|json|ico))["\'`]', src)):
                        if not os.path.exists(os.path.join(base, ref)):
                            missing.append(f'{app or "home"}/{os.path.relpath(os.path.join(d, f), base)}: {ref}')
        self.assertEqual(missing, [])

    def test_no_python_caches_or_os_litter(self):
        bad = [os.path.relpath(os.path.join(d, f), self.out) for d, ds, fs in os.walk(self.out)
               for f in fs + ds if f in ('__pycache__', 'Thumbs.db', '.DS_Store') or f.endswith('.pyc')]
        self.assertEqual(bad, [])

    def test_fits_on_github_pages(self):
        size = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(self.out) for f in fs)
        self.assertLess(size, 1000 * 1000 * 1000, 'GitHub Pages allows 1 GB')

    def test_no_working_tools_or_notes_are_published(self):
        bad = [os.path.relpath(os.path.join(d, f), self.out) for d, _, fs in os.walk(self.out) for f in fs
               if f.endswith('.md') or (f.endswith('.html') and os.sep + 'tools' + os.sep in os.path.join(d, f))]
        self.assertEqual(bad, [])

    def test_every_published_page_asks_to_stay_out_of_search(self):
        bad = []
        for d, _, fs in os.walk(self.out):
            for f in fs:
                if f.endswith('.html') and os.sep + 'tools' + os.sep not in os.path.join(d, f):
                    if 'noindex, noai, noimageai' not in open(os.path.join(d, f), encoding='utf-8', errors='replace').read():
                        bad.append(os.path.relpath(os.path.join(d, f), self.out))
        self.assertEqual(bad, [])


if __name__ == '__main__':
    unittest.main()
