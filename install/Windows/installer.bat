@echo off
setlocal

rem Check if Python is already installed
python --version > nul 2>&1
if %errorlevel% equ 0 (
    echo Python is already installed.
    goto :check_dependencies
)

rem Download and install Python (adjust version and URL as needed)
set "pythonVersion=3.9.7"
set "pythonUrl=https://www.python.org/ftp/python/%pythonVersion%/python-%pythonVersion%-amd64.exe"
set "pythonInstaller=python-installer.exe"

echo Installing Python...
curl -o %pythonInstaller% %pythonUrl%
start /wait %pythonInstaller% /quiet PrependPath=1
del %pythonInstaller%

echo Python has been installed.

rem Refresh environment variables
for /f "usebackq tokens=*" %%a in (`"reg query HKCU\Environment /v PATH"`) do (
    setx PATH "%%~nxa" /m >nul
)

:check_dependencies

rem Check if PyQt5 is installed
python -c "import PyQt5.QtWidgets" > nul 2>&1
if %errorlevel% equ 0 (
    echo PyQt5 is already installed.
    goto :check_pyinstaller
)

echo Installing PyQt5...
pip --default-timeout=1000 install PyQt5

:check_pyinstaller

rem Check if PyInstaller is installed
pyinstaller --version > nul 2>&1
if %errorlevel% equ 0 (
    echo PyInstaller is already installed.
    goto :create_executable
)

echo Installing PyInstaller...
pip --default-timeout=1000 install pyinstaller

:create_executable

echo Creating executable using PyInstaller...
pyinstaller ..\..\src\main.py --onefile

echo Executable created.

rem Copy executable to desktop
set "desktopPath=%userprofile%\Desktop"
copy dist\main.exe "%desktopPath%\JDaily.exe" > nul

echo Executable copied to desktop.

:end
endlocal
