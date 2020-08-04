@echo off

start cmd /k "cd venv\Scripts & activate & cd ..\.. & start chrome.exe http://127.0.0.1:5000/ & SET PYTHONPATH=. & python -m app.main"

rem call venv/Scripts/activate.bat set PYTHONPATH=. python -m app.main start chrome.exe http://127.0.0.1:5000/