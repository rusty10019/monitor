@echo off
echo ========================================
echo   PUSH TO GITHUB
echo ========================================
echo.
echo Repo: https://github.com/rusty10019/monitor.git
echo.
echo This will push ONLY essential files:
echo   - dist/ (encrypted script)
echo   - README.md
echo   - requirements.txt
echo   - cookies_template.txt
echo   - .gitignore
echo.
pause
echo.

echo Initializing git...
git init

echo.
echo Adding files...
git add .

echo.
echo Committing...
git commit -m "Encrypted SHEIN monitor - minimal version"

echo.
echo Connecting to GitHub...
git remote add origin https://github.com/rusty10019/monitor.git

echo.
echo Setting main branch...
git branch -M main

echo.
echo Pushing to GitHub...
echo.
echo When prompted for password, use your GitHub token
echo.
git push -u origin main --force

echo.
echo ========================================
echo   DONE!
echo ========================================
echo.
echo Your repo is live at:
echo https://github.com/rusty10019/monitor
echo.
echo Share this link with users!
echo.
pause
