from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot import get_response
from sentiment import get_mood, get_mood_emoji

app = FastAPI()

# Root route to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "Manna.html")
    return FileResponse(html_path)

# Serve static files
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

class UserMessage(BaseModel):
    message: str
    user_id: str = "guest"

@app.post("/chat")
async def chat_endpoint(user_msg: UserMessage):
    response = get_response(user_msg.message, user_msg.user_id)
    
    # Detect mood from user message
    try:
        mood = get_mood(user_msg.message)
        mood_emoji = get_mood_emoji(mood)
    except Exception:
        mood = "neutral"
        mood_emoji = "😐"
    
    return {
        "response": response,
        "mood": mood,
        "mood_emoji": mood_emoji
    }

# Vercel serverless handler
handler = app

