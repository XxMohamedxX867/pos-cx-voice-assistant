# POS CX Voice Assistant - Custom LLM for Retell

This is a custom LLM implementation for Retell that acts as a voice scheduling assistant for POS CX. The assistant (Skylar) helps callers schedule meetings with the POS CX team.

## Features

- 🤖 **AI Voice Assistant**: Skylar from POS CX (Powered by Gemini 2.0 Flash)
- 📅 **Meeting Scheduling**: Collects caller information and schedules meetings
- 🎯 **Context-Aware**: Maintains conversation state and follows specific workflow
- 🔄 **Retell Integration**: Compatible with Retell's custom LLM API
- 📞 **Professional Greeting**: Starts with proper introduction and recording notice

## Conversation Flow

1. **Greeting**: "Hey, this is Skylar from POS CX. You're on a recorded line. How can I help you today?"
2. **Intent Detection**: Determines if caller wants to schedule a meeting
3. **Information Collection**: Gathers name, phone number, and preferred meeting time
4. **Confirmation**: Reviews all details with the caller
5. **Completion**: Confirms booking and ends call professionally

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

### 3. Test the Endpoint

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello"}
    ]
  }'
```

## Deployment Options

### Option 1: Local Development (for testing)

1. Run the server locally
2. Use ngrok to expose it to the internet:
   ```bash
   ngrok http 8000
   ```
3. Use the ngrok URL in Retell

### Option 2: Cloud Deployment (Recommended)

#### Deploy to Railway

1. Create a Railway account
2. Connect your GitHub repository
3. Railway will automatically detect the Python app
4. Add environment variables if needed
5. Deploy and get your public URL

#### Deploy to Render

1. Create a Render account
2. Create a new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy and get your public URL

#### Deploy to Heroku

1. Create a `Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
2. Deploy using Heroku CLI or GitHub integration

## Retell Integration

### 1. Get Your Deployment URL

After deploying, you'll get a URL like:
- `https://your-app-name.railway.app`
- `https://your-app-name.onrender.com`
- `https://your-app-name.herokuapp.com`

### 2. Configure in Retell

1. Go to your Retell dashboard
2. Create a new voice agent
3. Select "Custom LLM" as the AI provider
4. Enter your deployment URL + `/chat` endpoint:
   ```
   https://your-app-name.railway.app/chat
   ```
5. Configure voice settings (recommended: friendly, professional voice)
6. Test the integration

### 3. API Endpoint Details

**Endpoint**: `POST /chat`

**Request Format**:
```json
{
  "messages": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hey, this is Skylar from POS CX..."}
  ]
}
```

**Response Format**:
```json
{
  "message": "Hey, this is Skylar from POS CX. You're on a recorded line. How can I help you today?",
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 25,
    "total_tokens": 175
  }
}
```

## Customization

### Modify the System Prompt

Edit the `SYSTEM_PROMPT` variable in `main.py` to change:
- Company name
- Available hours
- Greeting message
- Conversation flow

### Add New Features

1. **Database Integration**: Add meeting storage
2. **Calendar Integration**: Connect to Google Calendar
3. **Email Notifications**: Send confirmation emails
4. **Analytics**: Track call metrics

## Environment Variables

Create a `.env` file for sensitive data:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## Monitoring

The server includes:
- Health check endpoint: `GET /health`
- Request logging
- Error handling
- Usage tracking

## Troubleshooting

### Common Issues

1. **CORS Errors**: The server includes CORS middleware for Retell
2. **API Key Issues**: Verify your Gemini API key is valid
3. **Deployment Issues**: Check logs in your cloud provider dashboard

### Testing

Test the conversation flow:
1. Start with "Hello"
2. Say "I want to schedule a meeting"
3. Provide name: "John Doe"
4. Provide phone: "555-123-4567"
5. Provide time: "Monday at 2 PM"
6. Confirm details

## Security Notes

- The Gemini API key is currently hardcoded for simplicity
- For production, use environment variables
- Consider adding rate limiting
- Implement proper session management

## Support

For issues with:
- **Retell Integration**: Check Retell documentation
- **Deployment**: Check your cloud provider's logs
- **API Issues**: Check the `/health` endpoint

## License

This project is for POS CX internal use. 