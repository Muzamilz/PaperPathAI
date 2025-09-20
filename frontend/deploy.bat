@echo off
REM Frontend Deployment Script for PaperPathAI (Windows)
echo 🚀 Deploying PaperPathAI Frontend...

REM Check if we're in the frontend directory
if not exist "package.json" (
    echo ❌ Error: Please run this script from the frontend directory
    exit /b 1
)

REM Install dependencies
echo 📦 Installing dependencies...
npm ci

REM Build the project
echo 🔨 Building project...
npm run build

REM Check if build was successful
if %errorlevel% equ 0 (
    echo ✅ Build successful!
    echo 📁 Build files are in the 'dist' directory
    echo.
    echo 🔗 Next steps:
    echo 1. Deploy to Render using the dashboard or CLI
    echo 2. Set environment variables in Render:
    echo    - VITE_API_BASE_URL=https://paperpathai.onrender.com/api
    echo    - VITE_APP_NAME=PaperPathAI
    echo 3. Update backend CORS_ALLOWED_ORIGINS with your frontend URL
    echo.
    echo 🎉 Ready for deployment!
) else (
    echo ❌ Build failed. Please check the errors above.
    exit /b 1
)

pause