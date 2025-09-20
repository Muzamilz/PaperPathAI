#!/bin/bash

# Frontend Deployment Script for PaperPathAI
echo "🚀 Deploying PaperPathAI Frontend..."

# Check if we're in the frontend directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the frontend directory"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm ci

# Build the project
echo "🔨 Building project..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "📁 Build files are in the 'dist' directory"
    echo ""
    echo "🔗 Next steps:"
    echo "1. Deploy to Render using the dashboard or CLI"
    echo "2. Set environment variables in Render:"
    echo "   - VITE_API_BASE_URL=https://paperpathai.onrender.com/api"
    echo "   - VITE_APP_NAME=PaperPathAI"
    echo "3. Update backend CORS_ALLOWED_ORIGINS with your frontend URL"
    echo ""
    echo "🎉 Ready for deployment!"
else
    echo "❌ Build failed. Please check the errors above."
    exit 1
fi