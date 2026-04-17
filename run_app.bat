@echo off
cd /d %~dp0

where py >nul 2>&1
if %errorlevel%==0 (
  py launch_voice_memo.py
  goto end
)

where python >nul 2>&1
if %errorlevel%==0 (
  python launch_voice_memo.py
  goto end
)

echo Python was not found on this computer.
echo Please install Python 3 and run this file again.
pause
exit /b 1

:end
if errorlevel 1 (
  echo.
  echo App exited with an error.
  pause
)
