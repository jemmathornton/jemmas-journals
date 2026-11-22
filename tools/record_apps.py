"""Record each app's current version in Jemma's Journals (the parent) and push it.

    python tools/record_apps.py            (each app's weekly backup runs this at the end; safe to run any time)

After an app commits (by hand or by its weekly backup), the parent still points at the app's older version until this
"second commit" is made (her layout, 21 Nov: Jemma's Journals is the parent, the apps are submodules). It only records
apps that are on their main branch with nothing uncommitted, never touches anything else in the parent, and never
prompts. A failure is printed and the exit code is 1, so a backup's log shows it.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = ['library', 'sim-world', 'pokedex', 'travels']
GH = 'C:/Program Files/GitHub CLI/gh.exe'   # forward slashes: git runs the helper through sh


def git(*args, cwd=ROOT):
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')


def main():
    if git('rev-parse', '--abbrev-ref', 'HEAD').stdout.strip() != 'main':
        print('Jemma’s Journals is not on main: nothing recorded'); return 1
    # every network call uses the GitHub CLI's sign-in, never Windows' credential window (her note, 22 Nov: popups)
    helper = f"credential.helper=!'{GH}' auth git-credential" if os.path.exists(GH) else 'credential.helper='
    changed, skipped = [], []
    for app in APPS:
        path = os.path.join(ROOT, app)
        if not os.path.exists(os.path.join(path, '.git')):
            continue
        dirty = [l for l in git('status', '--porcelain', cwd=path).stdout.splitlines() if l.strip() and not l[3:].startswith('logs/') and not re.search(r'data/collection/(go|home)\.json', l)]   # a backup's own log line and her Pokédex ticks (GO's and, since 22 Nov, Pokémon HOME's; saved by the daily backup) don't count
        if dirty:
            print(f'{app}: has uncommitted changes, not recorded'); skipped.append(app); continue
        if git('rev-parse', '--abbrev-ref', 'HEAD', cwd=path).stdout.strip() != 'main':
            print(f'{app}: not on main, not recorded'); skipped.append(app); continue
        git('-c', 'credential.helper=', '-c', helper, 'fetch', '-q', cwd=path)
        if git('rev-list', '--count', '@{u}..HEAD', cwd=path).stdout.strip() not in ('0', ''):
            print(f'{app}: has commits not yet pushed, not recorded'); skipped.append(app); continue
        recorded = git('ls-tree', 'HEAD', app).stdout.split()
        current = git('rev-parse', 'HEAD', cwd=path).stdout.strip()
        if len(recorded) >= 3 and recorded[2] == current:
            continue
        changed.append(app)
    if not changed:
        print('nothing new to record' + (f' (skipped: {", ".join(skipped)})' if skipped else ': every app already recorded')); return 0
    r = git('add', '--', *changed)
    if r.returncode == 0:
        r = git('commit', '-m', 'Record app versions: ' + ', '.join(changed), '--', *changed)
    if r.returncode != 0:
        print('could not commit:', r.stderr.strip() or r.stdout.strip()); return 1
    r = git('-c', 'credential.helper=', '-c', helper, 'push', '-q')
    if r.returncode != 0:
        print('recorded, but the push failed:', r.stderr.strip()); return 1
    print('recorded and pushed:', ', '.join(changed)); return 0


if __name__ == '__main__':
    sys.exit(main())
