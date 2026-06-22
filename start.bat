@echo off
echo ========================================
echo    SmartReview - Demarrage...
echo ========================================
echo.

start "SmartReview Backend" cmd /k "cd /d "%~dp0backend" && py -3.11 -m uvicorn main:app --reload --port 8001"

timeout /t 3 /nobreak > nul

start "SmartReview Frontend" cmd /k "cd /d "%~dp0" && py -3.11 server.py"

timeout /t 2 /nobreak > nul

start chrome http://localhost:3000

echo.
echo SmartReview est ouvert dans Chrome !
echo Backend  : http://localhost:8001
echo Frontend : http://localhost:3000
echo.
pause
