"""Daily backup of the sites made by tools/new_site.py: commit what has changed in each one’s own repo and push it.

    python tools/backup_new_sites.py         (meant to run from the daily backup, tools/weekly.py, before record_apps.py)

A site is skipped quietly until it has a GitHub remote (making its repo is her decision: for-jemma/new-site.md), and
skipped with a note if it isn’t on main. Pushes sign in through the GitHub CLI, never a window. Prints one line per site;
exit 1 if any failed. tools/new_site.py adds each new site to SITES (and --remove takes it out).
"""
import os, subprocess, sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GH = 'C:/Program Files/GitHub CLI/gh.exe'
NO_WINDOW = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
SITES = [   # (name, folder): one line per site, added by tools/new_site.py
]


def git(cwd, *args, push=False):
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='never')   # nothing may wait for a sign-in window
    if push and os.path.exists(GH):
        env.update(GIT_CONFIG_COUNT='2', GIT_CONFIG_KEY_0='credential.helper', GIT_CONFIG_VALUE_0='',
                   GIT_CONFIG_KEY_1='credential.helper', GIT_CONFIG_VALUE_1=f"!'{GH}' auth git-credential")
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace',
                          env=env, stdin=subprocess.DEVNULL, timeout=600, creationflags=NO_WINDOW)


def backup(folder):
    """(ok, what happened); ok is None when skipped."""
    cwd = os.path.join(ROOT, folder)
    if not os.path.exists(os.path.join(cwd, '.git')):
        return None, 'not found'
    if not git(cwd, 'remote').stdout.strip():
        return None, 'no GitHub repo yet'
    if git(cwd, 'rev-parse', '--abbrev-ref', 'HEAD').stdout.strip() != 'main':
        return False, 'not on main, nothing saved'
    git(cwd, 'add', '-A')
    if git(cwd, 'diff', '--cached', '--name-only').stdout.strip():
        r = git(cwd, 'commit', '-q', '-m', f'Daily backup {datetime.now():%Y-%m-%d}')
        if r.returncode:
            return False, 'commit failed: ' + (r.stderr or r.stdout).strip()[-200:]
        saved = 'saved and pushed'
    else:
        saved = 'nothing new'
    r = git(cwd, 'push', '-q', 'origin', 'main', push=True)   # also sends anything committed by hand
    return (True, saved) if r.returncode == 0 else (False, 'push failed: ' + r.stderr.strip()[-200:])


def main():
    failed = False
    for name, folder in SITES:
        try:
            ok, what = backup(folder)
        except Exception as e:
            ok, what = False, str(e)
        print(f"{name}: {'skipped' if ok is None else 'done' if ok else 'FAILED'}: {what}")
        failed |= ok is False
    if not SITES:
        print('no new sites to back up')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
