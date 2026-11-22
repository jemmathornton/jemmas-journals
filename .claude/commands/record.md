---
description: Record each app's current version in the parent (tools/record_apps.py) and report
---
In `C:\Users\Jemma\Documents\JemmasJournals`, run `python -X utf8 tools/record_apps.py`.

It records every app (library, sim-world, pokedex, travels) that is on `main`, has nothing uncommitted and is pushed: it commits "Record app versions: …" in the parent and pushes with the GitHub CLI sign-in. It touches nothing else in the parent.

Report in one or two plain lines: which apps were recorded and the new parent commit (`git log --oneline -1`), or "nothing new". For any app it skipped, say why (uncommitted, not on main, not pushed) and show its `git status --short`, but don't commit or push in that app yourself: another session may be working there. Ask her first.
