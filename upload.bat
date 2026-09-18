@echo off
cd /d "%~dp0"
echo Uploading to GitHub (dxkalee/WahFungWeb)...
git add -A
git status
set /p msg=Commit message (Enter for "Update site"): 
if "%msg%"=="" set msg=Update site
git commit -m "%msg%"
if errorlevel 1 (
  echo Nothing to commit, or commit failed.
) else (
  git push origin main
)
pause
