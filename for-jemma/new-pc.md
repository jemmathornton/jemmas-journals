# Setting up the sites on a new (or rebuilt) PC

Everything lives on GitHub, so nothing is lost if this PC dies. Your ticks and books are backed up daily, as are Travels posts. To get going again:

1. **Install** these, if they're missing:
   - Python 3.13, from python.org. Tick “Add to PATH”.
   - Pillow, by running `python -m pip install pillow` in a terminal.
   - Git.
   - The GitHub CLI.
2. **Sign in to GitHub**: run `gh auth login` and follow the steps. This is the sign-in the backups use, so there are no popups.
3. **Get the sites**, in a terminal inside your Documents folder:
   ```
   git clone --recurse-submodules https://github.com/jemmathornton/jemmas-journals.git JemmasJournals
   ```
   Then put each site on its `main` branch (they start “detached”, and the backups only save from `main`):
   ```
   cd JemmasJournals
   git submodule foreach git checkout main
   ```
4. **Set everything up**: run this inside the `JemmasJournals` folder:
   ```
   powershell -ExecutionPolicy Bypass -File tools\setup_pc.ps1
   ```
   It makes the daily backup, the server that starts when you log in, and the Library, Sim World and Pokédex shortcuts, then starts everything.
5. **Only for running the checks (optional)**:
   - Put a portable Node in `JemmasJournals\.tools\node`.
   - Then run `.tools\node\npm.cmd install` to fetch Playwright and axe-core.

Things that aren't on GitHub on purpose, so copy them across yourself if you want them:
- The Library’s phone-scanning key (`%LOCALAPPDATA%\Jemmas Library\scan-key.txt`; a new one is made by itself) and `library/data/scanned.json`.
- Logs.
- Your Sims save files and Pictures (outside these projects).
