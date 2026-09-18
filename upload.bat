@echo off
cd /d "%~dp0"
echo Uploading to GitHub (dxkalee/WahFungWeb)...
git add -A
git status
git diff --cached --quiet
if %errorlevel%==0 (
  echo.
  echo Nothing new to upload. GitHub is already up to date.
  echo You can close this window.
  pause
  exit /b 0
)
set /p msg=Commit message (Enter for "Update site"): 
if "%msg%"=="" set msg=Update site
git commit -m "%msg%"
if errorlevel 1 (
  echo Commit failed.
  pause
  exit /b 1
)
git push origin main
pause
