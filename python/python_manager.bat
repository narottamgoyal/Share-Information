@echo off
setlocal enabledelayedexpansion
title Ultimate Python and Ollama Manager - Secured Edition

:MAIN_MENU
cls
echo =====================================================================
echo          PYTHON AND OLLAMA ENVIRONMENT MANAGER FOR WINDOWS
echo =====================================================================

:: --- 1. DETECT INSTALLED PYTHON VERSIONS ---
echo CURRENTLY INSTALLED PYTHON VERSIONS:
set /a py_count=0
where python >nul 2>nul
if %errorlevel% equ 0 (
    python --version > "%temp%\py_check.txt" 2>&1
    set /p py_val=<"%temp%\py_check.txt"
    del "%temp%\py_check.txt"
    echo !py_val! | findstr /i "Python 3." >nul
    if !errorlevel! equ 0 (
        echo     - Default System Python: !py_val!
        set /a py_count+=1
    )
)
if exist "%LocalAppData%\Programs\Python" (
    for /d %%d in ("%LocalAppData%\Programs\Python\Python*") do (
        set "folder=%%~nxd"
        echo     - Local User Path: !folder:~6,1!.!folder:~7!
        set /a py_count+=1
    )
)
if exist "%ProgramFiles%\Python*" (
    for /d %%d in ("%ProgramFiles%\Python*") do (
        echo     - System Program Files: %%~nxd
        set /a py_count+=1
    )
)
if %py_count% equ 0 (
    echo     [-] No working Python installations detected on your system PATH.
)
echo ---------------------------------------------------------------------

:: --- 2. MAIN MENU ---
echo MAIN MENU:
echo     1. Install Python Engine
echo     2. Manage Virtual Environments (venv)
echo     3. Manage Dependencies (requirements.txt)
echo     4. Manage Ollama and AI Models
echo     5. Exit
echo ---------------------------------------------------------------------

set "main_choice=1"
set /p main_choice="Choose an option (1-5) [Default: 1]: "

if "%main_choice%"=="1" goto SUB_INSTALL_PY
if "%main_choice%"=="2" goto SUB_VENV
if "%main_choice%"=="3" goto SUB_REQS
if "%main_choice%"=="4" goto SUB_OLLAMA
if "%main_choice%"=="5" exit /b
goto MAIN_MENU


:: =====================================================================
:: 1. SUBMENU: INSTALL PYTHON
:: =====================================================================
:SUB_INSTALL_PY
cls
echo =====================================================================
echo                      INSTALL PYTHON ENGINE
echo =====================================================================
echo Choose which version to install globally via WinGet:
echo     1. Python 3.12 (Recommended for AI)
echo     2. Python 3.11
echo     3. Custom Version (Specify exact version string)
echo     4. Back to Main Menu
echo ---------------------------------------------------------------------
set "py_choice=1"
set /p py_choice="Choose an option (1-4) [Default: 1]: "

if "%py_choice%"=="1" (
    echo. & echo Installing Python 3.12 via WinGet...
    winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    echo. & pause & goto SUB_INSTALL_PY
)
if "%py_choice%"=="2" (
    echo. & echo Installing Python 3.11 via WinGet...
    winget install -e --id Python.Python.3.11 --accept-package-agreements --accept-source-agreements
    echo. & pause & goto SUB_INSTALL_PY
)
if "%py_choice%"=="3" (
    echo.
    set "cust_ver=3.12.3"
    set /p cust_ver="Enter exact version string [Default: 3.12.3]: "
    echo Installing Python !cust_ver! via WinGet...
    winget install -e --id Python.Python.3.!cust_ver:~0,4! --version !cust_ver! --accept-package-agreements --accept-source-agreements
    echo. & pause & goto SUB_INSTALL_PY
)
if "%py_choice%"=="4" goto MAIN_MENU
goto SUB_INSTALL_PY


:: =====================================================================
:: 2. SUBMENU: VIRTUAL ENVIRONMENTS (SAFEGUARDED)
:: =====================================================================
:SUB_VENV
cls
echo =====================================================================
echo                  MANAGE VIRTUAL ENVIRONMENTS (VENV)
echo =====================================================================
echo Actions:
echo     1. Setup / Recreate Virtual Env (Current Folder)
echo     2. Setup / Recreate Virtual Env (Custom Folder Path)
echo     3. Activate Virtual Env (Current Folder)
echo     4. Activate Virtual Env (Custom Folder Path)
echo     5. Back to Main Menu
echo ---------------------------------------------------------------------
set "venv_choice=1"
set /p venv_choice="Choose an option (1-5) [Default: 1]: "

