# Deployment Guide - POS CX Voice Assistant

This guide will help you deploy your custom LLM to various cloud platforms for use with Retell.

## 🚀 Quick Deploy Options

### Option 1: Railway (Recommended - Easiest)

1. **Sign up for Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect Python and deploy

3. **Get Your URL**
   - Once deployed, click on your project
   - Copy the generated URL (e.g., `https://your-app-name.railway.app`)

4. **Configure in Retell**
   - Use: `https://your-app-name.railway.app/chat`

### Option 2: Render (Free Tier Available)

1. **Sign up for Render**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Choose free plan

3. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)

4. **Get Your URL**
   - Copy the generated URL (e.g., `https://your-app-name.onrender.com`)

### Option 3: Heroku (Paid)

1. **Install Heroku CLI**
   ```bash
   # Windows
   winget install --id=Heroku.HerokuCLI
   
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Login and Deploy**
   ```bash
   heroku login
   heroku create your-app-name
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

3. **Get Your URL**
   - Your app will be at: `https://your-app-name.herokuapp.com`

## 🔧 Local Testing with ngrok

Before deploying, test locally with ngrok:

1. **Install ngrok**
   ```bash
   # Download from https://ngrok.com/download
   # Or use npm: npm install -g ngrok
   ```

2. **Start your server**
   ```bash
   python main.py
   ```

3. **Expose with ngrok**
   ```bash
   ngrok http 8000
   ```

4. **Use ngrok URL in Retell**
   - Copy the HTTPS URL from ngrok (e.g., `https://abc123.ngrok.io`)
   - Use: `https://abc123.ngrok.io/chat`

## 📋 Retell Configuration

### Step 1: Create Voice Agent

1. Go to [Retell Dashboard](https://app.retellai.com/)
2. Click "Create New Agent"
3. Choose "Custom LLM" as AI provider

### Step 2: Configure Endpoint

1. **LLM Endpoint URL**: Enter your deployment URL + `/chat`
   ```
   https://your-app-name.railway.app/chat
   ```

2. **Request Format**: The endpoint expects:
   ```json
   {
     "messages": [
       {"role": "user", "content": "Hello"},
       {"role": "assistant", "content": "Previous response..."}
     ]
   }
   ```

3. **Response Format**: The endpoint returns:
   ```json
   {
     "message": "AI response here",
     "usage": {
       "prompt_tokens": 150,
       "completion_tokens": 25,
       "total_tokens": 175
     }
   }
   ```

### Step 3: Voice Settings

Recommended settings for Skylar:
- **Voice**: Choose a friendly, professional female voice
- **Language**: English (US)
- **Speed**: Normal (1.0x)
- **Pitch**: Slightly warm and approachable

### Step 4: Test the Integration

1. **Test with Text**
   - Use the test feature in Retell
   - Try: "Hello, I want to schedule a meeting"

2. **Test with Voice**
   - Call your Retell phone number
   - Follow the conversation flow

## 🧪 Testing Your Deployment

### Run the Test Script

1. **Update the URL** in `test_endpoint.py`:
   ```python
   BASE_URL = "https://your-app-name.railway.app"
   ```

2. **Run the test**:
   ```bash
   python test_endpoint.py
   ```

### Manual Testing

Test the conversation flow:
1. "Hello"
2. "I want to schedule a meeting"
3. "My name is John Doe"
4. "My phone number is 555-123-4567"
5. "I'd like to meet on Monday at 2 PM"
6. "Yes, that's correct"

## 🔍 Troubleshooting

### Common Issues

1. **CORS Errors**
   - ✅ Already handled in the code
   - The server includes CORS middleware

2. **API Key Issues**
   - ✅ Already configured with your Gemini key
   - If you need to change it, edit `main.py`

3. **Deployment Fails**
   - Check the logs in your cloud provider dashboard
   - Ensure all files are committed to GitHub
   - Verify `requirements.txt` is present

4. **Retell Can't Connect**
   - Verify your endpoint URL is correct
   - Test with curl or Postman first
   - Check if your deployment is running

### Debug Commands

**Test endpoint manually**:
```bash
curl -X POST "https://your-app-name.railway.app/chat" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

**Check health**:
```bash
curl "https://your-app-name.railway.app/health"
```

## 📊 Monitoring

### Health Check
- Endpoint: `GET /health`
- Returns: `{"status": "healthy", "service": "POS CX Voice Assistant"}`

### Logs
- Check your cloud provider's dashboard for logs
- The server logs all requests and errors

### Usage Tracking
- Each response includes token usage information
- Monitor your Gemini API usage in Google AI Studio

## 🔒 Security Considerations

### For Production

1. **Environment Variables**
   - Move API key to environment variables
   - Don't commit sensitive data to GitHub

2. **Rate Limiting**
   - Consider adding rate limiting
   - Monitor for abuse

3. **HTTPS Only**
   - All cloud providers provide HTTPS
   - Never use HTTP in production

## 📞 Support

### Getting Help

1. **Deployment Issues**: Check your cloud provider's documentation
2. **Retell Issues**: Check Retell's documentation and support
3. **Code Issues**: Review the logs and error messages

### Useful Links

- [Railway Documentation](https://docs.railway.app/)
- [Render Documentation](https://render.com/docs)
- [Heroku Documentation](https://devcenter.heroku.com/)
- [Retell Documentation](https://docs.retellai.com/)
- [Google AI Studio](https://makersuite.google.com/app/apikey)

---

**Next Steps**: After deployment, test thoroughly and then integrate with your phone system! 