---
description: Run every site's tests and the family git checks (tools/check_all.py), then summarise
argument-hint: "[full]  (default: --quick)"
---
Run the family checks from `C:\Users\Jemma\Documents\JemmasJournals`.

- If the argument is `full`, run `python -B -X utf8 tools/check_all.py` (about 20 minutes: run it in the background and wait to be told it has finished). Otherwise run `python -B -X utf8 tools/check_all.py --quick` (a few minutes: home, the family rules, the tool tests, accessibility and git; skips the four apps' own suites).
- It starts its own test copy of the family server on a spare port (for the family rules and accessibility), so her 8050 server isn't needed and isn't touched.
- The checks only read. Never "fix" a failure by changing her data (Pokédex ticks, Library data, Travels posts).

Argument: $ARGUMENTS

Then reply in short, plain British English:
1. One line per check: ok or failed, with its time.
2. For each failure, the relevant lines from its log in `logs/check-all/` and the likely cause. Don't fix anything unless asked.
3. The accessibility note (`logs/check-all/axe.txt`), and any app that is not clean, not pushed or not recorded in the parent.
