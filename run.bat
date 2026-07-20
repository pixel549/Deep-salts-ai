@echo off
setlocal enabledelayedexpansion
cd /d %~dp0

rem --- Load a saved key from .env if we don't already have one this session ---
if not defined GEMINI_API_KEY (
  if exist .env (
    for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
      if /i "%%A"=="GEMINI_API_KEY" set "GEMINI_API_KEY=%%B"
    )
  )
)

rem --- Still nothing? Ask once, offer to remember it for next time ---
if not defined GEMINI_API_KEY (
  echo No GEMINI_API_KEY found.
  set /p GEMINI_API_KEY="Paste your Gemini API key: "
  if not defined GEMINI_API_KEY (
    echo No key entered -- can't continue.
    pause
    exit /b 1
  )
  set /p SAVE_KEY="Save it to .env so you don't have to paste it again? (y/n): "
  if /i "!SAVE_KEY!"=="y" (
    echo GEMINI_API_KEY=!GEMINI_API_KEY!> .env
    echo Saved to .env -- this file is already in .gitignore, it will never be committed.
  )
)

:menu
echo.
echo ============================
echo   Deep Salts AI - Run Menu
echo ============================
echo  1. Run one turn
echo  2. Run end-of-session review
echo  3. Exit
echo.
set /p CHOICE="Choose an option (1-3): "

if "%CHOICE%"=="1" (
  python -m orchestrator.main turn
  echo.
  pause
  goto menu
)
if "%CHOICE%"=="2" (
  python -m orchestrator.main end-session
  echo.
  pause
  goto menu
)
if "%CHOICE%"=="3" (
  exit /b 0
)

echo Invalid choice, try again.
goto menu
