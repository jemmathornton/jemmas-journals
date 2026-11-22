"""tools/new_site.py, on a throwaway copy of the parent: dry run changes nothing, a real run makes the site and wires it in
(every edited file still works), running twice changes nothing more, --add-to-home and --remove put things back exactly,
and bad names are refused before anything is written.
"""
import hashlib, os, py_compile, re, shutil, subprocess, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from support import ROOT, GitSandbox, load  # noqa: E402

NODE = os.path.join(ROOT, '.tools', 'node', 'node.exe')
COPY = ['tools/serve_all.py', 'tools/open_site.pyw', 'tools/check_all.py', 'tools/build_site.py', 'tools/backup_new_sites.py',
        'tools/setup_pc.ps1', 'tools/new_site.py', 'tests/axe_all.js', '.gitignore', 'site/home.js']
WIRED = ['tools/serve_all.py', 'tools/open_site.pyw', 'tools/check_all.py', 'tools/build_site.py', 'tests/axe_all.js']


class NewSite(unittest.TestCase):
    def setUp(self):
        self.box = GitSandbox().__enter__()
        self.parent = self.box.path('JemmasJournals')
        for rel in COPY:
            src = os.path.join(ROOT, rel)
            if os.path.exists(src):
                os.makedirs(os.path.dirname(os.path.join(self.parent, rel)), exist_ok=True)
                shutil.copy2(src, os.path.join(self.parent, rel))
        shutil.copytree(os.path.join(ROOT, 'templates', 'new-site'), os.path.join(self.parent, 'templates', 'new-site'))
        self.box.git(self.parent, 'init', '-q', '-b', 'main')
        self.before = self.snapshot()

    def tearDown(self):
        self.box.__exit__(None, None, None)

    def snapshot(self):
        out = {}
        for rel in COPY:
            p = os.path.join(self.parent, rel)
            if os.path.exists(p):
                out[rel] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        return out

    def new_site(self, *args):
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', os.path.join(self.parent, 'tools', 'new_site.py'), *args, '--parent', self.parent],
                           cwd=self.parent, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=120)
        return r.returncode, r.stdout + r.stderr

    def text(self, rel):
        return open(os.path.join(self.parent, rel), encoding='utf-8').read()

    def assertStillWorks(self):
        for rel in WIRED + ['tools/backup_new_sites.py']:
            p = os.path.join(self.parent, rel)
            if not os.path.exists(p):
                continue
            if rel.endswith(('.py', '.pyw')):
                py_compile.compile(p, cfile=os.path.join(self.box.dir, 'compiled.pyc'), doraise=True)
            elif rel.endswith('.js') and os.path.exists(NODE):
                r = subprocess.run([NODE, '--check', p], capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, f'{rel}: {r.stderr}')

    # ---- tests ----
    def test_dry_run_changes_nothing(self):
        code, out = self.new_site('recipes', 'Recipes', '--dry-run')
        self.assertEqual(code, 0, out)
        self.assertIn('would', out)
        self.assertFalse(os.path.exists(os.path.join(self.parent, 'recipes')))
        self.assertEqual(self.snapshot(), self.before)

    def test_a_real_run_makes_and_wires_the_site(self):
        code, out = self.new_site('recipes', 'Recipes', '#8A3B2E')
        self.assertEqual(code, 0, out)
        site = os.path.join(self.parent, 'recipes')
        self.assertTrue(os.path.exists(os.path.join(site, 'site', 'index.html')))
        self.assertEqual(self.box.git(site, 'rev-list', '--count', 'HEAD'), '1', 'its own git with a first commit')
        self.assertEqual(self.box.git(site, 'status', '--porcelain'), '')
        left = []
        for d, _, files in os.walk(site):
            if '.git' in d.split(os.sep):
                continue
            for f in files:
                if f.endswith(('.html', '.css', '.js', '.md', '.json')):
                    left += [f + ': ' + m for m in re.findall(r'__[A-Z_]+__', open(os.path.join(d, f), encoding='utf-8').read())]
        self.assertEqual(left, [], 'every placeholder filled in')
        index = open(os.path.join(site, 'site', 'index.html'), encoding='utf-8').read()
        self.assertIn('Jemma’s Recipes', index)
        for rel in WIRED:
            if os.path.exists(os.path.join(self.parent, rel)):
                self.assertIn('recipes', self.text(rel), rel)
        self.assertStillWorks()
        # the wiring means what it should
        sa = load(os.path.join(self.parent, 'tools', 'serve_all.py'))
        self.assertEqual(sa.APPS['recipes'], ('recipes/site', None, None))
        self.assertEqual(load(os.path.join(self.parent, 'tools', 'build_site.py')).APPS['recipes'], 'recipes/site')
        os_ = load(os.path.join(self.parent, 'tools', 'open_site.pyw'))
        self.assertEqual(os_.SITES['recipes'][0], '/recipes/')
        ca = load(os.path.join(self.parent, 'tools', 'check_all.py'))
        self.assertTrue(any(c[1].endswith('recipes') for c in ca.CHECKS), 'check_all runs its tests')
        self.assertEqual(self.text('site/home.js'), open(os.path.join(ROOT, 'site', 'home.js'), encoding='utf-8').read(), 'home unchanged without --add-to-home')

    def test_running_twice_changes_nothing_more(self):
        self.new_site('recipes', 'Recipes')
        once = self.snapshot()
        code, out = self.new_site('recipes', 'Recipes')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.snapshot(), once)

    def test_add_to_home_then_remove_puts_everything_back(self):
        self.new_site('recipes', 'Recipes')
        code, out = self.new_site('recipes', '--add-to-home')
        self.assertEqual(code, 0, out)
        home = self.text('site/home.js')
        self.assertIn('url:"/recipes/"', home)
        if os.path.exists(NODE):
            r = subprocess.run([NODE, '--check', os.path.join(self.parent, 'site', 'home.js')], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
        code, out = self.new_site('recipes', '--remove')
        self.assertEqual(code, 0, out)
        after = self.snapshot()
        for rel, h in self.before.items():
            self.assertEqual(after.get(rel), h, f'{rel} back exactly as it was')
        self.assertTrue(os.path.isdir(os.path.join(self.parent, 'recipes')), 'the folder itself is kept')

    def test_bad_folder_names_are_refused_before_anything_changes(self):
        for folder in ('Recipes', 'site', 'library', 'tools', '../x', 'a--b', '-a', 'a b', 'x' * 41, 'family', 'api'):
            code, out = self.new_site(folder, 'Recipes')
            self.assertNotEqual(code, 0, folder)
        self.assertEqual(self.snapshot(), self.before)
        self.assertEqual(sorted(os.listdir(self.parent)), sorted(['.git', '.gitignore', 'site', 'templates', 'tests', 'tools']))

    def test_bad_display_names_are_refused(self):
        for name in ('<b>', 'A "quote"', 'back\\slash', '${x}', 'x' * 41, 'tab\there'):
            code, out = self.new_site('recipes', name)
            self.assertNotEqual(code, 0, name)
        self.assertFalse(os.path.exists(os.path.join(self.parent, 'recipes')))
        self.assertEqual(self.snapshot(), self.before)

    def test_a_bad_colour_is_refused(self):
        code, out = self.new_site('recipes', 'Recipes', 'not-a-colour')
        self.assertNotEqual(code, 0)
        self.assertFalse(os.path.exists(os.path.join(self.parent, 'recipes')))

    def test_pale_accents_are_made_readable(self):
        ns = load(os.path.join('tools', 'new_site.py'))
        for accent in ('#FFFF00', '#EEEEEE', '#000000', '#3D6A8A'):
            light, dark, _ = ns.accents(accent)
            for bg in ns.LIGHT_BGS:
                self.assertGreaterEqual(ns.contrast(ns.rgb(light), ns.rgb(bg)), 4.5, f'{accent} light on {bg}')
            for bg in ns.DARK_BGS:
                self.assertGreaterEqual(ns.contrast(ns.rgb(dark), ns.rgb(bg)), 4.5, f'{accent} dark on {bg}')


if __name__ == '__main__':
    unittest.main()
