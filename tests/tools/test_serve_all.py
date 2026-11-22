"""tools/serve_all.py, the family server: who may use it, what it will and won't send, dark mode, and passing saves on.

Each test class runs the real Handler on a spare port with its dark-mode file in a temp folder (never her
logs/family-mode.txt) and the apps' save servers replaced by a fake one (or by nothing), and never starts her app servers.
"""
import http.client, http.server, json, os, socket, subprocess, sys, tempfile, threading, time, unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from support import ROOT, free_port, load  # noqa: E402

SECRET = 'The whole family on one address'   # words from serve_all.py itself: must never be sent


class FakeApp(http.server.BaseHTTPRequestHandler):
    """An app's save server: records what it was sent and answers with JSON (or an error for /api/missing)."""
    seen = []

    def answer(self):
        body = self.rfile.read(int(self.headers.get('Content-Length') or 0)) if self.command == 'POST' else b''
        FakeApp.seen.append({'method': self.command, 'path': self.path, 'body': body, 'headers': dict(self.headers)})
        if self.path.startswith('/api/missing'):
            data, status = b'{"error":"no"}', 404
        else:
            data, status = json.dumps({'ok': True, 'path': self.path}).encode(), 200
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Secret', 'should-not-pass')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    do_GET = do_POST = answer

    def log_message(self, *a):
        pass


class ServeAllCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix='jj-serve-')
        cls.sa = load(os.path.join('tools', 'serve_all.py'))
        cls.port = free_port()
        cls.app_port = free_port()
        cls.fake = http.server.ThreadingHTTPServer(('127.0.0.1', cls.app_port), FakeApp)
        threading.Thread(target=cls.fake.serve_forever, daemon=True).start()
        cls.sa.PORT = cls.port
        cls.sa.MODE_FILE = os.path.join(cls.tmp, 'logs', 'family-mode.txt')
        cls.started = []
        cls.sa.start_app_servers = lambda: cls.started.append(1)
        cls.sa.APPS = {k: (folder, cls.app_port if port else None, None) for k, (folder, port, _) in cls.sa.APPS.items()}
        cls.server = cls.sa.Server(('127.0.0.1', cls.port), cls.sa.Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close()
        cls.fake.shutdown(); cls.fake.server_close()
        import shutil; shutil.rmtree(cls.tmp, ignore_errors=True)

    def setUp(self):
        FakeApp.seen.clear()
        self.started.clear()
        if os.path.exists(self.sa.MODE_FILE):
            os.remove(self.sa.MODE_FILE)

    # ---- helpers ----
    def req(self, method, path, body=None, headers=None, host=None):
        c = http.client.HTTPConnection('127.0.0.1', self.port, timeout=10)
        h = {'Host': host if host is not None else f'localhost:{self.port}'}
        h.update(headers or {})
        c.request(method, path, body=body, headers=h)
        r = c.getresponse()
        data = r.read()
        c.close()
        return r.status, dict(r.getheaders()), data

    def raw(self, line, host=None):
        """Send a request line exactly as written (no client tidying of the path)."""
        s = socket.create_connection(('127.0.0.1', self.port), timeout=10)
        s.sendall(line.encode('latin-1') + f'\r\nHost: {host or "localhost:%d" % self.port}\r\nConnection: close\r\n\r\n'.encode())
        out = b''
        try:
            while True:
                chunk = s.recv(65536)
                if not chunk:
                    break
                out += chunk
        except (ConnectionResetError, socket.timeout):
            pass
        s.close()
        status = int(out.split(b' ', 2)[1]) if out.startswith(b'HTTP/') else None
        return status, out


class WhoMayUseIt(ServeAllCase):
    def test_localhost_and_127_are_served(self):
        for host in (f'localhost:{self.port}', f'127.0.0.1:{self.port}', f'LOCALHOST:{self.port}'):
            self.assertEqual(self.req('GET', '/', host=host)[0], 200, host)

    def test_other_names_are_refused(self):
        # a page elsewhere pointing its own name at this computer (DNS rebinding) gets nothing
        for host in ('evil.example', f'evil.example:{self.port}', 'localhost', f'localhost:{self.port + 1}', f'192.168.1.5:{self.port}', ''):
            for method in ('GET', 'HEAD', 'POST'):
                status, _, data = self.req(method, '/library/api/books', body=b'' if method == 'POST' else None, host=host)
                self.assertEqual(status, 403, f'{method} with Host {host!r}')
        self.assertEqual(FakeApp.seen, [], 'nothing was passed on to an app')

    def test_listens_on_this_computer_only(self):
        self.assertEqual(self.server.server_address[0], '127.0.0.1')
        with open(os.path.join(ROOT, 'tools', 'serve_all.py'), encoding='utf-8') as f:
            src = f.read()
        self.assertIn("Server(('127.0.0.1', PORT)", src)


class WhatItSends(ServeAllCase):
    def assertNotLeaked(self, status, data, what):
        self.assertNotEqual(status, 200, what)
        self.assertNotIn(SECRET.encode(), data, what)

    def test_no_way_out_of_the_site_folders(self):
        for path in ('/../tools/serve_all.py', '/%2e%2e/tools/serve_all.py', '/%2E%2E%2Ftools%2Fserve_all.py',
                     '/library/../../tools/serve_all.py', '/library/..%2f..%2ftools%2fserve_all.py', '/family/../../tools/serve_all.py',
                     '/..\\tools\\serve_all.py', '/library/..\\..\\tools\\serve_all.py', '/library/%5c..%5c..%5ctools%5cserve_all.py',
                     '/sim-world/%2e%2e/%2e%2e/tools/serve_all.py', '//tools/serve_all.py', '/C:/Windows/win.ini',
                     '/library/C:%5cWindows%5cwin.ini', '/%252e%252e/tools/serve_all.py'):
            status, data = self.raw(f'GET {path} HTTP/1.1')
            self.assertNotLeaked(status, data, path)

    def test_a_nul_in_the_address_is_refused(self):
        for path in ('/%00', '/index.html%00.txt', '/library/%00/../x'):
            status, data = self.raw(f'GET {path} HTTP/1.1')
            self.assertIn(status, (400, 403, 404, None), path)
            self.assertNotLeaked(status, data, path)

    def test_no_folder_listings(self):
        for path in ('/img/', '/img/maps/', '/library/js/', '/family/', '/pokedex/img/'):
            status, _, data = self.req('GET', path)
            self.assertEqual(status, 404, path)
            self.assertNotIn(b'Directory listing', data, path)

    def test_missing_pages_get_the_404_page(self):
        for path in ('/no-such-page', '/library/no-such.html', '/travels/js/nope.js'):
            status, headers, data = self.req('GET', path)
            self.assertEqual(status, 404, path)
            self.assertIn(b'Page not found', data, path)
            self.assertIn(b'data-jj-server-mode="light"', data, path)
        self.assertEqual(self.req('HEAD', '/no-such-page')[0], 404)

    def test_each_site_and_the_shared_code(self):
        for path, words in (('/', b'Jemma'), ('/library/', b'Library'), ('/sim-world/', b'Sim World'), ('/pokedex/', b'Pok'),
                            ('/travels/', b'Travels'), ('/family/family.js', b'JJFamily'), ('/family/mode.js', b'jj-mode')):
            status, headers, data = self.req('GET', path)
            self.assertEqual(status, 200, path)
            self.assertIn(words, data, path)
            self.assertEqual(headers.get('Cache-Control'), 'no-cache', path)

    def test_an_app_without_its_slash_is_sent_to_it(self):
        status, headers, _ = self.req('GET', '/pokedex?x=1')
        self.assertEqual((status, headers.get('Location')), (301, '/pokedex/?x=1'))

    def test_other_methods_are_refused(self):
        self.assertEqual(self.req('POST', '/index.html', body=b'x')[0], 405)
        self.assertIn(self.req('PUT', '/index.html', body=b'x')[0], (405, 501))
        self.assertIn(self.req('DELETE', '/index.html')[0], (405, 501))


class DarkMode(ServeAllCase):
    def set_file(self, text):
        os.makedirs(os.path.dirname(self.sa.MODE_FILE), exist_ok=True)
        with open(self.sa.MODE_FILE, 'w', encoding='utf-8') as f:
            f.write(text)

    def test_light_until_chosen(self):
        self.assertEqual(self.req('GET', '/family/mode')[2], b'light')
        self.set_file('dark\n')
        self.assertEqual(self.req('GET', '/family/mode')[2], b'dark')
        self.set_file('purple')
        self.assertEqual(self.req('GET', '/family/mode')[2], b'light')

    def test_saving_needs_the_family_header(self):
        status, _, data = self.req('POST', '/family/mode', body=b'dark', headers={'X-Family': '1', 'Content-Type': 'text/plain'})
        self.assertEqual((status, data), (200, b'dark'))
        self.assertEqual(open(self.sa.MODE_FILE, encoding='utf-8').read(), 'dark')
        self.assertFalse(os.path.exists(self.sa.MODE_FILE + '.tmp'))
        status, _, _ = self.req('POST', '/family/mode', body=b'light', headers={'Content-Type': 'text/plain'})
        self.assertEqual(status, 405, 'without X-Family')
        self.assertEqual(open(self.sa.MODE_FILE, encoding='utf-8').read(), 'dark', 'unchanged')
        status, _, _ = self.req('POST', '/family/mode', body=b'light', headers={'X-Family': '1'}, host='evil.example')
        self.assertEqual(status, 403, 'from another name')
        for bad in (b'purple', b'', b'darkdarkdarkdarkdark', b'<script>'):
            self.assertEqual(self.req('POST', '/family/mode', body=bad, headers={'X-Family': '1'})[0], 400, bad)
        self.assertEqual(open(self.sa.MODE_FILE, encoding='utf-8').read(), 'dark', 'unchanged by bad values')

    def test_the_choice_is_written_into_every_page(self):
        for mode in ('light', 'dark'):
            self.set_file(mode)
            for path in ('/', '/index.html', '/library/', '/sim-world/', '/pokedex/index.html', '/travels/', '/404.html'):
                status, headers, data = self.req('GET', path)
                self.assertEqual(status, 200, path)
                self.assertEqual(data.lower().count(b'data-jj-server-mode='), 1, path)
                self.assertRegex(data[:400].decode('utf-8', 'replace'), r'<html data-jj-server-mode="%s"[ >]' % mode, path)
                self.assertEqual(int(headers['Content-Length']), len(data), path)
                self.assertIn('text/html', headers['Content-Type'])
        status, _, data = self.req('GET', '/family/family.css')
        self.assertNotIn(b'data-jj-server-mode', data, 'only pages are changed')


class PassingSavesOn(ServeAllCase):
    def test_gets_and_posts_go_to_the_apps_own_server(self):
        status, headers, data = self.req('GET', '/library/api/reading-status?x=1', headers={'X-Library': '1', 'Cookie': 'a=b'})
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(data)['path'], '/api/reading-status?x=1')
        self.assertEqual(headers.get('Content-Type'), 'application/json')
        self.assertEqual(headers.get('Cache-Control'), 'no-store', "the app's own cache rule, not no-cache")
        self.assertNotIn('X-Secret', headers, 'only Content-Type and Cache-Control come back')
        sent = FakeApp.seen[-1]
        self.assertEqual(sent['headers'].get('X-Library'), '1')
        self.assertNotIn('Cookie', sent['headers'], 'only the listed headers are passed on')
        status, _, data = self.req('POST', '/pokedex/api/collection', body=b'{"a":1}',
                                   headers={'Content-Type': 'application/json', 'X-Pokedex': '1'})
        self.assertEqual(status, 200)
        self.assertEqual((FakeApp.seen[-1]['method'], FakeApp.seen[-1]['body'], FakeApp.seen[-1]['headers'].get('X-Pokedex')),
                         ('POST', b'{"a":1}', '1'))
        self.req('POST', '/travels/api/post', body=b'{}', headers={'X-Travels': '1'})
        self.assertEqual(FakeApp.seen[-1]['path'], '/api/post')

    def test_the_apps_errors_come_back_as_they_are(self):
        status, _, data = self.req('GET', '/library/api/missing')
        self.assertEqual((status, data), (404, b'{"error":"no"}'))

    def test_sim_world_has_no_save_server(self):
        status, _, _ = self.req('GET', '/sim-world/api/anything')
        self.assertEqual(status, 404)
        self.assertEqual(FakeApp.seen, [])

    def test_size_limits(self):
        status, _, _ = self.req('POST', '/library/api/add', body=b'', headers={'Content-Length': str(64 * 1024 * 1024 + 1)})
        self.assertEqual(status, 413)
        status, _, _ = self.req('POST', '/library/api/add', body=b'', headers={'Content-Length': '-1'})
        self.assertEqual(status, 413)
        status, data = self.raw('POST /library/api/add HTTP/1.1\r\nContent-Length: lots')
        self.assertEqual(status, 400)
        self.assertEqual(FakeApp.seen, [], 'nothing was passed on')


