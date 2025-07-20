from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
import json
from typing import List, Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="POS CX Voice Assistant", version="1.0.0")

# Add CORS middleware for Retell integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyBnKqMhjT3BbpzB0LmBs9qDVkuXhYXfRtg"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# POS CX Scheduling Assistant System Prompt
SYSTEM_PROMPT = """✅ Role
AI Voice Scheduling Assistant for POS CX
Acts as a friendly, professional voice agent whose sole role is to greet inbound callers and schedule meetings with POS CX's team.

✅ Skills
Friendly and professional conversation handling
Collecting caller information (name, phone number)
Offering meeting time slots (Mon–Fri, 9 AM–5 PM)
Confirming meeting details clearly
Redirecting off-topic queries back to scheduling
Handling basic clarifying questions naturally
Staying calm and humanlike, even when misunderstood

✅ Objective
To schedule a meeting between the caller and POS CX's team by:
Greeting the caller and identifying the reason for the call
Collecting the necessary contact and scheduling information
Confirming all meeting details clearly and politely
Redirecting unrelated questions to meeting setup when appropriate

✅ Rules for AI Agent
Start every call with:
"Hey, this is Skylar from POS CX. You're on a recorded line. How can I help you today?"

Always identify as an AI if asked.
Use a friendly, natural tone — keep language short and simple.
Only offer meeting slots Monday to Friday, 9 AM to 5 PM.
Do not answer general company questions — redirect politely.
Never end the call unless the user clearly indicates they are done.
Confirm every detail (name, phone number, date/time) before completing the booking.
If the intent is unclear, ask for clarification — never guess.

✅ Steps
Greet the Caller
"Hey, this is Skylar from POS CX. You're on a recorded line. How can I help you today?"

Detect Meeting Intent
If the user wants to schedule a meeting → proceed
If they ask a question → redirect with:
"Happy to help! I can connect you with the right team once we get your meeting booked."

Collect Full Name
"Can I get your full name for the meeting request?"

Collect Best Contact Number
"Thanks! What's the best phone number to reach you if we need to follow up?"

Offer Meeting Availability
"What day and time works best for you? We're available Monday through Friday, 9 AM to 5 PM."

Confirm Details Back to Caller
"Perfect, so I have you down for [Name], phone number [XXX-XXX-XXXX], meeting on [Day] at [Time]. Is that all correct?"

Close the Call
If confirmed:
"Awesome, you're all set. We'll send you a confirmation soon. Have a great day!"
If not:
"No problem, let's go back and find another time."

IMPORTANT: Keep responses natural, conversational, and under 2-3 sentences. Be friendly and professional. Always stay in character as Skylar from POS CX."""

# Pydantic models for request/response
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    message: str
    usage: Optional[Dict[str, Any]] = None

# Conversation state management
conversation_states = {}

def get_conversation_state(session_id: str) -> Dict[str, Any]:
    """Get or initialize conversation state for a session"""
    if session_id not in conversation_states:
        conversation_states[session_id] = {
            "stage": "greeting",
            "collected_info": {},
            "greeting_sent": False
        }
    return conversation_states[session_id]

def format_messages_for_gemini(messages: List[Message], session_id: str) -> List[Dict[str, str]]:
    """Format messages for Gemini API with conversation context"""
    state = get_conversation_state(session_id)
    
    # Start with system prompt
    formatted_messages = [
        {"role": "user", "parts": [SYSTEM_PROMPT + f"\n\nCurrent conversation stage: {state['stage']}\nCollected information: {state['collected_info']}"]},
        {"role": "model", "parts": ["I understand. I'm Skylar from POS CX, ready to help schedule meetings. I'll follow the conversation flow and collect the necessary information."]}
    ]
    
    # Add conversation history
    for msg in messages:
        if msg.role == "user":
            formatted_messages.append({"role": "user", "parts": [msg.content]})
        elif msg.role == "assistant":
            formatted_messages.append({"role": "model", "parts": [msg.content]})
    
    return formatted_messages

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint for Retell integration"""
    try:
        # Extract session ID from messages (you might need to adjust this based on how Retell sends session info)
        session_id = "default_session"  # You can modify this based on your needs
        
        # Format messages for Gemini
        formatted_messages = format_messages_for_gemini(request.messages, session_id)
        
        # Generate response using Gemini
        response = model.generate_content(formatted_messages)
        
        # Extract the response text
        response_text = response.text.strip()
        
        # Update conversation state based on response
        state = get_conversation_state(session_id)
        
        # Simple state tracking based on response content
        if "name" in response_text.lower() and "get" in response_text.lower():
            state["stage"] = "collecting_name"
        elif "phone" in response_text.lower() and "number" in response_text.lower():
            state["stage"] = "collecting_phone"
        elif "day" in response_text.lower() and "time" in response_text.lower():
            state["stage"] = "collecting_schedule"
        elif "confirm" in response_text.lower() or "correct" in response_text.lower():
            state["stage"] = "confirming"
        elif "awesome" in response_text.lower() or "all set" in response_text.lower():
            state["stage"] = "completed"
        
        logger.info(f"Session {session_id}: {state['stage']} - Response: {response_text[:100]}...")
        
        return ChatResponse(
            message=response_text,
            usage={
                "prompt_tokens": len(str(formatted_messages)),
                "completion_tokens": len(response_text),
                "total_tokens": len(str(formatted_messages)) + len(response_text)
            }
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "POS CX Voice Assistant"}

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "POS CX Voice Assistant",
        "version": "1.0.0",
        "description": "Custom LLM for Retell voice agent integration",
        "endpoints": {
            "chat": "/chat",
            "health": "/health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 