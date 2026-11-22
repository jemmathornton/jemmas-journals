"""Start a new site in Jemma’s family of websites, from the family template (templates/new-site).

    python tools/new_site.py recipes "Recipes"               a new folder JemmasJournals/recipes, “Jemma’s Recipes”
    python tools/new_site.py recipes "Recipes" "#8A3B2E"      … with its own accent colour (default a quiet blue)
    python tools/new_site.py recipes "Recipes" --dry-run      shows everything it would do, changes nothing
    python tools/new_site.py recipes "Recipes" --add-to-home  also puts a placeholder place on the home page (PLACES in site/home.js)
    python tools/new_site.py recipes --remove                 undoes the wiring for a site made by mistake (never deletes the folder)

What it does:
1. copies templates/new-site to the new folder and fills in the name, folder and colours (the accent is checked against the
   backgrounds, 4.5:1 or more in light and dark, and darkened or lightened if it needs to be);
2. `git init` there (branch main, her name and email from this repo) with a first commit. No GitHub repo: that is her
   decision, so it prints the commands for making one and adding the site to Jemma’s Journals as a submodule;
3. wires it into the family: tools/serve_all.py (APPS: http://localhost:8050/<folder>/), tools/open_site.pyw (SITES),
   tools/build_site.py (APPS) and tools/check_all.py (its tests). Each edit is checked first and is safe to run twice.
The home page only changes with --add-to-home (a new place on home is her yes, and tests/check_page.js expects four places);
otherwise it prints the line to add.
"""
import argparse, colorsys, datetime, difflib, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_NAME = os.path.join('templates', 'new-site')
DEFAULT_ACCENT = '#3D6A8A'
MARK = 'added by tools/new_site.py'
TAKEN = {'site', 'family', 'tools', 'tests', 'templates', 'research', 'for-jemma', 'logs', 'node_modules', '_site', 'api',
         'library', 'sim-world', 'pokedex', 'travels', 'img', 'fonts', 'home'}
TEXT = ('.html', '.css', '.js', '.md', '.svg', '.gitignore', '.json')
# the backgrounds in templates/new-site/site/site.css that the accent sits on (the darkest light one, the lightest dark one)
LIGHT_BGS = ('#F1F0EB', '#FAFAF7', '#FFFFFF')
DARK_BGS = ('#24262A', '#202226', '#1B1C1F')
BAR_LIGHT, BAR_DARK = '#F1F0EB', '#202226'


# ---------- colours ----------
def rgb(h):
    h = h.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if not re.fullmatch(r'[0-9a-fA-F]{6}', h):
        raise ValueError(f'“{h}” is not a colour like #3D6A8A')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def hexs(c):
    return '#' + ''.join(f'{round(max(0, min(1, v)) * 255):02X}' for v in c)


def lum(c):
    f = lambda v: v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def mix(c, other, t):
    return tuple(x + (y - x) * t for x, y in zip(c, other))


def accents(accent):
    """(light accent, dark-mode accent, notes): both at least 4.6:1 on every background they sit on."""
    base, notes = rgb(accent), []
    light = base
    for i in range(41):
        if min(contrast(light, rgb(b)) for b in LIGHT_BGS) >= 4.6:
            break
        light = mix(base, (0, 0, 0), i / 40)
    if hexs(light) != hexs(base):
        notes.append(f'the accent {hexs(base)} was too pale on the light background, so light mode uses {hexs(light)}')
    h, l, s = colorsys.rgb_to_hls(*base)   # dark mode: the same hue, lighter, a little softer
    start = colorsys.hls_to_rgb(h, max(l, 0.62), min(s, 0.55))
    dark = start
    for i in range(41):
        if min(contrast(dark, rgb(b)) for b in DARK_BGS) >= 5:
            break
        dark = mix(start, (1, 1, 1), i / 40)
    return hexs(light), hexs(dark), notes


# ---------- the wiring: each edit is (add, remove), both return the new text (unchanged if already done / not there) ----------
def block(text, start, end):
    """(i, j) of the inside of `start … end` (end is the first line that is exactly `end`)."""
    i = text.find(start)
    if i < 0:
        raise ValueError(f'could not find “{start.strip()}”')
    i += len(start)
    m = re.compile('^' + re.escape(end) + '$', re.M).search(text, i)
    if not m:
        raise ValueError(f'could not find the end of “{start.strip()}”')
    return i, m.start()


