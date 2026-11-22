"""Start a new site in Jemma’s family of websites, from the family template (templates/new-site).

    python tools/new_site.py recipes "Recipes"               a new folder JemmasJournals/recipes, “Jemma’s Recipes”
    python tools/new_site.py recipes "Recipes" "#8A3B2E"      … with its own accent colour (default a quiet blue)
    python tools/new_site.py recipes "Recipes" --dry-run      shows everything it would do, changes nothing
    python tools/new_site.py recipes --add-to-home            (later) also put it on the home page: a placeholder place in
                                                              site/home.js, in the site’s own colour
    python tools/new_site.py recipes --shortcut               (later) also a Desktop/Start shortcut, made by tools/setup_pc.ps1
    python tools/new_site.py recipes --unignore               before `git submodule add`: takes it out of the parent’s .gitignore
    python tools/new_site.py recipes --remove                 undoes the wiring for a site made by mistake (never deletes the folder)

What it does:
1. works out every change first; if any of them can’t be made, it stops before anything is written or copied;
2. copies templates/new-site to the new folder and fills in the name, folder and colours (the accent is checked against the
   backgrounds, 4.5:1 or more in light and dark, and darkened or lightened if it needs to be);
3. `git init` there (branch main, her name and email from this repo) with a first commit. No GitHub repo: that is her
   decision, so it prints the commands for making one and adding the site to Jemma’s Journals as a submodule;
4. wires it into the family: tools/serve_all.py (http://localhost:8050/<folder>/), tools/open_site.pyw, tools/build_site.py,
   tools/check_all.py (its tests), tests/axe_all.js (accessibility), tools/backup_new_sites.py (a daily commit and push of its own
   repo, once it has a GitHub remote), and the parent’s .gitignore (it is its own repo until it becomes a submodule).
Every edit is marked “added by tools/new_site.py”, keeps each file’s own line endings (LF or CRLF), and is safe to run twice.
The home page only changes with --add-to-home (a new place on home is her yes, and tests/check_page.js expects four places).
Afterwards: python tools/restart_family.py, so the family server knows the new site.
"""
import argparse, colorsys, datetime, difflib, json, os, re, shutil, stat, subprocess, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_NAME = os.path.join('templates', 'new-site')
DEFAULT_ACCENT = '#3D6A8A'
MARK = 'added by tools/new_site.py'
TAKEN = {'site', 'family', 'tools', 'tests', 'templates', 'research', 'for-jemma', 'logs', 'node_modules', '_site', 'api',
         'library', 'sim-world', 'pokedex', 'travels', 'img', 'fonts', 'home', 'concepts'}
TEXT = ('.html', '.css', '.js', '.md', '.svg', '.gitignore', '.json')
# the backgrounds in templates/new-site/site/site.css that the accent sits on
LIGHT_BGS = ('#F1F0EB', '#FAFAF7', '#FFFFFF')
DARK_BGS = ('#24262A', '#202226', '#1B1C1F')
BAR_LIGHT, BAR_DARK = '#F1F0EB', '#202226'
BAD_NAME = re.compile(r'[\x00-\x1f\x7f<>"&\\`${}]')


# ---------- colours ----------
def rgb(typed):
    h = typed.strip().lstrip('#')
    if len(h) == 3 and re.fullmatch(r'[0-9a-fA-F]{3}', h):
        h = ''.join(c * 2 for c in h)
    if not re.fullmatch(r'[0-9a-fA-F]{6}', h):
        raise ValueError(f'“{typed}” is not a colour: give it like #3D6A8A')
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


# ---------- reading and writing, keeping each file's own line endings ----------
def read(p):
    """(text with \\n line endings, the file's own line ending)."""
    with open(p, encoding='utf-8', newline='') as f:
        raw = f.read()
    return raw.replace('\r\n', '\n'), ('\r\n' if '\r\n' in raw else '\n')


def write(p, text, eol='\n'):
    with open(p + '.tmp', 'w', encoding='utf-8', newline='') as f:
        f.write(text.replace('\n', eol) if eol != '\n' else text)
    os.replace(p + '.tmp', p)


