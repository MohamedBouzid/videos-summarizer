@echo off
echo Starting Video Summarizer Application...
echo.
start /B ollama serve
echo Starting Python Backend...
start "Video Summarizer Backend" cmd /k "cd backend && python api.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo Starting React Frontend...
start "Video Summarizer Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo Video Summarizer is starting...
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
echo ========================================
pause > nul
