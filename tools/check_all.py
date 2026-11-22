"""Check the whole family in one go: the home page, the family rules on every site, the family's tools, accessibility,
every site's own tests, and that git is tidy everywhere.

    python tools/check_all.py --quick    (a few minutes) home page, family suite, tool tests, accessibility report, git
    python tools/check_all.py            (about 25 minutes) the same, plus each app's own suite (Travels' is the long one)

The parts (research/tests-audit.md says what each covers):
  Home page      tests/check_page.js: home itself at 1600, 1280, 1000 and 390, its Open links on a plain host
  Family rules   tests/family/family.test.js: the shared rules on all five sites through a test copy of the family server
                 (footer, dark mode and its carry, drawer, robots, CSP, fonts, links), and the online-style build
  Tools          tests/tools/test_*.py: serve_all, record_apps, weekly, build_site, new_site, open_site
  Accessibility  tests/axe_all.js against a test copy of the family server: a report, not a failure yet
  <each app>     its own suite (not with --quick)
  git            each app on main, nothing uncommitted (logs/ and her Pokédex ticks don't count), pushed

Prints one line per part and a summary; exits 1 if anything failed. Logs in logs/check-all/. It only reads: every suite
works on throwaway copies and its own servers on spare ports (never her 8050 server, her dark-mode file or her data).
"""
import contextlib, importlib.util, io, os, shutil, socket, subprocess, sys, tempfile, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
NODE = os.path.join(ROOT, '.tools', 'node', 'node.exe')
QUICK = '--quick' in sys.argv
LOGS = os.path.join(ROOT, 'logs', 'check-all')
PARTS = [   # (name, command): the parent's own checks, run every time
    ('Family rules', [NODE, 'tests/family/family.test.js']),
    ('Tools', [PY, '-B', '-X', 'utf8', '-W', 'ignore::ResourceWarning', '-m', 'unittest', 'discover', '-s', 'tests/tools', '-t', 'tests/tools']),
]
CHECKS = [   # (name, folder, command): the home page, then each site's own suite (the apps' only without --quick)
    ('Home page', ROOT, [NODE, 'tests/check_page.js']),
    ('Library', os.path.join(ROOT, 'library'), [PY, '-B', '-X', 'utf8', 'tests/run_tests.py']),
    ('Sim World', os.path.join(ROOT, 'sim-world'), [PY, '-B', '-X', 'utf8', 'tools/run_tests.py']),
    ('Pokédex', os.path.join(ROOT, 'pokedex'), [PY, '-B', '-X', 'utf8', 'tests/run_tests.py']),
    ('Travels', os.path.join(ROOT, 'travels'), [PY, '-B', '-X', 'utf8', 'tests/run_tests.py']),
]
APP_SUITES = {'Library', 'Sim World', 'Pokédex', 'Travels'}   # the long ones, skipped by --quick
GIT_APPS = ('library', 'sim-world', 'pokedex', 'travels')


def git(cwd, *args):
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace').stdout.strip()


def log_name(name):
    return name.lower().replace(' ', '-').replace('é', 'e') + '.txt'


def run_part(name, cmd, cwd, env=None):
    """Runs one part, keeps its whole output in logs/check-all/, prints one line. (name, passed, summary)"""
    if cmd[0] == NODE and not os.path.exists(NODE):
        summary = f'skipped: no Node at {os.path.relpath(NODE, ROOT)} (put the portable Node there, then .tools/node/npm.cmd install)'
        print(f'FAIL {name:13} {summary}', flush=True)
        return name, False, summary
    t = time.time()
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)
        out, code = (r.stdout or '') + (r.stderr or ''), r.returncode
    except OSError as e:
        out, code = str(e), 1
    with open(os.path.join(LOGS, log_name(name)), 'w', encoding='utf-8') as f:
        f.write(out)
    lines = [l for l in out.strip().splitlines() if l.strip()]
    tail = next((l for l in reversed(lines) if l.startswith(('Ran ', 'OK', 'FAILED')) or 'passed' in l or 'failed' in l), lines[-1] if lines else '')
    if lines and lines[-1].startswith(('OK', 'FAILED')) and len(lines) > 1 and lines[-2].startswith('Ran '):   # unittest: "Ran 80 tests …  OK"
        tail = lines[-2].split(' in ')[0] + ', ' + lines[-1]
    summary = f'{time.time() - t:4.0f}s  {tail.strip()[:100]}'
    print(f"{'ok  ' if code == 0 else 'FAIL'} {name:13} {summary}", flush=True)
    return name, code == 0, summary


