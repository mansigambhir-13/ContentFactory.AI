@echo off
echo ?? Setting up AI Social Media Content Engine...
echo.

echo ?? Creating virtual environment...
python -m venv venv

echo ? Activating virtual environment...
call venv\Scripts\activate.bat

echo ?? Installing requirements...
pip install -r requirements.txt

echo.
echo ? Setup complete!
echo.
echo Next steps:
echo   1. Add your OPENAI_API_KEY to the .env file
echo   2. Run: run_engine.bat
echo.
pause
