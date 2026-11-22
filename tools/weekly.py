"""The family's one backup job (her asks, 22 Nov: the three separate weekly tasks all ran at once after the PC had been
off and their sign-ins popped up together; and back up her ticks and books daily, not weekly). Runs each app's own job in
turn, then records the apps' new versions in Jemma's Journals once.

    pythonw tools/weekly.py [--all]    (the Windows task "Jemma's Journals - backup", every day 09:30, catches up after)

  1. Sim World: the Gallery refresh (tools/gallery_refresh.py: new uploads and comments, rebuild, back up to GitHub),
     on Sundays only (or with --all): it asks the Gallery for every upload, once a week is plenty
  2. Library: back up to GitHub (tools/backup.py), every day
  3. Pokédex: refresh What's on, back up to GitHub (tools/backup.py), every day
  4. tools/record_apps.py: the parent records the new versions and pushes

Every push signs in through the GitHub CLI (never a window). One app failing doesn't stop the others. Log: logs/weekly.log
(each app also writes its own log as before).
"""
import os, subprocess, sys, time
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = os.path.join(os.path.dirname(sys.executable), 'python.exe')
PY = PY if os.path.exists(PY) else sys.executable
JOBS = [   # (name, folder, script and arguments, time limit in seconds, Sundays only)
    ('Sim World', 'sim-world', ['tools/gallery_refresh.py'], 1800, True),
    ('Library', 'library', ['tools/backup.py'], 900, False),
    ('Pokédex', 'pokedex', ['tools/backup.py'], 1200, False),
]
LOG = os.path.join(ROOT, 'logs', 'weekly.log')
NO_WINDOW = getattr(subprocess, 'CREATE_NO_WINDOW', 0)


def log(msg):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M} {msg}\n")


def run(cmd, cwd, limit):
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='never')   # nothing may wait for a sign-in window
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace', env=env,
                           stdin=subprocess.DEVNULL, timeout=limit, creationflags=NO_WINDOW)
        out = ' '.join((r.stdout + r.stderr).split())[-300:]
        return r.returncode, out
    except subprocess.TimeoutExpired:
        return 1, f'stopped after {limit // 60} minutes'
    except Exception as e:
        return 1, str(e)


def main():
    log('started')
    failed = []
    sunday = (datetime.now().weekday() == 6 or '--all' in sys.argv) and '--daily-only' not in sys.argv
    for name, folder, args, limit, weekly in JOBS:
        if weekly and not sunday:
            continue
        cwd = os.path.join(ROOT, folder)
        if not os.path.exists(os.path.join(cwd, args[0])):
            log(f'{name}: skipped, {args[0]} not found'); continue
        t = time.time()
        code, out = run([PY, '-X', 'utf8', *args], cwd, limit)
        log(f"{name}: {'done' if code == 0 else 'FAILED (exit ' + str(code) + ')'} in {time.time() - t:.0f}s" + (f': {out}' if code and out else ''))
        if code:
            failed.append(name)
    code, out = run([PY, '-X', 'utf8', os.path.join(ROOT, 'tools', 'record_apps.py')], ROOT, 600)
    log(f"record_apps: {'done' if code == 0 else 'FAILED'}: {out}")
    log('finished' + (f' (failed: {", ".join(failed)})' if failed else ''))
    return 1 if failed or code else 0


if __name__ == '__main__':
    sys.exit(main())
