"""tools/weekly.py, the family's one daily backup job: which jobs run when, one failing doesn't stop the rest, and the
Travels backup commits only the Write page's files.

Runs in temp folders: the apps' jobs are tiny stand-in scripts, Travels is a throwaway repo with a bare "GitHub" remote,
the log goes to a temp file, and record_apps is a stand-in too. Nothing of hers is touched.
"""
import io, os, sys, tempfile, unittest
from datetime import datetime
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from support import GitSandbox, load  # noqa: E402

SUNDAY, MONDAY = datetime(2026, 11, 22, 9, 30), datetime(2026, 11, 23, 9, 30)


def fence(w, folder):
    """Every git and job command weekly.py runs must be inside the test folder (never her real repos)."""
    real_git, real_run = w.git, w.run

    def inside(cwd):
        if not os.path.normcase(os.path.abspath(cwd)).startswith(os.path.normcase(os.path.abspath(folder))):
            raise AssertionError(f'weekly.py tried to work in {cwd}, outside the test folder')

    def git(cwd, *args, **kw):
        inside(cwd); return real_git(cwd, *args, **kw)

    def run(cmd, cwd, limit):
        inside(cwd); return real_run(cmd, cwd, limit)
    w.git, w.run = git, run


def fixed_now(when):
    class Fixed(datetime):
        @classmethod
        def now(cls, tz=None):
            return when
    return Fixed


class WhenTheWeeklyJobRuns(unittest.TestCase):
    """weekly_due: Sundays, or when the Gallery refresh's last good run is overdue; --all forces it, --daily-only skips it."""

    def setUp(self):
        self.w = load(os.path.join('tools', 'weekly.py'))
        if not hasattr(self.w, 'weekly_due'):
            self.skipTest('weekly.py has no weekly_due (older version)')

    def due(self, now, last=None, argv=()):
        return self.w.weekly_due(now=now, last=last, argv=['weekly.py', *argv])[0]

    def test_sundays(self):
        self.assertTrue(self.due(SUNDAY, last=datetime(2026, 11, 21)))

    def test_not_on_other_days_when_it_ran_lately(self):
        self.assertFalse(self.due(MONDAY, last=datetime(2026, 11, 22, 10, 0)))
        self.assertFalse(self.due(datetime(2026, 11, 28, 9, 30), last=datetime(2026, 11, 22, 10, 0)), 'Saturday after a Sunday run')

    def test_catches_up_when_overdue(self):
        self.assertTrue(self.due(MONDAY, last=datetime(2026, 11, 15, 10, 0)), 'Sunday missed (PC off)')

    def test_no_good_run_known(self):
        self.assertTrue(self.due(MONDAY, last=None))

    def test_flags(self):
        self.assertTrue(self.due(MONDAY, last=datetime(2026, 11, 22), argv=['--all']))
        self.assertFalse(self.due(SUNDAY, argv=['--daily-only']))
        self.assertFalse(self.due(SUNDAY, argv=['--all', '--daily-only']), '--daily-only wins')


class ReadingTheGalleryLog(unittest.TestCase):
    def setUp(self):
        self.w = load(os.path.join('tools', 'weekly.py'))
        if not hasattr(self.w, 'last_gallery_ok'):
            self.skipTest('weekly.py has no last_gallery_ok (older version)')
        self.tmp = tempfile.mkdtemp(prefix='jj-weekly-')

    def log(self, text):
        p = os.path.join(self.tmp, 'gallery-refresh.log')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(text)
        return p

    def test_the_last_finished_run(self):
        p = self.log('Gallery refresh, 15 Nov 2026 09:31\nFinished\nGallery refresh, 22 Nov 2026 09:30\nStopped with an error: x\n'
                     'Gallery refresh, 20 Nov 2026 11:00\nSaved in the project history\n')
        self.assertEqual(self.w.last_gallery_ok(p), datetime(2026, 11, 20, 11, 0))

    def test_problems_are_not_good(self):
        p = self.log('Gallery refresh, 22 Nov 2026 09:30\nFinished with problems\n')
        self.assertIsNone(self.w.last_gallery_ok(p))

    def test_no_log(self):
        self.assertIsNone(self.w.last_gallery_ok(os.path.join(self.tmp, 'missing.log')))


