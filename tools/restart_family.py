"""Restart the family server (tools/serve_all.py, http://localhost:8050), e.g. after tools/new_site.py added a site.

    python tools/restart_family.py           (or double-click it: no window needed)

The server runs without a window from the Startup folder, so there is no button to stop it. This finds the Python that
runs this folder's tools/serve_all.py on that port, stops it, and starts it again on its own (detached, no window), the
same way tools/open_site.pyw does. The apps' own save servers (Library, Pokédex, Travels) keep running. Your open app
windows just need a reload.
"""
import json, os, socket, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, 'tools', 'serve_all.py')
PORT = int(sys.argv[sys.argv.index('--port') + 1]) if '--port' in sys.argv else 8050   # another port only for testing a copy


def answering():
    try:
        with socket.create_connection(('127.0.0.1', PORT), timeout=.5):
            return True
    except OSError:
        return False


def servers():
    """Process ids of the Pythons running this folder's serve_all.py on PORT."""
    ps = ("Get-CimInstance Win32_Process -Filter \"Name like 'python%'\" | Select-Object ProcessId, CommandLine | ConvertTo-Json -Compress")
    r = subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-Command', ps], capture_output=True, text=True,
                       encoding='utf-8', errors='replace', creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    try:
        rows = json.loads(r.stdout or '[]')
    except ValueError:
        return []
    rows = [rows] if isinstance(rows, dict) else rows
    want = os.path.normcase(os.path.normpath(SCRIPT))
    found = []
    for row in rows:
        cmd = row.get('CommandLine') or ''
        if want not in os.path.normcase(cmd.replace('/', '\\')):
            continue
        parts = cmd.split()
        port = int(parts[parts.index('--port') + 1]) if '--port' in parts and parts.index('--port') + 1 < len(parts) else 8050
        if port == PORT and row.get('ProcessId') != os.getpid():
            found.append(row['ProcessId'])
    return found


def main():
    pids = servers()
    for pid in pids:
        subprocess.run(['taskkill', '/PID', str(pid), '/F'], capture_output=True)
    for _ in range(50):
        if not answering():
            break
        time.sleep(.1)
    if answering():
        print(f'Something else is answering on port {PORT} (not this folder’s serve_all.py): not restarted.')
        return 1
    pyw = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
    exe = pyw if os.path.exists(pyw) else sys.executable
    flags = 0x00000008 | 0x00000200 | 0x08000000   # detached, its own process group, no window
    subprocess.Popen([exe, SCRIPT] + (['--port', str(PORT)] if PORT != 8050 else []), cwd=ROOT, creationflags=flags,
                     close_fds=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(100):
        if answering():
            print(f"The family server {'restarted' if pids else 'started'}: http://localhost:{PORT}/")
            return 0
        time.sleep(.1)
    print(f'Started it, but nothing answers on port {PORT} yet: try  python tools/serve_all.py  to see why.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
