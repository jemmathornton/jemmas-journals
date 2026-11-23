"""The family's one backup job (her asks, 22 Nov: the three separate weekly tasks all ran at once after the PC had been
off and their sign-ins popped up together; and back up her ticks and books daily, not weekly). Runs each app's own job in
turn, then records the apps' new versions in Jemma's Journals once.

    pythonw tools/weekly.py [--all]    (the Windows task "Jemma's Journals - backup", every day 09:30, catches up after)

  1. Sim World: the Gallery refresh (tools/gallery_refresh.py: new uploads and comments, rebuild, back up to GitHub),
     on Sundays, or any day when its last successful run (read from sim-world/logs/gallery-refresh.log) is more than
     6 days ago, so a Sunday with the PC off catches up the next day; --all forces it, --daily-only skips it
  2. Library: back up to GitHub (tools/backup.py), every day
  3. Pokédex: refresh What's on, back up to GitHub (tools/backup.py), every day
  4. New sites (tools/backup_new_sites.py): each site made from the template with its own GitHub repo, every day
  5. Travels: any posts saved on the Write page (data/, site/photos/, the rebuilt site/js/data.js, the restamped
     site/index.html) are committed (those paths only) and pushed, every day; not pushed if main already had other
     unpushed commits (logged instead) (her pick, 22 Nov: Travels in the daily backup)
  6. tools/record_apps.py: the parent records the new versions and pushes

Every push signs in through the GitHub CLI (never a window). One app failing doesn't stop the others. Log: logs/weekly.log
(each app also writes its own log as before).
"""
import os, re, subprocess, sys, time
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = os.path.join(os.path.dirname(sys.executable), 'python.exe')
PY = PY if os.path.exists(PY) else sys.executable
JOBS = [   # (name, folder, script and arguments, time limit in seconds, weekly: Sundays or when overdue)
    ('Sim World', 'sim-world', ['tools/gallery_refresh.py'], 1800, True),
    ('Library', 'library', ['tools/backup.py'], 900, False),
    ('Pokédex', 'pokedex', ['tools/backup.py'], 1200, False),
    ('New sites', '.', ['tools/backup_new_sites.py'], 900, False),   # any site made by tools/new_site.py with its own GitHub repo
]
LOG = os.path.join(ROOT, 'logs', 'weekly.log')
GALLERY_LOG = os.path.join(ROOT, 'sim-world', 'logs', 'gallery-refresh.log')
WEEKLY_GAP = 6   # days: a weekly job also runs when its last good run is older than this
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


GH = 'C:/Program Files/GitHub CLI/gh.exe'
TRAVELS_PATHS = ['data', 'site/photos', 'site/js/data.js', 'site/index.html']   # index.html: every save restamps it


def git(cwd, *args, push=False):
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='never')
    if push and os.path.exists(GH):   # sign in through the GitHub CLI, never a window
        env.update(GIT_CONFIG_COUNT='2', GIT_CONFIG_KEY_0='credential.helper', GIT_CONFIG_VALUE_0='',
                   GIT_CONFIG_KEY_1='credential.helper', GIT_CONFIG_VALUE_1=f"!'{GH}' auth git-credential")
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace',
                          env=env, stdin=subprocess.DEVNULL, timeout=600, creationflags=NO_WINDOW)


def last_gallery_ok(path=GALLERY_LOG):
    """When the Sim World Gallery refresh last finished well, from its own log, or None.
    Each run starts with "Gallery refresh, 22 Nov 2026 11:28[, started]"; a good run ends with a line "Finished"
    ("Finished with problems" is not good). Older runs, from before "Finished" was written, count if they reached
    "Saved in the project history"."""
    try:
        with open(path, encoding='utf-8', errors='replace') as f:
            lines = f.read().splitlines()
    except OSError:
        return None
    last, when, good = None, None, False
    for line in lines + ['Gallery refresh, end']:
        m = re.match(r'Gallery refresh, (\d{1,2} \w{3} \d{4} \d{2}:\d{2})', line)
        if m or line == 'Gallery refresh, end':
            if when and good and (last is None or when > last):
                last = when
            when, good = None, False
            if m:
                try:
                    when = datetime.strptime(m.group(1), '%d %b %Y %H:%M')
                except ValueError:
                    when = None
        elif line.strip() == 'Finished' or line.startswith('Saved in the project history'):
            good = True
        elif line.startswith('Finished with problems') or line.startswith('Stopped with an error'):
            good = False
    return last