class TheJobs(unittest.TestCase):
    """main(): stand-in jobs that write a marker file; Travels and record_apps stood in too."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='jj-weekly-')
        self.w = load(os.path.join('tools', 'weekly.py'))
        self.w.ROOT = self.tmp
        self.w.LOG = os.path.join(self.tmp, 'logs', 'weekly.log')
        if hasattr(self.w, 'GALLERY_LOG'):
            self.w.GALLERY_LOG = os.path.join(self.tmp, 'missing.log')
        self.w.PY = sys.executable
        fence(self.w, self.tmp)
        for folder, code in (('sim-world', 0), ('library', 3), ('pokedex', 0)):
            os.makedirs(os.path.join(self.tmp, folder, 'tools'))
            script = 'gallery_refresh.py' if folder == 'sim-world' else 'backup.py'
            with open(os.path.join(self.tmp, folder, 'tools', script), 'w') as f:
                f.write(f"open('ran.txt', 'w').write('x'); print('job output'); raise SystemExit({code})\n")
        os.makedirs(os.path.join(self.tmp, 'tools'))
        with open(os.path.join(self.tmp, 'tools', 'record_apps.py'), 'w') as f:
            f.write("open('recorded.txt', 'w').write('x'); print('nothing new to record')\n")
        self.travels = mock.patch.object(self.w, 'travels_backup', return_value=(0, 'nothing new'))
        self.travels.start()

    def tearDown(self):
        self.travels.stop()

    def ran(self, folder):
        return os.path.exists(os.path.join(self.tmp, folder, 'ran.txt'))

    def go(self, when, argv=()):
        with mock.patch.object(self.w, 'datetime', fixed_now(when)), mock.patch.object(sys, 'argv', ['weekly.py', *argv]):
            return self.w.main()

    def logged(self):
        return open(self.w.LOG, encoding='utf-8').read()

    def test_monday_runs_the_daily_jobs_not_the_gallery(self):
        if hasattr(self.w, 'last_gallery_ok'):
            self.w.last_gallery_ok = lambda *a, **k: datetime(2026, 11, 22, 10, 0)   # ran yesterday
        code = self.go(MONDAY)
        self.assertFalse(self.ran('sim-world'))
        self.assertTrue(self.ran('library') and self.ran('pokedex'), 'one failing (Library) does not stop the next')
        self.assertTrue(os.path.exists(os.path.join(self.tmp, 'recorded.txt')), 'record_apps runs at the end')
        self.assertEqual(code, 1, 'the Library job failed')
        log = self.logged()
        self.assertIn('Library: FAILED (exit 3)', log)
        self.assertIn('Pokédex: done', log)
        self.assertIn('finished (failed: Library)', log)

    def test_sunday_runs_the_gallery_too(self):
        self.go(SUNDAY)
        self.assertTrue(self.ran('sim-world'))
        self.assertIn('Sim World: done', self.logged())

    def test_daily_only_on_a_sunday(self):
        self.go(SUNDAY, ['--daily-only'])
        self.assertFalse(self.ran('sim-world'))

    def test_all_on_a_monday(self):
        self.go(MONDAY, ['--all'])
        self.assertTrue(self.ran('sim-world'))

    def test_a_missing_script_is_skipped_and_logged(self):
        os.remove(os.path.join(self.tmp, 'pokedex', 'tools', 'backup.py'))
        self.go(MONDAY)
        self.assertIn('Pokédex: skipped, tools/backup.py not found', self.logged())

    def test_a_travels_failure_is_counted(self):
        self.travels.stop()
        self.travels = mock.patch.object(self.w, 'travels_backup', side_effect=RuntimeError('boom'))
        self.travels.start()
        os.remove(os.path.join(self.tmp, 'library', 'tools', 'backup.py'))
        code = self.go(MONDAY)
        self.assertEqual(code, 1)
        self.assertIn('Travels: FAILED: boom', self.logged())

    def test_nothing_waits_for_a_sign_in_window(self):
        src = open(self.w.__file__, encoding='utf-8').read()
        self.assertIn("GIT_TERMINAL_PROMPT='0'", src)
        self.assertIn('stdin=subprocess.DEVNULL', src)


class TravelsBackup(unittest.TestCase):
    def setUp(self):
        self.box = GitSandbox().__enter__()
        b = self.box
        seed, self.bare = b.repo_with_remote('travels', {'data/trips.json': '[]\n', 'site/js/data.js': 'var D=[];\n', 'site/app.js': '1\n'})
        os.makedirs(b.path('family'))
        self.cwd = b.path('family', 'travels')
        b.git(b.dir, 'clone', '-q', self.bare, self.cwd)
        self.w = load(os.path.join('tools', 'weekly.py'))
        self.w.ROOT = b.path('family')
        fence(self.w, b.dir)

    def tearDown(self):
        self.box.__exit__(None, None, None)

    def head(self):
        return self.box.git(self.cwd, 'rev-parse', 'HEAD')

    def remote_head(self):
        return self.box.git(self.bare, 'rev-parse', 'main')

    def test_new_posts_are_committed_and_pushed(self):
        self.box.write(os.path.join(self.cwd, 'data', 'trips.json'), '[{"t":"Rome"}]\n')
        self.box.write(os.path.join(self.cwd, 'site', 'photos', 'rome', '1.jpg'), 'jpg')
        code, msg = self.w.travels_backup()
        self.assertEqual(code, 0, msg)
        self.assertEqual(msg, 'saved and pushed')
        self.assertRegex(self.box.git(self.cwd, 'log', '-1', '--format=%s'), r'^Posts saved up to \d{4}-\d\d-\d\d \(daily backup\)$')
        self.assertEqual(self.remote_head(), self.head())
        self.assertEqual(sorted(self.box.git(self.cwd, 'show', '--name-only', '--format=', 'HEAD').split()),
                         ['data/trips.json', 'site/photos/rome/1.jpg'])

    def test_nothing_new_is_a_no_op(self):
        head = self.head()
        code, msg = self.w.travels_backup()
        self.assertEqual(code, 0)
        self.assertTrue(msg.startswith('nothing new'), msg)
        self.assertEqual(self.head(), head)

    def test_only_the_write_pages_files_go_in(self):
        self.box.write(os.path.join(self.cwd, 'data', 'trips.json'), '[1]\n')
        self.box.write(os.path.join(self.cwd, 'site', 'app.js'), 'half-done code\n')   # someone's work in progress
        self.box.write(os.path.join(self.cwd, 'notes.txt'), 'staged by a session\n')
        self.box.git(self.cwd, 'add', 'notes.txt')
        code, msg = self.w.travels_backup()
        self.assertEqual(code, 0, msg)
        self.assertEqual(self.box.git(self.cwd, 'show', '--name-only', '--format=', 'HEAD'), 'data/trips.json')
        status = self.box.git(self.cwd, 'status', '--porcelain')
        self.assertIn(' M site/app.js', status)
        self.assertIn('notes.txt', status)

    def test_only_other_staged_work_is_not_a_backup(self):
        self.box.write(os.path.join(self.cwd, 'notes.txt'), 'staged by a session\n')
        self.box.git(self.cwd, 'add', 'notes.txt')
        head = self.head()
        code, msg = self.w.travels_backup()
        self.assertEqual(code, 0)
        self.assertEqual(self.head(), head, 'no commit for files that are not the Write page’s')

    def test_not_on_main(self):
        self.box.git(self.cwd, 'checkout', '-q', '-b', 'trial')
        self.box.write(os.path.join(self.cwd, 'data', 'trips.json'), '[2]\n')
        code, msg = self.w.travels_backup()
        self.assertEqual(code, 1)
        self.assertIn('not on main', msg)

    def test_someone_elses_unpushed_commits_are_not_pushed(self):
        if not hasattr(self.w, 'unpushed'):
            self.skipTest('this weekly.py pushes everything (older version)')
        self.box.write(os.path.join(self.cwd, 'site', 'app.js'), 'finished by hand, not pushed yet\n')
        self.box.git(self.cwd, 'commit', '-q', '-am', 'by hand')
        before = self.remote_head()
        self.box.write(os.path.join(self.cwd, 'data', 'trips.json'), '[3]\n')
        code, msg = self.w.travels_backup()
        self.assertEqual(code, 0, msg)
        self.assertIn('not pushed', msg)
        self.assertEqual(self.remote_head(), before)

    def test_a_failed_push_is_reported(self):
        self.box.git(self.cwd, 'remote', 'set-url', 'origin', self.box.path('nowhere.git'))
        self.box.write(os.path.join(self.cwd, 'data', 'trips.json'), '[4]\n')
        code, msg = self.w.travels_backup()
        self.assertEqual(code, 1)
        self.assertIn('push failed', msg)


if __name__ == '__main__':
    unittest.main()
