"""tools/record_apps.py: the parent records each app's new version, only when that is safe, and pushes.

Every test builds a throwaway family in a temp folder: bare "GitHub" remotes, a parent with two apps as submodules.
git runs with a test config (no sign-in helper of hers), and record_apps is pointed at the temp parent.
"""
import io, os, shutil, sys, unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from support import GitSandbox, load  # noqa: E402


class RecordApps(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # the family is built once (submodule add is slow on Windows) and copied for each test
        cls.box = GitSandbox().__enter__()
        b, cls.runs = cls.box, 0
        t = b.path('template')
        os.makedirs(t)
        b.dir, real = t, b.dir   # build inside template/
        b.repo_with_remote('library', {'site/index.html': 'lib\n'})
        b.repo_with_remote('pokedex', {'site/index.html': 'pok\n'})
        b.repo_with_remote('parent', {'README.md': 'parent\n'})
        lib_bare, pok_bare, parent_bare = (b.path('remotes', n + '.git') for n in ('library', 'pokedex', 'parent'))
        parent = b.path('JemmasJournals')
        b.git(t, 'clone', '-q', parent_bare, parent)
        b.git(parent, 'submodule', '-q', 'add', lib_bare, 'library')
        b.git(parent, 'submodule', '-q', 'add', pok_bare, 'pokedex')
        b.git(parent, 'commit', '-q', '-m', 'apps as submodules')
        b.git(parent, 'push', '-q')
        for app in ('library', 'pokedex'):   # as on her PC: each app on main, tracking GitHub
            b.git(os.path.join(parent, app), 'checkout', '-q', '-B', 'main', '--track', 'origin/main')
        b.dir = real
        cls.template = t

    @classmethod
    def tearDownClass(cls):
        cls.box.__exit__(None, None, None)

    def setUp(self):
        b = self.box
        RecordApps.runs += 1
        run = b.path(f'run{self.runs}')
        shutil.copytree(self.template, run, symlinks=True)
        self.lib_bare, self.pok_bare = os.path.join(run, 'remotes', 'library.git'), os.path.join(run, 'remotes', 'pokedex.git')
        self.parent_bare, self.parent = os.path.join(run, 'remotes', 'parent.git'), os.path.join(run, 'JemmasJournals')
        b.git(self.parent, 'remote', 'set-url', 'origin', self.parent_bare)   # the copies' remotes point at the copied remotes
        b.git(os.path.join(self.parent, 'library'), 'remote', 'set-url', 'origin', self.lib_bare)
        b.git(os.path.join(self.parent, 'pokedex'), 'remote', 'set-url', 'origin', self.pok_bare)
        self.rec = load(os.path.join('tools', 'record_apps.py'))
        self.rec.ROOT = self.parent
        self.rec.APPS = ['library', 'pokedex']
        # record_apps' git() has cwd=ROOT as a default argument, fixed when the module loads: changing ROOT alone would leave
        # its parent commands running in her real Jemma's Journals. Every git call is sent to the temp family, and refused
        # anywhere else.
        real_git, box = self.rec.git, self.box

        def git(*args, cwd=None):
            cwd = cwd or self.parent
            if not os.path.normcase(os.path.abspath(cwd)).startswith(os.path.normcase(box.dir)):
                raise AssertionError(f'record_apps tried to run git in {cwd}, outside the test folder')
            return real_git(*args, cwd=cwd)
        self.rec.git = git

    # ---- helpers ----
    def run_it(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = self.rec.main()
        return code, out.getvalue()

    def app_commit(self, app, rel='site/index.html', text='new\n', push=True):
        p = os.path.join(self.parent, app)
        self.box.write(os.path.join(p, rel), text)
        self.box.git(p, 'add', '-A')
        self.box.git(p, 'commit', '-q', '-m', 'change ' + rel)
        if push:
            self.box.git(p, 'push', '-q')
        return self.box.git(p, 'rev-parse', 'HEAD')

    def recorded(self, app, ref='HEAD'):
        return self.box.git(self.parent, 'ls-tree', ref, app).split()[2]

    def parent_head(self):
        return self.box.git(self.parent, 'rev-parse', 'HEAD')

    # ---- tests ----
    def test_a_new_pushed_version_is_recorded_and_pushed(self):
        sha = self.app_commit('library')
        code, out = self.run_it()
        self.assertEqual(code, 0, out)
        self.assertIn('recorded and pushed: library', out)
        self.assertEqual(self.recorded('library'), sha)
        self.assertEqual(self.box.git(self.parent, 'log', '-1', '--format=%s'), 'Record app versions: library')
        self.assertEqual(self.box.git(self.parent_bare, 'rev-parse', 'main'), self.parent_head(), 'pushed')
        self.assertEqual(self.box.git(self.parent, 'show', '--name-only', '--format=', 'HEAD'), 'library', 'only the app')

    def test_two_apps_in_one_commit(self):
        self.app_commit('library'); self.app_commit('pokedex')
        code, out = self.run_it()
        self.assertEqual(code, 0, out)
        self.assertEqual(self.box.git(self.parent, 'log', '-1', '--format=%s'), 'Record app versions: library, pokedex')

    def test_nothing_new(self):
        head = self.parent_head()
        code, out = self.run_it()
        self.assertEqual(code, 0)
        self.assertIn('nothing new to record', out)
        self.assertEqual(self.parent_head(), head)

    def test_uncommitted_changes_are_skipped(self):
        self.app_commit('library')
        self.box.write(os.path.join(self.parent, 'library', 'site', 'index.html'), 'half done\n')
        head = self.parent_head()
        code, out = self.run_it()
        self.assertIn('library: has uncommitted changes, not recorded', out)
        self.assertEqual(self.parent_head(), head)
        self.assertEqual(code, 0)

    def test_an_untracked_new_file_is_uncommitted_work_too(self):
        self.app_commit('library')
        self.box.write(os.path.join(self.parent, 'library', 'site', 'new.js'), 'x\n')
        code, out = self.run_it()
        self.assertIn('library: has uncommitted changes', out)

    def test_a_backups_own_log_does_not_count(self):
        sha = self.app_commit('pokedex', 'logs/backup.log', 'old line\n')
        self.box.write(os.path.join(self.parent, 'pokedex', 'logs', 'backup.log'), 'old line\nnew line\n')   # written after the commit
        self.box.write(os.path.join(self.parent, 'pokedex', 'logs', 'other.log'), 'x\n')
        code, out = self.run_it()
        self.assertEqual(code, 0, out)
        self.assertIn('recorded and pushed: pokedex', out)
        self.assertEqual(self.recorded('pokedex'), sha)

    def test_not_on_main_is_skipped(self):
        p = os.path.join(self.parent, 'library')
        self.box.git(p, 'checkout', '-q', '-b', 'trial')
        self.app_commit('library', push=False)
        code, out = self.run_it()
        self.assertIn('library: not on main, not recorded', out)

    def test_commits_not_yet_pushed_are_skipped(self):
        self.app_commit('library', push=False)
        head = self.parent_head()
        code, out = self.run_it()
        self.assertIn('library: has commits not yet pushed, not recorded', out)
        self.assertEqual(self.parent_head(), head)

    def test_other_changes_in_the_parent_are_left_alone(self):
        self.app_commit('library')
        self.box.write(os.path.join(self.parent, 'README.md'), 'someone is editing this\n')
        self.box.write(os.path.join(self.parent, 'staged.txt'), 'staged by someone\n')
        self.box.git(self.parent, 'add', 'staged.txt')
        code, out = self.run_it()
        self.assertEqual(code, 0, out)
        self.assertEqual(self.box.git(self.parent, 'show', '--name-only', '--format=', 'HEAD'), 'library')
        status = self.box.git(self.parent, 'status', '--porcelain')
        self.assertRegex(status, r'(^| )M README.md')
        self.assertIn('A  staged.txt', status)

    def test_the_parent_not_on_main(self):
        self.box.git(self.parent, 'checkout', '-q', '-b', 'side')
        self.app_commit('library')
        code, out = self.run_it()
        self.assertEqual(code, 1)
        self.assertIn('not on main', out)

    def test_a_failed_push_is_reported(self):
        self.app_commit('library')
        self.box.git(self.parent, 'remote', 'set-url', 'origin', self.box.path('nowhere.git'))
        code, out = self.run_it()
        self.assertEqual(code, 1)
        self.assertIn('recorded, but the push failed', out)

    def test_an_app_that_is_not_there_is_ignored(self):
        self.rec.APPS = ['library', 'pokedex', 'travels']
        self.app_commit('library')
        code, out = self.run_it()
        self.assertEqual(code, 0, out)
        self.assertIn('recorded and pushed: library', out)

    def test_every_push_and_fetch_uses_the_github_cli_or_nothing(self):
        src = open(self.rec.__file__, encoding='utf-8').read()
        for line in src.splitlines():
            if "'push'" in line or "'fetch'" in line:
                self.assertIn("'-c', 'credential.helper='", line, line.strip())


if __name__ == '__main__':
    unittest.main()
