@echo off
cd /d %~dp0
python launch_voice_memo.py
if errorlevel 1 (
  echo.
  echo App exited with an error.
  pause
)
