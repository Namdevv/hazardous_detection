@echo off
color 0A
title Git Push Automation
cls

:menu
echo ====================================
echo    Git Push Automation Script
echo ====================================
echo.
echo 1. Check status
echo 2. Add and commit changes and Push
echo 3. Push to remote
echo 4. Pull from remote
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto status
if "%choice%"=="2" goto addcommit
if "%choice%"=="3" goto push
if "%choice%"=="4" goto pull
if "%choice%"=="5" goto end

:status
cls
echo ====================================
echo    Checking Git Status
echo ====================================
git status
echo.
pause
goto menu

:addcommit
cls
echo =========================================
echo    Adding and Committing Changes -> Push
echo =========================================
git add .
set /p commit_msg="Enter commit message: "
git commit -m "%commit_msg%"
git push
echo.
pause
goto menu

:pull
cls
echo ====================================
echo    Pulling from Remote Repository
echo ====================================
git pull
echo.
pause
goto menu

:end
echo ====================================
echo    Thank you for using Git Push Automation!
echo ====================================
pause
exit