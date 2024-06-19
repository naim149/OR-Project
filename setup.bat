@echo off
echo Removing existing virtual environment if it exists...
if exist venv (
    rmdir /s /q venv
)

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip and setuptools...
pip install --upgrade pip setuptools==57.5.0

echo Installing requirements...
pip install -r requirements.txt

pause
