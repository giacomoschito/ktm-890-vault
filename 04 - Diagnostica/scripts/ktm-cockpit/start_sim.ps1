$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$here\.venv\Scripts\python.exe" -m app.simulator
