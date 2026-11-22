"""Record each app's current version in Jemma's Journals (the parent) and push it.

    python tools/record_apps.py            (each app's weekly backup runs this at the end; safe to run any time)

After an app commits (by hand or by its weekly backup), the parent still points at the app's older version until this
"second commit" is made (her layout, 21 Nov: Jemma's Journals is the parent, the apps are submodules). It only records
apps that are on their main branch with nothing uncommitted, never touches anything else in the parent, and never
prompts. A failure is printed and the exit code is 1, so a backup's log shows it.
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = ['library', 'sim-world', 'pokedex', 'travels']
GH = r'C:\Program Files\GitHub CLI\gh.exe'


def git(*args, cwd=ROOT):
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')


def main():
    changed = []
    for app in APPS:
        path = os.path.join(ROOT, app)
        if not os.path.exists(os.path.join(path, '.git')):
            continue
        if git('status', '--porcelain', cwd=path).stdout.strip():
            print(f'{app}: has uncommitted changes, not recorded'); continue
        if git('rev-parse', '--abbrev-ref', 'HEAD', cwd=path).stdout.strip() != 'main':
            print(f'{app}: not on main, not recorded'); continue
        recorded = git('ls-tree', 'HEAD', app).stdout.split()
        current = git('rev-parse', 'HEAD', cwd=path).stdout.strip()
        if len(recorded) >= 3 and recorded[2] == current:
            continue
        changed.append(app)
    if not changed:
        print('every app already recorded'); return 0
    r = git('add', '--', *changed)
    if r.returncode == 0:
        r = git('commit', '-m', 'Record app versions: ' + ', '.join(changed), '--', *changed)
    if r.returncode != 0:
        print('could not commit:', r.stderr.strip() or r.stdout.strip()); return 1
    helper = f"credential.helper=!'{GH}' auth git-credential" if os.path.exists(GH) else 'credential.helper='
    r = git('-c', helper, 'push', '-q')
    if r.returncode != 0:
        print('recorded, but the push failed:', r.stderr.strip()); return 1
    print('recorded and pushed:', ', '.join(changed)); return 0


if __name__ == '__main__':
    sys.exit(main())