def weekly_due(now=None, last=None, argv=None):
    """(run it?, why) for the weekly job: Sundays, or when the last good run is more than WEEKLY_GAP days ago."""
    now, argv = now or datetime.now(), sys.argv if argv is None else argv
    if '--daily-only' in argv:
        return False, 'skipped (--daily-only)'
    if '--all' in argv:
        return True, 'run (--all)'
    if now.weekday() == 6:
        return True, 'run (Sunday)'
    if last is None:
        return True, 'run (no good run found in its log)'
    days = (now.date() - last.date()).days   # calendar days, so a late Sunday run never makes Saturday due too
    if days > WEEKLY_GAP:
        return True, f'run (catching up: last good run {last:%a %d %b %H:%M}, {days} days ago)'
    return False, f'not due (last good run {last:%a %d %b %H:%M})'


def unpushed(cwd):
    """How many commits on main GitHub doesn't have yet (as far as this copy last heard), or None if unknown."""
    r = git(cwd, 'rev-list', '--count', 'origin/main..HEAD')
    return int(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip().isdigit() else None


def travels_backup():
    """Commit and push the posts saved since last time (only the Write page's own files), if any.
    Only its own commit is pushed: if main already had commits GitHub doesn't have (someone's work, perhaps half done),
    it commits but doesn't push, and says so in the log (round 5 Travels review)."""
    cwd = os.path.join(ROOT, 'travels')
    if git(cwd, 'rev-parse', '--abbrev-ref', 'HEAD').stdout.strip() != 'main':
        return 1, 'not on main, nothing saved'
    paths = [p for p in TRAVELS_PATHS if os.path.exists(os.path.join(cwd, p))]
    if not paths:
        return 0, 'nothing to save (no Write-page files)'
    before = unpushed(cwd)
    git(cwd, 'add', '--', *paths)
    if not git(cwd, 'diff', '--cached', '--name-only', '--', *paths).stdout.strip():   # only its own paths count
        note = f'; note: {before} commit(s) on main not on GitHub yet, not pushed (left for her to push by hand)' if before else ''
        return 0, 'nothing new' + note
    # "-- paths": only the Write page's files go in, never anything else a session had staged
    r = git(cwd, 'commit', '-q', '-m', f'Posts saved up to {datetime.now():%Y-%m-%d} (daily backup)', '--', *paths)
    if r.returncode:
        return 1, 'commit failed: ' + (r.stderr or r.stdout).strip()[-200:]
    if before != 0:
        why = f'{before} earlier commit(s) on main not on GitHub' if before else 'could not tell what GitHub has'
        return 0, f'saved, not pushed: {why} (not made by the backup), so nothing was pushed; push by hand when they are ready'
    r = git(cwd, 'push', '-q', 'origin', 'main', push=True)
    return (0, 'saved and pushed') if r.returncode == 0 else (1, 'saved, but the push failed: ' + r.stderr.strip()[-200:])


def main():
    log('started')
    failed = []
    for name, folder, args, limit, weekly in JOBS:
        if weekly:
            due, why = weekly_due(last=last_gallery_ok())
            log(f'{name}: {why}')
            if not due:
                continue
        cwd = os.path.join(ROOT, folder)
        if not os.path.exists(os.path.join(cwd, args[0])):
            log(f'{name}: skipped, {args[0]} not found'); continue
        t = time.time()
        code, out = run([PY, '-X', 'utf8', *args], cwd, limit)
        log(f"{name}: {'done' if code == 0 else 'FAILED (exit ' + str(code) + ')'} in {time.time() - t:.0f}s" + (f': {out}' if code and out else ''))
        if code:
            failed.append(name)
    try:
        tcode, tout = travels_backup()
    except Exception as e:
        tcode, tout = 1, str(e)
    log(f"Travels: {'done' if tcode == 0 else 'FAILED'}: {tout}")
    if tcode:
        failed.append('Travels')
    code, out = run([PY, '-X', 'utf8', os.path.join(ROOT, 'tools', 'record_apps.py')], ROOT, 600)
    log(f"record_apps: {'done' if code == 0 else 'FAILED'}: {out}")
    log('finished' + (f' (failed: {", ".join(failed)})' if failed else ''))
    return 1 if failed or code else 0


if __name__ == '__main__':
    sys.exit(main())
