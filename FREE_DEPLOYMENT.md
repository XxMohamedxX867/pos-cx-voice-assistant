# 🆓 Free Deployment Guide - POS CX Voice Assistant

## 🎯 **Quick & Free Deployment on Render**

This guide will help you deploy your custom LLM to Render's free tier for testing.

## 📋 **Prerequisites**

✅ **GitHub Account** - Free account needed  
✅ **Render Account** - Free account needed  
✅ **Your Code** - Already prepared and committed  

## 🚀 **Step-by-Step Deployment**

### Step 1: Create GitHub Repository

1. **Go to GitHub.com** and sign in
2. **Click "New repository"** (green button)
3. **Repository name**: `pos-cx-voice-assistant`
4. **Make it Public** (free tier requirement)
5. **Don't initialize** with README (we already have one)
6. **Click "Create repository"**

### Step 2: Push Your Code to GitHub

Run these commands in your project folder:

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/pos-cx-voice-assistant.git

# Push your code
git push -u origin master
```

**Replace `YOUR_USERNAME` with your actual GitHub username**

### Step 3: Deploy on Render

1. **Go to [render.com](https://render.com)**
2. **Sign up with GitHub** (use your GitHub account)
3. **Click "New +"** → **"Web Service"**
4. **Connect your GitHub repository**:
   - Select your `pos-cx-voice-assistant` repository
   - Click "Connect"

### Step 4: Configure Your Service

Fill in these settings:

- **Name**: `pos-cx-voice-assistant`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Plan**: `Free`

### Step 5: Deploy

1. **Click "Create Web Service"**
2. **Wait 2-3 minutes** for deployment
3. **Copy your URL** (e.g., `https://pos-cx-voice-assistant.onrender.com`)

## 🔗 **Configure in Retell**

1. **Go to [Retell Dashboard](https://app.retellai.com/)**
2. **Create New Agent**
3. **Select "Custom LLM"** as AI provider
4. **Enter your endpoint URL**:
   ```
   https://pos-cx-voice-assistant.onrender.com/chat
   ```
5. **Configure voice settings** (friendly female voice)
6. **Test the integration**

## 🧪 **Test Your Deployment**

### Test the Endpoint

Update your test script and run it:

```python
# In test_endpoint.py, change:
BASE_URL = "https://pos-cx-voice-assistant.onrender.com"
```

Then run:
```bash
python test_endpoint.py
```

### Test with Retell

1. **Call your Retell phone number**
2. **Test conversation flow**:
   - "Hello"
   - "I want to schedule a meeting"
   - "My name is John Doe"
   - "My phone number is 555-123-4567"
   - "I'd like to meet on Monday at 2 PM"
   - "Yes, that's correct"

## 💰 **Free Tier Limits**

- **750 hours/month** (enough for testing)
- **Auto-sleep** after 15 minutes of inactivity
- **Cold start** takes 30-60 seconds
- **Perfect for testing and development**

## 🔧 **Troubleshooting**

### Common Issues

1. **Build fails**:
   - Check that `requirements.txt` exists
   - Verify Python version compatibility

2. **Service won't start**:
   - Check the start command is correct
   - Verify port is set to `$PORT`

3. **Retell can't connect**:
   - Test endpoint manually first
   - Check if service is running

### Debug Commands

**Test your endpoint**:
```bash
curl -X POST "https://pos-cx-voice-assistant.onrender.com/chat" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

**Check health**:
```bash
curl "https://pos-cx-voice-assistant.onrender.com/health"
```

## 🎉 **You're Ready!**

Once deployed, your POS CX Voice Assistant will be:
- ✅ **Live and accessible** via HTTPS
- ✅ **Integrated with Retell**
- ✅ **Ready for real calls**
- ✅ **Completely free** for testing

**Next step**: Start taking calls with Skylar! 🚀 