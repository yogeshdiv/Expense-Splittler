@echo off
REM Quick setup script for Windows
REM Required: Python 3.11.9

echo.
echo ===============================================
echo Expense Splitter - Backend Setup
echo Requires Python 3.11.9
echo ===============================================
echo.

REM Check Python version
python --version
echo.
echo If you don't have Python 3.11.9, install it from https://www.python.org/downloads/
echo.

REM Check if venv exists
if not exist venv (
    echo Creating virtual environment with Python 3.11.9...
    py -3.11 -m venv venv
    if errorlevel 1 (
        echo Error: Python 3.11.9 not found.
        echo Please install Python 3.11.9 from https://www.python.org/downloads/
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Creating .env file from template...
if not exist .env (
    copy .env.example .env
    echo .env file created. Please update it with your database settings.
) else (
    echo .env file already exists.
)

echo.
echo ===============================================
echo Setup Complete!
echo ===============================================
echo.
echo To start the server, run:
echo   python main.py
echo.
echo The API will be available at:
echo   http://localhost:8000
echo.
echo Swagger Docs available at:
echo   http://localhost:8000/docs
echo.
pause
