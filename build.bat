@echo off
REM build.bat — build a one-file Windows exe using PyInstaller
REM Usage: open cmd in this folder and run: build.bat




















)  echo PyInstaller failed. Try building without --windowed to see console errors.) else (  echo Build complete. Output: dist\screener.exeif %errorlevel% equ 0 (python -m PyInstaller --onefile --windowed --name screener screener.pyecho Running PyInstaller...python -m pip install --upgrade pyinstallerpython -m pip install -r requirements.txtpython -m pip install --upgrade pipecho Installing/ensuring dependencies...)  exit /b 1  echo Python not found in PATH. Install Python 3.8+ and retry.if %errorlevel% neq 0 (python --version >nul 2>&1@echo Checking Python...