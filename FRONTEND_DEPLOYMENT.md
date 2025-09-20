# Frontend Deployment Guide

## 🎯 **Frontend Configuration Complete**

Your frontend has been configured to connect to your working backend at:
**https://paperpathai.onrender.com**

## 📋 **Configuration Changes Made**

### 1. **Environment Variables Updated**
- ✅ **Production**: `VITE_API_BASE_URL=https://paperpathai.onrender.com/api`
- ✅ **Development**: Updated app name to PaperPathAI
- ✅ **Render Config**: Updated service name and API URL

### 2. **Files Modified**
- ✅ `frontend/.env.production` - Updated API URL and app name
- ✅ `frontend/.env.development` - Updated app name
- ✅ `frontend/render.yaml` - Updated service name and environment variables

## 🚀 **Deploy Your Frontend**

### **Option 1: Deploy via Render Dashboard**
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `paperpathai-frontend`
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm ci && npm run build`
   - **Start Command**: `npm run preview -- --host 0.0.0.0 --port $PORT`

### **Option 2: Deploy via Render CLI**
```bash
# Navigate to frontend directory
cd frontend

# Deploy using render.yaml
render deploy
```

## 🔧 **Environment Variables to Set in Render**

In your Render service dashboard, add these environment variables:

```bash
NODE_VERSION=18.17.0
VITE_API_BASE_URL=https://paperpathai.onrender.com/api
VITE_APP_NAME=PaperPathAI
VITE_APP_DESCRIPTION=Professional student services platform
```

## 🔗 **Backend CORS Configuration**

Your backend needs to allow your frontend domain. Add these environment variables to your **backend** service in Render:

```bash
CORS_ALLOWED_ORIGINS=https://paperpathai-frontend1.onrender.com
FRONTEND_URL=https://paperpathai-frontend1.onrender.com
```

**✅ Your frontend is deployed at: https://paperpathai-frontend1.onrender.com**

## 🧪 **Testing After Deployment**

### 1. **Frontend Health Check**
- Visit your frontend URL
- Check browser console for errors
- Verify API calls are going to `https://paperpathai.onrender.com/api`

### 2. **API Connection Test**
- Open browser dev tools → Network tab
- Navigate through your app
- Verify API calls return status 200
- Check for CORS errors

### 3. **Features to Test**
- ✅ Home page loads
- ✅ Services display correctly
- ✅ Contact form submission
- ✅ Admin login (if implemented)
- ✅ Language switching

## 🔍 **Troubleshooting**

### **CORS Errors**
If you see CORS errors:
1. Update backend `CORS_ALLOWED_ORIGINS` with your frontend URL
2. Redeploy backend service
3. Clear browser cache

### **API Connection Issues**
1. Check `VITE_API_BASE_URL` in Render environment variables
2. Verify backend is responding at `/api/` endpoints
3. Check network tab for failed requests

### **Build Failures**
1. Ensure Node.js version is 18.17.0
2. Check for missing dependencies
3. Verify build command: `npm ci && npm run build`

## 📱 **Expected Frontend URLs**

Once deployed, your frontend will be available at:
- **Production**: `https://paperpathai-frontend.onrender.com` (or similar)
- **API Endpoint**: `https://paperpathai.onrender.com/api`

## 🎉 **Next Steps**

1. **Deploy Frontend** using one of the methods above
2. **Update Backend CORS** with your frontend URL
3. **Test Full Integration** between frontend and backend
4. **Monitor Logs** for any issues

Your backend is already working perfectly! Once the frontend is deployed and CORS is configured, your full-stack application will be live! 🚀