def build_once(folder):
    """The online-style build, made once for the family suite and the tool tests (tools/build_site.py's own build())."""
    spec = importlib.util.spec_from_file_location('build_site_for_checks', os.path.join(ROOT, 'tools', 'build_site.py'))
    bs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bs)
    bs.OUT = folder
    t = time.time()
    try:
        with contextlib.redirect_stdout(io.StringIO()):   # its "_site/: … files" line would break the one-line-per-part list
            bs.build()
        print(f'     {"(built the online-style copy for them)":13} {time.time() - t:.0f}s', flush=True)
        return True
    except Exception as e:
        print(f'note online-style build failed ({e}): each part builds its own', flush=True)
        return False


def free_port():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close()
    return p


def accessibility(tmp):
    """axe-core over every site (her OK, 22 Nov), through a test copy of the family server: a report, not a failure yet."""
    if not os.path.exists(NODE):
        print('note Accessibility  skipped: no Node', flush=True); return
    port = free_port()
    server = subprocess.Popen([PY, '-I', os.path.join(ROOT, 'tests', 'family', 'serve_family.py'), '--port', str(port),
                               '--mode-file', os.path.join(tmp, 'axe-mode.txt')], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        ready = server.stdout.readline().decode('utf-8', 'replace')
        if not ready.startswith('ready'):
            print(f'note Accessibility  skipped: the test family server did not start ({ready.strip()[:80]})', flush=True); return
        t = time.time()
        r = subprocess.run([NODE, 'tests/axe_all.js', '--base', f'http://localhost:{port}'], cwd=ROOT, capture_output=True, text=True,
                           encoding='utf-8', errors='replace')
        first = ((r.stdout or '').strip().splitlines() or [(r.stderr or 'no output').strip()[:100]])[0]
        print(f"note {'Accessibility':13} {time.time() - t:4.0f}s  {first}  (details in logs/check-all/axe.txt)", flush=True)
    finally:
        server.kill()


def git_checks(results):
    """Each app on main, nothing uncommitted (her Pokédex ticks and any logs/ don't count, as in record_apps), pushed."""
    for app in GIT_APPS:
        p = os.path.join(ROOT, app)
        if not os.path.isdir(p):
            print(f'note git {app:9} not there', flush=True); continue
        dirty = [l for l in git(p, 'status', '--porcelain').splitlines()
                 if l.strip() and 'data/collection/go.json' not in l and not l[3:].startswith('logs/')]
        branch = git(p, 'rev-parse', '--abbrev-ref', 'HEAD')
        ahead = git(p, 'rev-list', '--count', '@{u}..HEAD') if branch == 'main' else '?'
        recorded = (git(ROOT, 'ls-tree', 'HEAD', app).split() + ['', '', ''])[2] == git(p, 'rev-parse', 'HEAD')
        ok = not dirty and branch == 'main' and ahead == '0'
        summary = f"branch {branch}, {len(dirty)} uncommitted, {ahead} not pushed"
        results.append((f'git {app}', ok, summary))
        print(f"{'ok  ' if ok else 'FAIL'} git {app:9} {summary}", flush=True)
        if ok and not recorded:   # not a failure: record_apps does it after each backup; a note so it isn't forgotten
            print(f'note git {app:9} its new version is not recorded in Jemma’s Journals yet (python tools/record_apps.py)', flush=True)
    dirty = git(ROOT, 'status', '--porcelain')
    print(f"{'ok  ' if not dirty else 'note'} git parent    {len(dirty.splitlines())} changed paths", flush=True)


def main():
    os.makedirs(LOGS, exist_ok=True)
    results = []
    tmp = tempfile.mkdtemp(prefix='jj-check-all-')
    try:
        home = CHECKS[0]
        results.append(run_part(home[0], home[2], home[1]))
        build = os.path.join(tmp, 'build')
        env = dict(os.environ, JJ_BUILD_DIR=build) if build_once(build) else None
        for name, cmd in PARTS:
            results.append(run_part(name, cmd, ROOT, env))
        accessibility(tmp)
        for name, cwd, cmd in CHECKS[1:]:
            if QUICK and name in APP_SUITES:
                continue
            if not os.path.isdir(cwd):   # a site wired in by tools/new_site.py whose folder has gone: a note, not a crash
                print(f"note {name:13} skipped: {cwd} not found (a site from tools/new_site.py deleted by hand? its --remove takes the wiring out)", flush=True)
                continue
            results.append(run_part(name, cmd, cwd))
        if QUICK:
            print('note Apps          their own suites not run (--quick)', flush=True)
        git_checks(results)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    bad = [n for n, ok, _ in results if not ok]
    print('\nAll checks passed.' if not bad else '\nFailed: ' + ', '.join(bad) + f'  (logs in {LOGS})')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
