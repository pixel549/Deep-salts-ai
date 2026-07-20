@echo off
cd /d %~dp0
echo Installing dependencies (only needs to be run once, or after requirements.txt changes)...
python -m pip install -r requirements.txt
echo.
echo Done. Run run.bat whenever you want to play.
pause
