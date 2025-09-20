# 🆓 **Free Tier Deployment - PaperPathAI**

## 🎯 **Simplified Deployment (No Redis/Celery Required)**

This guide shows how to deploy PaperPathAI on Render's free tier without Redis or background workers.

### ✅ **What Works on Free Tier**
- ✅ Django backend with PostgreSQL
- ✅ Vue.js frontend
- ✅ Email notifications (synchronous)
- ✅ Admin dashboard
- ✅ Multilingual support
- ✅ All core functionality

### ❌ **What's Different**
- ❌ No background email processing (emails sent immediately)
- ❌ No periodic tasks (daily notifications)
- ❌ No Redis caching

---

## 🚀 **Step-by-Step Deployment**

### **1. Deploy Backend**

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Create Web Service**:
   - Click "New" → "Web Service"
   - Connect GitHub: `Muzamilz/PaperPathAI`
   - **Name**: `paperpathAI-backend`
   - **Root Directory**: `backend`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`

3. **Environment Variables**:
   ```bash
   DEBUG=false
   SECRET_KEY=[auto-generated]
   ALLOWED_HOSTS=*
   CELERY_TASK_ALWAYS_EAGER=true
   
   # Update after frontend deployment
   CORS_ALLOWED_ORIGINS=https://paperpathAI-frontend.onrender.com
   FRONTEND_URL=https://paperpathAI-frontend.onrender.com
   
   # Gmail Configuration
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=true
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-gmail-app-password
   DEFAULT_FROM_EMAIL=noreply@paperpathAI.com
   ```

### **2. Add PostgreSQL Database**

1. **Create Database**:
   - Dashboard → "New" → "PostgreSQL"
   - **Name**: `paperpathAI-db`
   - **Database**: `paperpathAI`
   - **User**: `paperpathAI_user`

2. **Link to Backend**: The `DATABASE_URL` will auto-link

### **3. Deploy Frontend**

1. **Create Static Site**:
   - Dashboard → "New" → "Static Site"
   - Connect same repository
   - **Name**: `paperpathAI-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm ci && npm run build`
   - **Publish Directory**: `dist`

2. **Environment Variables**:
   ```bash
   VITE_API_BASE_URL=https://paperpathAI-backend.onrender.com/api
   VITE_APP_NAME=PaperPathAI
   ```

### **4. Update Backend URLs**

After frontend deploys, update backend environment variables:
```bash
CORS_ALLOWED_ORIGINS=https://paperpathAI-frontend.onrender.com
FRONTEND_URL=https://paperpathAI-frontend.onrender.com
```

---

## 📧 **Email Setup (Gmail)**

### **1. Enable 2-Factor Authentication**
- Google Account → Security → 2-Step Verification

### **2. Generate App Password**
- Security → App passwords → Mail
- Use this password as `EMAIL_HOST_PASSWORD`

### **3. Test Emails**
- Submit a service request
- Check if confirmation email arrives
- Test admin notifications

---

## 🧪 **Testing Your Deployment**

### **Health Check**
```bash
curl https://paperpathAI-backend.onrender.com/health/
```

### **API Test**
```bash
curl https://paperpathAI-backend.onrender.com/api/services/
```

### **Frontend Test**
- Visit your frontend URL
- Switch languages (English ↔ Arabic)
- Submit a test service request
- Check admin dashboard

---

## 🎯 **Expected Results**

### ✅ **Working Features**
- **Website**: Fully functional multilingual site
- **Service Requests**: Clients can submit requests
- **Email Notifications**: Immediate email delivery
- **Admin Dashboard**: Complete request management
- **Languages**: Arabic RTL + English LTR

### 📧 **Email Flow**
1. **Client submits request** → Gets confirmation email immediately
2. **Admin gets notification** → Email sent right away
3. **Status changes** → Client gets update email instantly

### 🌐 **Your URLs**
- **Frontend**: `https://paperpathAI-frontend.onrender.com`
- **Backend**: `https://paperpathAI-backend.onrender.com`
- **Admin**: `https://paperpathAI-backend.onrender.com/admin`
- **API Docs**: `https://paperpathAI-backend.onrender.com/api/docs`

---

## 🔄 **Upgrade to Paid Tier Later**

When you're ready to upgrade:

1. **Add Redis**: For background task processing
2. **Add Background Workers**: For Celery tasks
3. **Set Environment Variable**: `CELERY_TASK_ALWAYS_EAGER=false`
4. **Deploy Workers**: Using the original `render.yaml`

The system will automatically switch to async email processing!

---

## 🐛 **Troubleshooting**

### **Build Fails**
- Check build logs in Render dashboard
- Verify `runtime.txt` has Python 3.11.9

### **Emails Not Sending**
- Verify Gmail app password
- Check email environment variables
- Look at application logs

### **Database Issues**
- Ensure PostgreSQL is linked
- Check migration logs
- Verify `DATABASE_URL` is set

### **CORS Errors**
- Update `CORS_ALLOWED_ORIGINS` with actual frontend URL
- Redeploy backend after updating

---

## 💡 **Performance Notes**

### **Free Tier Limitations**
- Services sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- 750 hours/month limit per service

### **Email Performance**
- Emails sent synchronously (slight delay on form submission)
- No retry mechanism (emails either send or fail)
- No email queue management

### **Optimization Tips**
- Keep services active with uptime monitoring
- Consider upgrading for production use
- Monitor email delivery success

---

## 🎉 **You're Done!**

Your PaperPathAI platform is now live on Render's free tier with:
- ✅ Full functionality
- ✅ Email notifications
- ✅ Multilingual support
- ✅ Admin dashboard
- ✅ Production-ready setup

**Perfect for testing, demos, and initial deployment!** 🚀