class WhenAnAppServerIsDown(unittest.TestCase):
    def test_503_and_it_is_started_for_next_time(self):
        sa = load(os.path.join('tools', 'serve_all.py'))
        tmp = tempfile.mkdtemp(prefix='jj-serve-')
        sa.PORT = free_port()
        sa.MODE_FILE = os.path.join(tmp, 'mode.txt')
        calls = []
        sa.start_app_servers = lambda: calls.append(1)
        dead = free_port()
        sa.APPS = {k: (f, dead if p else None, None) for k, (f, p, _) in sa.APPS.items()}
        server = sa.Server(('127.0.0.1', sa.PORT), sa.Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            c = http.client.HTTPConnection('127.0.0.1', sa.PORT, timeout=10)
            c.request('GET', '/travels/api/ping', headers={'Host': f'localhost:{sa.PORT}'})
            r = c.getresponse(); body = r.read()
            self.assertEqual(r.status, 503)
            self.assertIn(b'not running', body)
            self.assertEqual(calls, [1])
        finally:
            server.shutdown(); server.server_close()


class StartingAppServers(unittest.TestCase):
    def setUp(self):
        self.sa = load(os.path.join('tools', 'serve_all.py'))
        self.tmp = tempfile.mkdtemp(prefix='jj-start-')
        self.sa.ROOT = self.tmp
        for app in ('library', 'pokedex'):   # travels' script is missing here
            os.makedirs(os.path.join(self.tmp, app, 'tools'))
            open(os.path.join(self.tmp, app, 'tools', 'serve.py'), 'w').close()

    def test_starts_only_the_missing_ones_whose_script_is_there(self):
        running = {8020}
        with mock.patch.object(self.sa, 'answering', side_effect=lambda p: p in running), \
                mock.patch.object(self.sa.subprocess, 'Popen') as popen:
            self.sa.start_app_servers()
        started = [c.args[0][1] for c in popen.call_args_list]
        self.assertEqual(started, [os.path.join(self.tmp, 'pokedex/tools/serve.py')])
        kw = popen.call_args.kwargs
        self.assertEqual(kw['cwd'], os.path.join(self.tmp, 'pokedex'))
        self.assertEqual(kw['stdin'], subprocess.DEVNULL)
        if os.name == 'nt':
            self.assertTrue(kw['creationflags'] & 0x00000008, 'detached, so it keeps running on its own')

    def test_nothing_when_all_are_running(self):
        with mock.patch.object(self.sa, 'answering', return_value=True), mock.patch.object(self.sa.subprocess, 'Popen') as popen:
            self.sa.start_app_servers()
        popen.assert_not_called()


class OneCopyOnly(unittest.TestCase):
    def test_a_second_copy_exits_quietly_when_the_port_is_taken(self):
        port = free_port()
        holder = socket.socket(); holder.bind(('127.0.0.1', port)); holder.listen(5)
        try:
            t = time.time()
            r = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'tools', 'serve_all.py'), '--port', str(port)],
                               capture_output=True, text=True, timeout=30)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertLess(time.time() - t, 15)
            self.assertNotIn('Ctrl+C', r.stdout, 'it did not start serving')
        finally:
            holder.close()

    def test_the_port_is_not_shared(self):
        sa = load(os.path.join('tools', 'serve_all.py'))
        self.assertFalse(sa.Server.allow_reuse_address)
        self.assertGreaterEqual(sa.Server.request_queue_size, 64)
        port = free_port()
        a = sa.Server(('127.0.0.1', port), sa.Handler)
        try:
            with self.assertRaises(OSError):
                sa.Server(('127.0.0.1', port), sa.Handler)
        finally:
            a.server_close()


if __name__ == '__main__':
    unittest.main()
