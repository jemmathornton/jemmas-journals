"""A throwaway copy of the family server (tools/serve_all.py) for the tests, on a spare port.

    python -I tests/family/serve_family.py --port 8151 --mode-file <temp file> [--app-port <port>]

It is the real Handler from tools/serve_all.py, with three things changed so a test can never touch her own things:
  - the dark-mode choice is kept in --mode-file (a temp file), never her logs/family-mode.txt;
  - it never starts the apps' own save servers;
  - save requests (…/api/…) go to --app-port (default: a port nothing listens on, so they get the 503 page).
Prints "ready <port>" once it is listening.
"""
import argparse, importlib.util, os, socket, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dead_port():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close()
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, required=True)
    ap.add_argument('--mode-file', required=True)
    ap.add_argument('--app-port', type=int, default=0)
    a = ap.parse_args()
    if os.path.normcase(os.path.abspath(a.mode_file)) == os.path.normcase(os.path.join(ROOT, 'logs', 'family-mode.txt')):
        sys.exit('refusing to use her own logs/family-mode.txt')
    sa = load('serve_all_under_test', os.path.join('tools', 'serve_all.py'))
    app_port = a.app_port or dead_port()
    sa.PORT = a.port
    sa.MODE_FILE = os.path.abspath(a.mode_file)
    sa.start_app_servers = lambda: None
    sa.APPS = {k: (folder, app_port if port else None, None) for k, (folder, port, _) in sa.APPS.items()}
    server = sa.Server(('127.0.0.1', a.port), sa.Handler)
    print(f'ready {a.port}', flush=True)
    server.serve_forever()


if __name__ == '__main__':
    main()