# ---------- the wiring: each edit takes and returns \n text (unchanged if already done / not there) ----------
def block(text, start, end):
    """(i, j) of the inside of `start … end` (end is the first line after start that is exactly `end`)."""
    i = text.find(start)
    if i < 0:
        raise ValueError(f'could not find “{start.strip()}”')
    i += len(start)
    m = re.compile('^' + re.escape(end) + r'[ \t]*$', re.M).search(text, i)
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
    return text[:i] + re.sub(key_re + r'.*\n', '', text[i:j], flags=re.M) + text[j:]


def build_add(t, folder):
    m = re.search(r'^APPS = \{(.*)\}[ \t]*$', t, re.M)
    if not m:
        raise ValueError('could not find “APPS = {…}” on one line')
    if f"'{folder}':" in m.group(1):
        return t
    return t[:m.end(1)] + f", '{folder}': '{folder}/site'" + t[m.end(1):]


def build_remove(t, folder):
    return re.sub(rf",\s*'{re.escape(folder)}': '[^']*'(?=[^\n]*\}}[ \t]*$)", '', t, count=1, flags=re.M)


def ignore_lines(folder):
    return f'# {folder}: {MARK} (its own repo until it becomes a submodule: `new_site.py {folder} --unignore` takes these two lines out)\n/{folder}/\n'


def ignore_add(t, folder):
    if re.search(rf'^/{re.escape(folder)}/[ \t]*$', t, re.M):
        return t
    return t + ('' if t.endswith('\n') or not t else '\n') + ignore_lines(folder)


def ignore_remove(t, folder):
    t = re.sub(rf'^# {re.escape(folder)}: {re.escape(MARK)}.*\n', '', t, flags=re.M)
    return re.sub(rf'^/{re.escape(folder)}/[ \t]*\n?', '', t, flags=re.M)


