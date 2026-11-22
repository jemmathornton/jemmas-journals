"""Check the whole family in one go: every site's own tests, the home page checks, and that git is tidy everywhere.

    python tools/check_all.py            (about 20 minutes: Travels' tests are the long ones)
    python tools/check_all.py --quick    (skips the Travels end-to-end half)

Prints one line per check and a summary; exits 1 if anything failed. It only reads: each suite runs on its own throwaway
copy, as each app's notes describe (the Pokédex and Library suites never touch her ticks or books).
"""
import os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
NODE = os.path.join(ROOT, '.tools', 'node', 'node.exe')
QUICK = '--quick' in sys.argv
CHECKS = [   # (name, folder, command)
    ('Home page', ROOT, [NODE, 'tests/check_page.js']),
    ('Library', os.path.join(ROOT, 'library'), [PY, '-B', '-X', 'utf8', 'tests/run_tests.py']),
    ('Sim World', os.path.join(ROOT, 'sim-world'), [PY, '-B', '-X', 'utf8', 'tools/run_tests.py']),
    ('Pokédex', os.path.join(ROOT, 'pokedex'), [PY, '-B', '-X', 'utf8', 'tests/run_tests.py']),
    ('Travels', os.path.join(ROOT, 'travels'), [PY, '-B', '-X', 'utf8', 'tests/run_tests.py'] + (['unit'] if QUICK else [])),
]


def git(cwd, *args):
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace').stdout.strip()


def main():
    results, logs = [], os.path.join(ROOT, 'logs', 'check-all')
    os.makedirs(logs, exist_ok=True)
    for name, cwd, cmd in CHECKS:
        t = time.time()
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        out = (r.stdout or '') + (r.stderr or '')
        log = os.path.join(logs, name.lower().replace(' ', '-').replace('é', 'e') + '.txt')
        open(log, 'w', encoding='utf-8').write(out)
        tail = [l for l in out.strip().splitlines() if l.strip()][-1:] or ['']
        results.append((name, r.returncode == 0, f'{time.time() - t:.0f}s  {tail[0][:90]}'))
        print(f"{'ok  ' if r.returncode == 0 else 'FAIL'} {name:10} {results[-1][2]}", flush=True)
    # git: each app on main, nothing uncommitted except her own data, pushed, and recorded in the parent
    for app in ('library', 'sim-world', 'pokedex', 'travels'):
        p = os.path.join(ROOT, app)
        dirty = [l for l in git(p, 'status', '--porcelain').splitlines() if 'data/collection/go.json' not in l]
        branch = git(p, 'rev-parse', '--abbrev-ref', 'HEAD')
        ahead = git(p, 'rev-list', '--count', '@{u}..HEAD') if branch == 'main' else '?'
        recorded = (git(ROOT, 'ls-tree', 'HEAD', app).split() + ['', '', ''])[2] == git(p, 'rev-parse', 'HEAD')
        ok = not dirty and branch == 'main' and ahead == '0'
        results.append((f'git {app}', ok, f"branch {branch}, {len(dirty)} uncommitted, {ahead} not pushed, {'recorded' if recorded else 'NOT recorded in parent'}"))
        print(f"{'ok  ' if ok else 'FAIL'} git {app:9} {results[-1][2]}", flush=True)
    dirty = git(ROOT, 'status', '--porcelain')
    print(f"{'ok  ' if not dirty else 'note'} git parent  {len(dirty.splitlines())} changed paths", flush=True)
    bad = [n for n, ok, _ in results if not ok]
    print('\nAll checks passed.' if not bad else '\nFailed: ' + ', '.join(bad) + f'  (logs in {logs})')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