if "%venv_choice%"=="1" (
    echo.
    if exist ".venv" (
        echo [!] Warning: A folder named '.venv' already exists in the current directory.
        set "confirm=N"
        set /p confirm="Do you want to permanently DELETE and recreate it? (Y/N) [Default: N]: "
        if /i not "!confirm!"=="Y" (
            echo [-] Aborted. No files were deleted.
            echo. & pause & goto SUB_VENV
        )
        echo Removing existing environment...
        rmdir /s /q .venv
    )
    echo Setting up venv named '.venv' in current folder...
    python -m venv .venv
    echo [+] Virtual environment '.venv' created successfully.
    echo. & pause & goto SUB_VENV
)

if "%venv_choice%"=="2" (
    echo.
    set "vpath=%cd%"
    set /p vpath="Enter full destination path [Default: Current Folder]: "
    set "vname=.venv"
    set /p vname="Enter a name for the venv folder [Default: .venv]: "
    
    if exist "!vpath!\!vname!" (
        echo.
        echo [!] DANGER: The target folder "!vpath!\!vname!" already exists.
        set "confirm=N"
        set /p confirm="Do you want to permanently DELETE everything inside it? (Y/N) [Default: N]: "
        if /i not "!confirm!"=="Y" (
            echo [-] Aborted. No files were deleted.
            echo. & pause & goto SUB_VENV
        )
        echo Removing target directory...
        rmdir /s /q "!vpath!\!vname!"
    )
    python -m venv "!vpath!\!vname!"
    echo [+] Virtual environment created successfully at "!vpath!\!vname!".
    echo. & pause & goto SUB_VENV
)

if "%venv_choice%"=="3" (
    echo.
    if not exist ".venv\Scripts\activate.bat" (
        echo [-] Error: Virtual environment '.venv' does not exist here.
    ) else (
        echo Spawning environment in a new terminal window...
        start cmd /k ".venv\Scripts\activate.bat"
    )
    echo. & pause & goto SUB_VENV
)

if "%venv_choice%"=="4" (
    echo.
    set "apath=%cd%"
    set /p apath="Enter the full folder path [Default: Current Folder]: "
    set "aname=.venv"
    set /p aname="Enter the venv folder name [Default: .venv]: "
    
    if not exist "!apath!\!aname!\Scripts\activate.bat" (
        echo [-] Error: Activation script not found at "!apath!\!aname!\Scripts\activate.bat"
    ) else (
        echo Spawning environment in a new terminal window...
        start cmd /k "!apath!\!aname!\Scripts\activate.bat"
    )
    echo. & pause & goto SUB_VENV
)
if "%venv_choice%"=="5" goto MAIN_MENU
goto SUB_VENV


:: =====================================================================
:: 3. SUBMENU: DEPENDENCIES (SAFEGUARDED OVERWRITES)
:: =====================================================================
:SUB_REQS
cls
echo =====================================================================
echo                 MANAGE DEPENDENCIES (REQUIREMENTS.TXT)
echo =====================================================================
echo Actions:
echo     1. Install from requirements.txt (Current Folder)
echo     2. Install from requirements.txt (Custom Folder Path)
echo     3. Automatically update/generate requirements.txt (pip freeze)
echo     4. Back to Main Menu
echo ---------------------------------------------------------------------
set "reqs_choice=1"
set /p reqs_choice="Choose an option (1-4) [Default: 1]: "

