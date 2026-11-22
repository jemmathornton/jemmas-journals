# Jemma's Journals: set up a PC (new, rebuilt, or after something went missing). Safe to run again: it replaces its own items.
#
#   powershell -ExecutionPolicy Bypass -File tools\setup_pc.ps1
#
# Makes (for the signed-in user, no admin needed):
#   - the daily backup task  "Jemma's Journals - backup"  (09:30 every day, catches up after; tools/weekly.py)
#   - the Startup item       "Jemma's Journals server"    (tools/serve_all.py: the family at http://localhost:8050)
#   - Desktop and Start-menu shortcuts: Jemma's Library, Jemma's Sim World, Jemma's Pokédex (tools/open_site.pyw)
# Needs: Python 3.13 (with Pillow), Git, the GitHub CLI signed in (gh auth login), and this folder cloned with
# --recurse-submodules. See for-jemma/new-pc.md.
$ErrorActionPreference = 'Stop'
$jj = Split-Path -Parent $PSScriptRoot
# Python: the python.org install for this user first (newest Python3*), then the py launcher's. Never the Windows Store
# alias in WindowsApps (it isn't a real Python and has no pythonw.exe).
$pyw = Get-ChildItem "$env:LOCALAPPDATA\Programs\Python\Python3*\pythonw.exe" -ErrorAction SilentlyContinue |
  Sort-Object { [int]($_.Directory.Name -replace '\D','') } -Descending | Select-Object -First 1 -ExpandProperty FullName
if (-not $pyw -and (Get-Command py.exe -ErrorAction SilentlyContinue)) {
  $exe = (& py.exe -3 -c "import sys; print(sys.executable)" 2>$null | Select-Object -First 1)
  if ($exe -and $exe -notmatch '\\WindowsApps\\') { $cand = Join-Path (Split-Path $exe) 'pythonw.exe'; if (Test-Path $cand) { $pyw = $cand } }
}
if (-not $pyw) { throw "Python not found. Install Python 3.13 from python.org (for this user), then run this again. (The Microsoft Store 'python' shortcut doesn't count.)" }
"pythonw: $pyw"
foreach ($app in 'library','sim-world','pokedex','travels') { if (-not (Test-Path "$jj\$app\site")) { throw "$app is missing: clone with --recurse-submodules (or run: git submodule update --init)" } }

# the daily backup task (2-hour limit: on Sundays the jobs' own limits add up to well over an hour)
$a = New-ScheduledTaskAction -Execute $pyw -Argument "`"$jj\tools\weekly.py`"" -WorkingDirectory $jj
$t = New-ScheduledTaskTrigger -Daily -At 09:30
$s = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 2) -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew
$p = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName "Jemma's Journals - backup" -Action $a -Trigger $t -Settings $s -Principal $p -Force `
  -Description "Every day: back up the Library, Pokédex and Travels to GitHub; Sundays also Sim World's Gallery refresh; then record the apps' versions (tools/weekly.py)." | Out-Null
"task: Jemma's Journals - backup (daily 09:30)"

# shortcuts
$sh = New-Object -ComObject WScript.Shell
function New-JJShortcut($path, $target, $arguments, $icon, $desc) {
  $l = $sh.CreateShortcut($path); $l.TargetPath = $target; $l.Arguments = $arguments; $l.WorkingDirectory = $jj
  if ($icon -and (Test-Path ($icon -replace ',\d+$',''))) { $l.IconLocation = $icon }
  $l.Description = $desc; $l.Save(); "shortcut: $path"
}
$startup = [Environment]::GetFolderPath('Startup')
New-JJShortcut "$startup\Jemma's Journals server.lnk" $pyw "`"$jj\tools\serve_all.py`"" "$jj\site\favicon.ico,0" "Jemma's Journals and every app at http://localhost:8050"
$apps = @(
  @{ name = "Jemma's Library";  site = 'library';   icon = "$jj\library\site\app-v2.ico,0" },
  @{ name = "Jemma's Sim World"; site = 'sim-world'; icon = "$jj\sim-world\site\icon.ico,0" },
  @{ name = "Jemma’s Pokédex";  site = 'pokedex';   icon = "$jj\pokedex\site\app-v1.ico,0" }
)
foreach ($dir in [Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('Programs')) {
  foreach ($x in $apps) { New-JJShortcut "$dir\$($x.name).lnk" $pyw "`"$jj\tools\open_site.pyw`" $($x.site)" $x.icon "Open $($x.name)" }
}

# start the family now
if (-not (Test-NetConnection 127.0.0.1 -Port 8050 -InformationLevel Quiet -WarningAction SilentlyContinue)) { Start-Process explorer.exe -ArgumentList "`"$startup\Jemma's Journals server.lnk`"" }
"done: open any shortcut, or http://localhost:8050"