def home_line(folder, name, accent):
    return (f'    {{name:{json.dumps(name, ensure_ascii=False)}, url:"/{folder}/", title:{json.dumps("My " + name, ensure_ascii=False)}, pc:"{accent}", pic:null,\n'
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
    new = re.sub(r'^    \{name:"[^\n]*", url:"/' + re.escape(folder) + r'/".*\n.*' + re.escape(MARK) + r'.*\n', '', inside, flags=re.M)
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


def profile_name(name, folder):
    plain = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()   # Café → Cafe
    return re.sub(r'[^A-Za-z0-9 ]', '', plain).strip() or folder


def wiring(folder, name, accent, shortcut=False):
    """{file: (add, remove)}: every place in the parent that lists the sites."""
    q = re.escape(folder)
    key = rf"^\s*'{q}':"
    py_name, ps_name = repr(name), name   # names can’t hold quotes, backslashes, ` or $ (BAD_NAME), so these are safe literals
    edits = {
        'tools/serve_all.py': (
            lambda t: add_line(t, 'APPS = {', '}', key, f"    '{folder}': ('{folder}/site', None, None),   # {MARK}"),
            lambda t: remove_line(t, 'APPS = {', '}', key)),
        'tools/open_site.pyw': (
            lambda t: add_line(t, 'SITES = {', '}', key, f"    '{folder}': ('/{folder}/', os.path.join(LOCAL, {('Jemmas ' + profile_name(name, folder))!r}, 'Chrome')),   # {MARK}"),
            lambda t: remove_line(t, 'SITES = {', '}', key)),
        'tools/check_all.py': (
            lambda t: add_line(t, 'CHECKS = [', ']', rf"^\s*\(.*os\.path\.join\(ROOT, '{q}'\)", f"    ({py_name}, os.path.join(ROOT, '{folder}'), [NODE, 'tests/check_site.js']),   # {MARK}"),
            lambda t: remove_line(t, 'CHECKS = [', ']', rf"^\s*\(.*os\.path\.join\(ROOT, '{q}'\)")),
        'tools/build_site.py': (lambda t: build_add(t, folder), lambda t: build_remove(t, folder)),
        'tests/axe_all.js': (
            lambda t: add_line(t, 'const PAGES = [', '];', rf"^\s*'/{q}/'", f"  '/{folder}/', '/{folder}/#/list',   // {MARK}"),
            lambda t: remove_line(t, 'const PAGES = [', '];', rf"^\s*'/{q}/'")),
        'tools/backup_new_sites.py': (
            lambda t: add_line(t, 'SITES = [', ']', rf"^\s*\(.*, '{q}'\),", f"    ({py_name}, '{folder}'),   # {MARK}"),
            lambda t: remove_line(t, 'SITES = [', ']', rf"^\s*\(.*, '{q}'\),")),
        '.gitignore': (lambda t: ignore_add(t, folder), lambda t: ignore_remove(t, folder)),
    }
    if shortcut:
        edits['tools/setup_pc.ps1'] = (
            lambda t: add_line(t, '$apps = @(', ')', rf"site = '{q}'", f'  @{{ name = "Jemma’s {ps_name}"; site = \'{folder}\'; icon = "$jj\\{folder}\\site\\icon.ico,0" }}   # {MARK}'),
            None)
    return edits


def setup_remove(folder):
    return lambda t: remove_line(t, '$apps = @(', ')', rf"^.*site = '{re.escape(folder)}'")


# ---------- helpers ----------
def show_diff(path, old, new):
    for line in difflib.unified_diff(old.splitlines(), new.splitlines(), path, path, n=0, lineterm=''):
        print('    ' + line)


def git(cwd, *args):
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')


def plan(root, changes):
    """Works out every edit without writing: [(rel, path, old, new, eol)]. Raises ValueError if any can’t be made."""
    out = []
    for rel, f in changes.items():
        p = os.path.join(root, rel)
        if not os.path.exists(p):
            print(f'  skip {rel}: not found')
            continue
        old, eol = read(p)
        try:
            new = f(old)
        except ValueError as e:
            raise ValueError(f'{rel}: {e}')
        out.append((rel, p, old, new, eol))
    return out


def show(planned, dry):
    for rel, p, old, new, eol in planned:
        if new == old:
            print(f'  {rel}: nothing to change')
            continue
        print(f'  {rel}:' + (' (would change)' if dry else ''))
        show_diff(rel, old, new)


def write_all(planned):
    for rel, p, old, new, eol in planned:
        if new != old:
            write(p, new, eol)


def rmtree(p):
    def again(func, path, _):   # git's object files are read-only on Windows
        os.chmod(path, stat.S_IWRITE)
        func(path)
    shutil.rmtree(p, onerror=again)


def existing(dest):
    """(name, accent) of a site already made, read back from its own files (None where not found)."""
    name = accent = None
    try:
        t, _ = read(os.path.join(dest, 'site', 'index.html'))
        m = re.search(r'<title>Jemma’s (.+?)</title>', t)
        name = m and m.group(1)
    except OSError:
        pass
    try:
        t, _ = read(os.path.join(dest, 'site', 'site.css'))
        m = re.findall(r'--accent:\s*(#[0-9A-Fa-f]{6})', t)   # light, then dark
        accent = m and tuple(m[:2]) if len(m) >= 2 else (m[0], None) if m else None
    except OSError:
        pass
    return name, accent


def make_folder(template, dest, fill, root, name):
    shutil.copytree(template, dest, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    left = []
    for d, _, files in os.walk(dest):
        for f in files:
            p = os.path.join(d, f)
            if not f.endswith(TEXT):
                continue
            t, eol = read(p)
            for k, v in fill.items():
                t = t.replace(k, v)
            write(p, t, eol)
            left += [os.path.relpath(p, dest) + ': ' + m for m in set(re.findall(r'__[A-Z_]+__', t))]
    if left:
        raise RuntimeError('not filled in: ' + '; '.join(left))
    r = git(dest, 'init', '-q', '-b', 'main')
    if r.returncode:
        raise RuntimeError('git init failed: ' + r.stderr.strip())
    for k in ('user.name', 'user.email'):
        v = git(root, 'config', '--get', k).stdout.strip()
        if v:
            git(dest, 'config', k, v)
    git(dest, 'add', '-A')
    r = git(dest, 'commit', '-q', '-m', f'Start Jemma’s {name} from the family template (tools/new_site.py in Jemma’s Journals)')
    if r.returncode:
        raise RuntimeError('git commit failed: ' + (r.stderr or r.stdout).strip())


def main():
    ap = argparse.ArgumentParser(description='Start a new site in Jemma’s family from templates/new-site.')
    ap.add_argument('folder', help='the folder and address, lower case with hyphens, e.g. recipes')
    ap.add_argument('name', nargs='?', help='the name after “Jemma’s”, e.g. Recipes (read from the site if it exists)')
    ap.add_argument('accent', nargs='?', help=f'the accent colour, e.g. #8A3B2E (default {DEFAULT_ACCENT}, or the site’s own if it exists)')
    ap.add_argument('--dry-run', action='store_true', help='show what would happen, change nothing')
    ap.add_argument('--remove', action='store_true', help='undo the wiring for this folder (the folder itself is kept)')
    ap.add_argument('--unignore', action='store_true', help='only take it out of the parent’s .gitignore (before git submodule add)')
    ap.add_argument('--add-to-home', action='store_true', help='also add a placeholder place to the home page (site/home.js)')
    ap.add_argument('--shortcut', action='store_true', help='also list it in tools/setup_pc.ps1 for a Desktop/Start shortcut')
    ap.add_argument('--parent', default=ROOT, help=argparse.SUPPRESS)   # for testing on a copy of Jemma’s Journals
    a = ap.parse_args()
    root = os.path.abspath(a.parent)
    folder = a.folder.strip().strip('/\\')
    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', folder) or len(folder) > 40 or folder in TAKEN:
        sys.exit(f'“{folder}” can’t be used: use lower case letters and numbers with single hyphens between words, not one of {", ".join(sorted(TAKEN))}')
    dest = os.path.join(root, folder)
    dry = ' (dry run: nothing changed)' if a.dry_run else ''

    if a.remove or a.unignore:
        if a.unignore:
            print(f'Taking {folder} out of the parent’s .gitignore{dry}:')
            changes = {'.gitignore': lambda t: ignore_remove(t, folder)}
        else:
            print(f'Taking {folder} out of the family wiring{dry}:')
            changes = {rel: rem for rel, (_, rem) in wiring(folder, folder, DEFAULT_ACCENT).items()}
            changes['site/home.js'] = lambda t: home_remove(t, folder)
            changes['tools/setup_pc.ps1'] = setup_remove(folder)
        planned = plan(root, changes)
        show(planned, a.dry_run)
        if not a.dry_run:
            write_all(planned)
        if a.remove:
            if os.path.exists(dest):
                print(f'\nThe folder itself is kept: {dest}\nTo delete it too (it can’t be undone; check nothing in it is wanted first):\n'
                      f'    Remove-Item -Recurse -Force "{dest}"')
                gm = os.path.join(root, '.gitmodules')
                if os.path.exists(gm) and f'path = {folder}' in read(gm)[0]:
                    print(f'It is a submodule of Jemma’s Journals: first  git rm {folder}  in {root}')
            print('Then: python tools/restart_family.py  (so the family server stops serving it)')
        return 0

    old_name, old = existing(dest) if os.path.exists(dest) else (None, None)
    old_accent, old_dark = old or (None, None)
    name = (a.name or old_name or '').strip().replace("'", '’')
    if not name:
        sys.exit('Give the name too, e.g.  python tools/new_site.py recipes "Recipes"')
    if BAD_NAME.search(name) or len(name) > 40:
        sys.exit('The name can’t be longer than 40 letters or contain tabs, new lines or any of  < > " & \\ ` $ { }')
    try:
        light, dark, notes = accents(a.accent or old_accent or DEFAULT_ACCENT)
    except ValueError as e:
        sys.exit(str(e))
    if old_accent and old_dark and not a.accent:
        dark = old_dark   # the site’s own pair, as it was made
    template = os.path.join(root, TEMPLATE_NAME)
    if not os.path.isdir(template):
        sys.exit(f'The template is missing: {template}')
    today = datetime.date.today()
    fill = {'__NAME__': name, '__FOLDER__': folder, '__ACCENT__': light, '__ACCENT_DARK__': dark,
            '__BAR_LIGHT__': BAR_LIGHT, '__BAR_DARK__': BAR_DARK, '__DATE__': f'{today.day} {today:%b %Y}'}
    print(f'Jemma’s {name}: folder {dest}, address /{folder}/, accent {light} (dark mode {dark})' + dry)
    if os.path.exists(dest):
        print(f'  {folder}/ already exists: not copied over (only the wiring is checked)'
              + (f'; its colour {old_accent} is used' if old_accent and not a.accent else ''))
    for n in notes:
        print('  note: ' + n)

    # 1. every change worked out first: if one can’t be made, nothing is copied or written
    changes = {rel: add for rel, (add, _) in wiring(folder, name, light, a.shortcut).items()}
    if a.add_to_home:
        changes['site/home.js'] = lambda t: home_add(t, folder, name, light)
    try:
        planned = plan(root, changes)
    except ValueError as e:
        sys.exit(f'Stopped before changing anything: {e}')

    # 2–3. the files and their own git
    if not os.path.exists(dest):
        if a.dry_run:
            print(f'  would copy {TEMPLATE_NAME} to {folder}/ and fill in the names and colours, then git init with a first commit')
        else:
            try:
                make_folder(template, dest, fill, root, name)
            except Exception as e:
                if os.path.exists(dest):
                    rmtree(dest)   # only the folder this run made
                sys.exit(f'Stopped: {e}. The half-made {folder}/ was taken away again; nothing else was changed.')
            print(f'  made {folder}/ from the template, with its own git and a first commit')

    # 4. the wiring
    print('Wiring it into the family:')
    show(planned, a.dry_run)
    if not a.dry_run:
        write_all(planned)
    if not a.add_to_home:
        print(f'\nThe home page is unchanged (a new place on home is her yes). To add it later:  python tools/new_site.py {folder} --add-to-home')
    else:
        print('  note: tests/check_page.js expects four places on home: update its “four places” checks.')
    if not a.shortcut:
        print(f'No Desktop/Start shortcut yet. For one:  python tools/new_site.py {folder} --shortcut  then run tools/setup_pc.ps1 again.')
    else:
        print('Shortcut listed in tools/setup_pc.ps1: run it again to make it (powershell -ExecutionPolicy Bypass -File tools\\setup_pc.ps1).')

    owner = 'jemmathornton'
    m = re.search(r'github\.com[:/]([^/]+)/', git(root, 'remote', 'get-url', 'origin').stdout)
    if m:
        owner = m.group(1)
    print(f'''
Next:
  - python tools/restart_family.py   (the family server then knows it), and open http://localhost:8050/{folder}/
  - its checks:  cd "{dest}"  then  ..\\.tools\\node\\node.exe tests\\check_site.js
  - make it hers: the words in site/js/data.js, the look in site/site.css (tokens at the top), its CLAUDE.md
  - until it has a GitHub repo it is only on this PC: no backup (the daily backup pushes it once it has one)

Only with her OK (a GitHub repo is her decision; public repos can be read by anyone):
  cd "{dest}"
  & "C:\\Program Files\\GitHub CLI\\gh.exe" repo create {owner}/{folder} --public --source . --push      (or --private)
  cd "{root}"
  python tools/new_site.py {folder} --unignore
  git submodule add https://github.com/{owner}/{folder}.git {folder}
  git commit -m "Add Jemma’s {name} as a submodule" -- .gitignore .gitmodules {folder}
  git -c "credential.helper=!'C:/Program Files/GitHub CLI/gh.exe' auth git-credential" push
Then add '{folder}' to APPS in tools/record_apps.py and to the git list in tools/check_all.py (they check submodules).''')
    return 0


if __name__ == '__main__':
    sys.exit(main())
