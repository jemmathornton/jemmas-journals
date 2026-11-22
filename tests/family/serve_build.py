"""The online-style copy for the tests: tools/build_site.py's build, in a temp folder, served like a plain web host.

    python -I tests/family/serve_build.py --port 8161 --out <temp folder> [--reuse]

Builds with tools/build_site.py's own build() (pointed at --out instead of _site/), then serves it with build_site's own
plain handler (its 404.html for missing pages; no forwarding, no dark-mode help). --reuse keeps an existing build in
--out (tools/check_all.py builds once for every part that needs it). Prints "ready <port>" once it is listening.
"""
import argparse, functools, http.server, importlib.util, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_build_site(out):
    spec = importlib.util.spec_from_file_location('build_site_under_test', os.path.join(ROOT, 'tools', 'build_site.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.OUT = os.path.abspath(out)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--reuse', action='store_true')
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    if os.path.normcase(out) == os.path.normcase(os.path.join(ROOT, '_site')):
        sys.exit('use a temp folder, not _site/ (the 8060 preview may be serving it)')
    bs = load_build_site(out)
    if not (a.reuse and os.path.exists(os.path.join(out, 'index.html'))):
        bs.build()
    handler = functools.partial(bs.Quiet, directory=out)
    class Host(http.server.ThreadingHTTPServer):
        daemon_threads = True
        request_queue_size = 128   # every picture is its own connection (as in serve_all.py)
    server = Host(('127.0.0.1', a.port), handler)
    print(f'ready {a.port}', flush=True)
    server.serve_forever()


if __name__ == '__main__':
    main()
