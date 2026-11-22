"""Open one of Jemma’s sites as an app window, through the family’s one address (no console window).

    pythonw tools/open_site.pyw library | sim-world | pokedex | travels | home

What her shortcuts run (her choice, 21 Nov: the apps load the shared code from Jemma’s Journals, so they open through it).
1. If the family server (tools/serve_all.py, http://localhost:8050) isn't running, start it on its own (it starts each
   app's own save server too), and wait for it to answer.
2. Open that site in its own Chrome window (no tabs or address bar). The Library and Pokédex keep the Chrome profiles
   they had, so Windows still gives each its own taskbar button.
"""
import os, socket, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8050
LOCAL = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
SITES = {   # name → (address, Chrome profile folder or None for her normal Chrome)
    'home': ('/', os.path.join(LOCAL, 'Jemmas Journals', 'Chrome')),
    'library': ('/library/', os.path.join(LOCAL, 'Jemmas Library', 'Chrome')),
    'sim-world': ('/sim-world/', None),
    'pokedex': ('/pokedex/', os.path.join(LOCAL, 'Jemmas Pokedex', 'Chrome')),
    'travels': ('/travels/', os.path.join(LOCAL, 'Jemmas Travels', 'Chrome')),
}
CHROMES = [os.path.join(os.environ.get(v, ''), *p) for v, p in (
    ('ProgramFiles', ('Google', 'Chrome', 'Application', 'chrome.exe')),
    ('ProgramFiles(x86)', ('Google', 'Chrome', 'Application', 'chrome.exe')),
    ('LOCALAPPDATA', ('Google', 'Chrome', 'Application', 'chrome.exe')),
    ('ProgramFiles(x86)', ('Microsoft', 'Edge', 'Application', 'msedge.exe')),
    ('ProgramFiles', ('Microsoft', 'Edge', 'Application', 'msedge.exe')))]


def answering(port=PORT):
    try:
        with socket.create_connection(('127.0.0.1', port), timeout=.5):
            return True
    except OSError:
        return False


def main():
    name = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in SITES else 'home'
    path, profile = SITES[name]
    url = f'http://localhost:{PORT}{path}'
    if not answering():
        pythonw = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
        exe = pythonw if os.path.exists(pythonw) else sys.executable
        flags = 0x00000008 | 0x00000200 | 0x08000000   # detached, its own process group, no window
        subprocess.Popen([exe, os.path.join(ROOT, 'tools', 'serve_all.py')], cwd=ROOT, creationflags=flags, close_fds=True,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(80):
            if answering():
                break
            time.sleep(.1)
    browser = next((c for c in CHROMES if os.path.exists(c)), None)
    if not browser:
        import webbrowser
        return webbrowser.open(url)
    args = [browser] + ([f'--user-data-dir={profile}', '--no-first-run', '--no-default-browser-check'] if profile else []) + [f'--app={url}']
    subprocess.Popen(args, close_fds=True)


if __name__ == '__main__':
    main()