def add_line(text, start, end, key_re, line):
    i, j = block(text, start, end)
    if re.search(key_re, text[i:j], re.M):
        return text
    return text[:j] + line + '\n' + text[j:]


def remove_line(text, start, end, key_re):
    try:
        i, j = block(text, start, end)
    except ValueError:
        return text
    inside = re.sub(key_re + r'.*\n', '', text[i:j], flags=re.M)
    return text[:i] + inside + text[j:]


def wiring(folder, name, accent):
    ascii_name = re.sub(r'[^A-Za-z0-9 ]', '', name.encode('ascii', 'ignore').decode()).strip() or folder
    key = rf"^\s*'{re.escape(folder)}':"
    edits = {
        'tools/serve_all.py': (
            lambda t: add_line(t, 'APPS = {', '}', key, f"    '{folder}': ('{folder}/site', None, None),   # {MARK}"),
            lambda t: remove_line(t, 'APPS = {', '}', key)),
        'tools/open_site.pyw': (
            lambda t: add_line(t, 'SITES = {', '}', key, f"    '{folder}': ('/{folder}/', os.path.join(LOCAL, 'Jemmas {ascii_name}', 'Chrome')),   # {MARK}"),
            lambda t: remove_line(t, 'SITES = {', '}', key)),
        'tools/check_all.py': (
            lambda t: add_line(t, 'CHECKS = [', ']', rf"^\s*\('[^']*', os\.path\.join\(ROOT, '{re.escape(folder)}'\)",
                               f"    ('{name}', os.path.join(ROOT, '{folder}'), [NODE, 'tests/check_site.js']),   # {MARK}"),
            lambda t: remove_line(t, 'CHECKS = [', ']', rf"^\s*\('[^']*', os\.path\.join\(ROOT, '{re.escape(folder)}'\)")),
        'tools/build_site.py': (lambda t: build_add(t, folder), lambda t: build_remove(t, folder)),
    }
    return edits


def build_add(t, folder):
    m = re.search(r'^APPS = \{(.*)\}$', t, re.M)
    if not m:
        raise ValueError('could not find “APPS = {…}” on one line')
    if f"'{folder}':" in m.group(1):
        return t
    return t[:m.end(1)] + f", '{folder}': '{folder}/site'" + t[m.end(1):]


def build_remove(t, folder):
    return re.sub(rf",\s*'{re.escape(folder)}': '[^']*'(?=[^\n]*\}}$)", '', t, count=1, flags=re.M)


def home_line(folder, name, accent):
    return (f'    {{name:"{name}", url:"/{folder}/", title:"My {name}", pc:"{accent}", pic:null,\n'
            f'     about:null}}   // {MARK}: the picture and the line are placeholders until she chooses')


def home_add(t, folder, name, accent):
    i, j = block(t, '  var PLACES=[\n', '  ];')
    inside = t[i:j]
    if f'url:"/{folder}/"' in inside:
        return t
    lines = inside.rstrip('\n').split('\n')
    last = lines[-1]
    code = last.split('//', 1)[0]
    k = code.rstrip().rfind('}')
    if k < 0:
        raise ValueError('could not find the last place in PLACES')
    if not code.rstrip().endswith(','):
        last = last[:k + 1] + ',' + last[k + 1:]
    lines[-1] = last
    return t[:i] + '\n'.join(lines) + '\n' + home_line(folder, name, accent) + '\n' + t[j:]


def home_remove(t, folder):
    try:
        i, j = block(t, '  var PLACES=[\n', '  ];')
    except ValueError:
        return t
    inside = t[i:j]
    new = re.sub(r'^    \{name:"[^"]*", url:"/' + re.escape(folder) + r'/".*\n.*' + re.escape(MARK) + r'.*\n', '', inside, flags=re.M)
    if new == inside:
        return t
    lines = new.rstrip('\n').split('\n')
    last = lines[-1]
    cut = last.find('//')
    code, rest = (last, '') if cut < 0 else (last[:cut], last[cut:])
    s = code.rstrip()
    if s.endswith('},'):   # take back the comma it added after the place before
        lines[-1] = s[:-1] + code[len(s):] + rest
    return t[:i] + '\n'.join(lines) + '\n' + t[j:]


