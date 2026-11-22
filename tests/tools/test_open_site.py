"""tools/open_site.pyw, what her shortcuts run: starts the family server if needed, then opens the site as an app window.
Nothing is started for real: answering(), subprocess.Popen and the browser list are stood in.
"""
import os, sys, unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from support import load  # noqa: E402


class OpenSite(unittest.TestCase):
    def setUp(self):
        self.o = load(os.path.join('tools', 'open_site.pyw'))
        self.o.CHROMES = [sys.executable]   # any file that exists stands in for Chrome

    def go(self, argv, running=True):
        answers = iter([running] + [False, False, True] * 30)
        with mock.patch.object(self.o, 'answering', side_effect=lambda *a: next(answers)), \
                mock.patch.object(self.o.subprocess, 'Popen') as popen, mock.patch.object(sys, 'argv', ['open_site.pyw', *argv]), \
                mock.patch.object(self.o.time, 'sleep'):
            self.o.main()
        return [c.args[0] for c in popen.call_args_list], popen

    def test_each_site_opens_at_the_family_address(self):
        for name, path in (('home', '/'), ('library', '/library/'), ('sim-world', '/sim-world/'), ('pokedex', '/pokedex/'), ('travels', '/travels/')):
            calls, _ = self.go([name])
            self.assertEqual(len(calls), 1, name)
            self.assertEqual(calls[0][-1], f'--app=http://localhost:8050{path}', name)

    def test_own_chrome_profiles_keep_their_taskbar_buttons(self):
        calls, _ = self.go(['library'])
        self.assertTrue(any(a.startswith('--user-data-dir=') and a.endswith(os.path.join('Jemmas Library', 'Chrome')) for a in calls[0]))
        calls, _ = self.go(['sim-world'])
        self.assertFalse(any(a.startswith('--user-data-dir=') for a in calls[0]), 'Sim World opens in her normal Chrome')

    def test_an_unknown_name_opens_home(self):
        calls, _ = self.go(['nonsense'])
        self.assertEqual(calls[0][-1], '--app=http://localhost:8050/')
        calls, _ = self.go([])
        self.assertEqual(calls[0][-1], '--app=http://localhost:8050/')

    def test_starts_the_family_server_when_it_is_not_running(self):
        calls, popen = self.go(['pokedex'], running=False)
        self.assertEqual(len(calls), 2)
        self.assertTrue(calls[0][1].endswith(os.path.join('tools', 'serve_all.py')))
        kw = popen.call_args_list[0].kwargs
        if os.name == 'nt':
            self.assertTrue(kw['creationflags'] & 0x08000000, 'no console window')
            self.assertTrue(kw['creationflags'] & 0x00000008, 'detached')
        self.assertEqual(calls[1][-1], '--app=http://localhost:8050/pokedex/')

    def test_never_starts_a_second_server(self):
        calls, _ = self.go(['home'], running=True)
        self.assertFalse(any('serve_all.py' in ' '.join(c) for c in calls))

    def test_no_browser_falls_back_to_the_default_one(self):
        self.o.CHROMES = [os.path.join(os.path.dirname(__file__), 'no-such-browser.exe')]
        with mock.patch('webbrowser.open') as wb:
            self.go(['travels'])
        wb.assert_called_once_with('http://localhost:8050/travels/')


if __name__ == '__main__':
    unittest.main()
