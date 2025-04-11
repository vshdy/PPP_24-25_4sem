@echo off

REM 
cd /d C:\Users\user\Desktop\projectt

REM 
powershell -Command "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass"

REM 
call venv\Scripts\activate.bat

REM 
start cmd /k "redis-server"

REM 
start cmd /k "cd /d C:\Users\user\Desktop\projectt && call venv\Scripts\activate.bat && celery -A app.services.task_service worker --loglevel=DEBUG --pool=solo"

REM 
start cmd /k "cd /d C:\Users\user\Desktop\projectt && call venv\Scripts\activate.bat && uvicorn main:app --reload"

echo Всё запущено
pause
