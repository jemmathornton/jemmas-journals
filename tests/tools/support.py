"""Shared bits for the tool tests (tests/tools/test_*.py): load a tool as a module, spare ports, throwaway git repos.

Nothing here touches her own files: every test works in a temp folder, and git runs with its own config (no global or
system settings, no sign-in helper), so a test can never push to GitHub or prompt for a password.
"""
import importlib.machinery, importlib.util, os, shutil, socket, subprocess, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLS = os.path.join(ROOT, 'tools')


def load(rel, name=None):
    """tools/<rel> as a fresh module (each call a new copy, so a test can change its globals freely)."""
    path = os.path.join(ROOT, rel)
    name = name or 'under_test_' + os.path.basename(rel).replace('.', '_')
    loader = importlib.machinery.SourceFileLoader(name, path)   # also loads .pyw
    spec = importlib.util.spec_from_loader(name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def free_port():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close()
    return p


class GitSandbox:
    """A temp folder plus environment settings that make git ignore her own config (name, credential helpers)."""

    def __init__(self):
        self.dir = tempfile.mkdtemp(prefix='jj-tooltest-')
        cfg = os.path.join(self.dir, 'gitconfig')
        with open(cfg, 'w', encoding='utf-8') as f:
            f.write('[user]\n\tname = Test\n\temail = test@example.invalid\n[init]\n\tdefaultBranch = main\n'
                    '[protocol "file"]\n\tallow = always\n[core]\n\tautocrlf = false\n[advice]\n\tdetachedHead = false\n')
        self.env = {'GIT_CONFIG_GLOBAL': cfg, 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_TERMINAL_PROMPT': '0', 'GCM_INTERACTIVE': 'never'}
        self.saved = {}

    def __enter__(self):
        for k, v in self.env.items():
            self.saved[k] = os.environ.get(k)
            os.environ[k] = v
        return self

    def __exit__(self, *exc):
        for k, v in self.saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(self.dir, ignore_errors=True)

    def path(self, *p):
        return os.path.join(self.dir, *p)

    def git(self, cwd, *args, check=True):
        r = subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if check and r.returncode:
            raise AssertionError(f'git {" ".join(args)} failed in {cwd}: {r.stderr or r.stdout}')
        return r.stdout.strip()

    def write(self, path, text):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)

    def repo_with_remote(self, name, files=None):
        """A bare 'GitHub' remote <name>.git and a clone <name>/ on main with one commit pushed. Returns the clone's path."""
        bare = self.path('remotes', name + '.git')
        os.makedirs(bare)
        self.git(bare, 'init', '-q', '--bare', '-b', 'main')
        work = self.path('seed-' + name)
        os.makedirs(work)
        self.git(work, 'init', '-q', '-b', 'main')
        for rel, text in (files or {'README.md': name + '\n'}).items():
            self.write(os.path.join(work, rel), text)
        self.git(work, 'add', '-A')
        self.git(work, 'commit', '-q', '-m', 'first')
        self.git(work, 'remote', 'add', 'origin', bare)
        self.git(work, 'push', '-q', '-u', 'origin', 'main')
        return work, bare