# ---------- helpers ----------
def read(p):
    with open(p, encoding='utf-8', newline='') as f:
        return f.read()


def write(p, text):
    with open(p + '.tmp', 'w', encoding='utf-8', newline='') as f:
        f.write(text)
    os.replace(p + '.tmp', p)


def show_diff(path, old, new):
    for line in difflib.unified_diff(old.splitlines(), new.splitlines(), path, path, n=0, lineterm=''):
        print('    ' + line)


def git(cwd, *args):
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')


def apply(root, changes, dry):
    """changes: {path: function(text) -> text}. Works out every edit first; writes only if all of them worked."""
    planned = []
    for rel, f in changes.items():
        p = os.path.join(root, rel)
        if not os.path.exists(p):
            print(f'  skip {rel}: not found')
            continue
        old = read(p)
        new = f(old)
        planned.append((rel, p, old, new))
    for rel, p, old, new in planned:
        if new == old:
            print(f'  {rel}: nothing to change')
            continue
        print(f'  {rel}:' + (' (would change)' if dry else ''))
        show_diff(rel, old, new)
        if not dry:
            write(p, new)


def main():
    ap = argparse.ArgumentParser(description='Start a new site in Jemma’s family from templates/new-site.')
    ap.add_argument('folder', help='the folder and address, lower case with hyphens, e.g. recipes')
    ap.add_argument('name', nargs='?', help='the name after “Jemma’s”, e.g. Recipes')
    ap.add_argument('accent', nargs='?', default=DEFAULT_ACCENT, help=f'the accent colour, e.g. #8A3B2E (default {DEFAULT_ACCENT})')
    ap.add_argument('--dry-run', action='store_true', help='show what would happen, change nothing')
    ap.add_argument('--remove', action='store_true', help='undo the wiring for this folder (the folder itself is kept)')
    ap.add_argument('--add-to-home', action='store_true', help='also add a placeholder place to the home page (site/home.js)')
    ap.add_argument('--parent', default=ROOT, help=argparse.SUPPRESS)   # for testing on a copy of Jemma’s Journals
    a = ap.parse_args()
    root = os.path.abspath(a.parent)
    folder = a.folder.strip().strip('/\\')
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,40}', folder) or folder in TAKEN:
        sys.exit(f'“{folder}” can’t be used: use lower case letters, numbers and hyphens, not one of {", ".join(sorted(TAKEN))}')
    dest = os.path.join(root, folder)

    if a.remove:
        print(f'Taking {folder} out of the family wiring' + (' (dry run: nothing changed)' if a.dry_run else '') + ':')
        changes = {rel: rem for rel, (_, rem) in wiring(folder, folder, DEFAULT_ACCENT).items()}
        changes['site/home.js'] = lambda t: home_remove(t, folder)
        apply(root, changes, a.dry_run)
        if os.path.exists(dest):
            print(f'\nThe folder itself is kept: {dest}\nTo delete it too (it can’t be undone; check nothing in it is wanted first):\n'
                  f'    Remove-Item -Recurse -Force "{dest}"')
            if os.path.exists(os.path.join(root, '.gitmodules')) and f'path = {folder}' in read(os.path.join(root, '.gitmodules')):
                print(f'It is a submodule of Jemma’s Journals: first  git rm {folder}  in {root}')
        print('Restart the family server (tools/serve_all.py) so it stops serving it.')
        return 0

    if not a.name:
        sys.exit('Give the name too, e.g.  python tools/new_site.py recipes "Recipes"')
    name = a.name.strip().replace("'", '’')
    if not name or re.search(r'[<>"&\\`$]', name) or len(name) > 40:
        sys.exit('The name can’t be empty, longer than 40 letters or contain < > " & \\ ` $')
    try:
        light, dark, notes = accents(a.accent)
    except ValueError as e:
        sys.exit(str(e))
    template = os.path.join(root, TEMPLATE_NAME)
    if not os.path.isdir(template):
        sys.exit(f'The template is missing: {template}')
    if os.path.exists(dest):
        print(f'{dest} already exists: not copied over (only the wiring is checked).')
    today = datetime.date.today()
    fill = {'__NAME__': name, '__FOLDER__': folder, '__ACCENT__': light, '__ACCENT_DARK__': dark,
            '__BAR_LIGHT__': BAR_LIGHT, '__BAR_DARK__': BAR_DARK, '__DATE__': f'{today.day} {today:%b %Y}'}
    print(f'Jemma’s {name}: folder {dest}, address /{folder}/, accent {light} (dark mode {dark})' + (' — dry run, nothing changed' if a.dry_run else ''))
    for n in notes:
        print('  note: ' + n)

    # 1–2. the files and their own git
    if not os.path.exists(dest):
        if a.dry_run:
            print(f'  would copy {TEMPLATE_NAME} to {folder}/ and fill in the names and colours, then git init with a first commit')
        else:
            shutil.copytree(template, dest, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            left = []
            for d, _, files in os.walk(dest):
                for f in files:
                    p = os.path.join(d, f)
                    if not f.endswith(TEXT):
                        continue
                    t = read(p)
                    for k, v in fill.items():
                        t = t.replace(k, v)
                    write(p, t)
                    left += [os.path.relpath(p, dest) + ': ' + m for m in set(re.findall(r'__[A-Z_]+__', t))]
            if left:
                print('  warning, not filled in: ' + '; '.join(left))
            r = git(dest, 'init', '-q', '-b', 'main')
            for k in ('user.name', 'user.email'):
                v = git(root, 'config', '--get', k).stdout.strip()
                if v:
                    git(dest, 'config', k, v)
            git(dest, 'add', '-A')
            r = git(dest, 'commit', '-q', '-m', f'Start Jemma’s {name} from the family template (tools/new_site.py in Jemma’s Journals)')
            print(f'  made {folder}/ from the template' + (', with its own git and a first commit' if r.returncode == 0 else f' (git commit failed: {r.stderr.strip()})'))

    # 3. the wiring
    print('Wiring it into the family:')
    changes = {rel: add for rel, (add, _) in wiring(folder, name, light).items()}
    if a.add_to_home:
        changes['site/home.js'] = lambda t: home_add(t, folder, name, light)
    try:
        apply(root, changes, a.dry_run)
    except ValueError as e:
        sys.exit(f'  stopped, nothing written: {e}')
    if not a.add_to_home:
        print('\nThe home page is unchanged (a new place on home is her yes). To add it, run again with --add-to-home, or add this to\n'
              'PLACES in site/home.js (with a comma after the place before it):\n' + home_line(folder, name, light))
    else:
        print('  note: tests/check_page.js expects four places on home: update its “four places” checks.')

    owner = 'jemmathornton'
    m = re.search(r'github\.com[:/]([^/]+)/', git(root, 'remote', 'get-url', 'origin').stdout)
    if m:
        owner = m.group(1)
    print(f'''
Next:
  - restart the family server (tools/serve_all.py), then open http://localhost:8050/{folder}/
  - its checks:  cd "{dest}"  then  ..\\.tools\\node\\node.exe tests\\check_site.js
  - make it hers: the words in site/js/data.js, the look in site/site.css (tokens at the top), its CLAUDE.md

Only with her OK (a GitHub repo is her decision; public repos can be read by anyone):
  cd "{dest}"
  & "C:\\Program Files\\GitHub CLI\\gh.exe" repo create {owner}/{folder} --public --source . --push      (or --private)
  cd "{root}"
  git submodule add https://github.com/{owner}/{folder}.git {folder}
  git commit -m "Add Jemma’s {name} as a submodule"
  git -c "credential.helper=!'C:/Program Files/GitHub CLI/gh.exe' auth git-credential" push
Then add '{folder}' to APPS in tools/record_apps.py and to the git list in tools/check_all.py (the apps it checks are submodules).''')
    return 0


if __name__ == '__main__':
    sys.exit(main())
