---
description: Status of the whole family - git in the parent and every app, servers, last backup, the backup task
---
Report the state of Jemma's family of sites. Only read; change nothing, start nothing, don't fetch.

From `C:\Users\Jemma\Documents\JemmasJournals`:

1. **Git**, for the parent and each of `library`, `sim-world`, `pokedex`, `travels`: branch; `git status --short` (a count; in the parent, mention untracked `for-jemma/concepts/` screenshots separately); commits not pushed (`git rev-list --count @{u}..HEAD`); the last commit (`git log -1 --format="%h %cr %s"`); and whether the parent has recorded the app's current commit (`git ls-tree HEAD <app>` against `git -C <app> rev-parse HEAD`).
2. **Servers:** is anything answering on 8050 (family), 8020 (Library), 8030 (Pokédex), 8041 (Travels)? A quick socket check, e.g. `python -c "import socket;[print(p, socket.socket().connect_ex(('127.0.0.1',p))==0) for p in (8050,8020,8030,8041)]"`.
3. **Last backup:** the last run in `logs/weekly.log` (from its last "started" line to "finished"), with any FAILED lines.
4. **The backup task:** in PowerShell, `Get-ScheduledTask -TaskName "Jemma's Journals - backup" | Get-ScheduledTaskInfo` (last run time, last result, next run time) and its state. Result 0 is success; 267011 means it hasn't run yet.

Reply with a short table, then only what needs her attention (uncommitted work, unpushed or unrecorded commits, a server down, a failed backup), in plain British English.