if "%reqs_choice%"=="1" (
    echo.
    if not exist "requirements.txt" (
        echo [-] Error: requirements.txt not found in the current folder.
    ) else (
        echo Installing requirements in current folder...
        python -m pip install -r requirements.txt
    )
    echo. & pause & goto SUB_REQS
)
if "%reqs_choice%"=="2" (
    echo.
    set "rpath=%cd%"
    set /p rpath="Enter full path where requirements.txt lives [Default: Current Folder]: "
    if not exist "!rpath!\requirements.txt" (
        echo [-] Error: requirements.txt not found at "!rpath!\requirements.txt".
    ) else (
        echo Installing requirements from custom folder...
        python -m pip install -r "!rpath!\requirements.txt"
    )
    echo. & pause & goto SUB_REQS
)
if "%reqs_choice%"=="3" (
    echo.
    if exist "requirements.txt" (
        echo [!] Warning: A 'requirements.txt' file already exists here.
        set "confirm=N"
        set /p confirm="Do you want to overwrite it? (Y/N) [Default: N]: "
        if /i not "!confirm!"=="Y" (
            echo [-] Aborted. File was not changed.
            echo. & pause & goto SUB_REQS
        )
    )
    echo Generating/Updating requirements.txt via pip freeze...
    python -m pip freeze > requirements.txt
    echo [+] Current folder's requirements.txt updated!
    echo. & pause & goto SUB_REQS
)
if "%reqs_choice%"=="4" goto MAIN_MENU
goto SUB_REQS


:: =====================================================================
:: 4. SUBMENU: OLLAMA AND MODELS
:: =====================================================================
:SUB_OLLAMA
cls
echo =====================================================================
echo                      MANAGE OLLAMA AND AI MODELS
echo =====================================================================
echo Actions:
echo     1. Install Ollama Engine (Official PowerShell Script)
echo     2. Check Ollama Server Status and List Downloaded Models
echo     3. Open Ollama Model Download Menu
echo     4. Back to Main Menu
echo ---------------------------------------------------------------------
set "ollama_choice=2"
set /p ollama_choice="Choose an option (1-4) [Default: 2]: "

if "%ollama_choice%"=="1" (
echo. & echo Executing official Ollama installation script...
powershell -Command "irm ollama.com | iex"
echo. & pause & goto SUB_OLLAMA
)
if "%ollama_choice%"=="2" (
echo. & echo Checking Ollama Server Status...
powershell -Command "$resp = Invoke-WebRequest -Uri '127.0.0' -UseBasicParsing -ErrorAction SilentlyContinue; if ($resp.StatusCode -eq 200) { Write-Output '[+] Ollama server status: RUNNING' } else { Write-Output '[-] Ollama server status: NOT RUNNING' }"
echo. & echo Currently Downloaded Models:
ollama list 2>nul
if %errorlevel% neq 0 echo Warning: Could not retrieve model list. Ensure Ollama is running.
echo. & pause & goto SUB_OLLAMA
)
if "%ollama_choice%"=="3" goto OLLAMA_MODELS_MENU
if "%ollama_choice%"=="4" goto MAIN_MENU
goto SUB_OLLAMA
:: =====================================================================
:: OLLAMA MODEL DOWNLOAD MENU
:: =====================================================================
:OLLAMA_MODELS_MENU
cls
echo =====================================================================
echo                      OLLAMA MODEL DOWNLOAD MENU
echo =====================================================================
echo Choose a popular model to pull, or enter a custom name:
echo     1. Llama 3 (8B)      - General purpose, highly smart
echo     2. Phi 3 (3.8B)      - Lightweight, fast, Microsoft-built
echo     3. Mistral (7B)      - Great balance of speed and reasoning
echo     4. Gemma 2 (9B)      - Powerful Google model
echo     5. Codegemma (7B)    - Optimized for programming
echo     6. Custom            - Enter any other model from ollama.com
echo     7. Back to Ollama Menu
echo ---------------------------------------------------------------------
set "model_choice=1"
set /p model_choice="Choose an option (1-7) [Default: 1]: "
set "mname="
if "%model_choice%"=="1" set "mname=llama3"
if "%model_choice%"=="2" set "mname=phi3"
if "%model_choice%"=="3" set "mname=mistral"
if "%model_choice%"=="4" set "mname=gemma2"
if "%model_choice%"=="5" set "mname=codegemma"
if "%model_choice%"=="6" (
echo.
set "mname=llama3"
set /p mname="Enter exact model name from ollama.com [Default: llama3]: "
)
if "%model_choice%"=="7" goto SUB_OLLAMA
if defined mname (
echo. & echo Pulling model: !mname! ...
ollama pull !mname!
echo. & pause
)
goto OLLAMA_MODELS_MENU