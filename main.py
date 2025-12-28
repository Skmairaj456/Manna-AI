from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import get_response
from sentiment import get_mood, get_mood_emoji
import os

app = FastAPI()

# Root route to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return FileResponse("static/Manna.html")

# Serve static files (mounted after root route to avoid conflicts)
app.mount("/static", StaticFiles(directory="static"), name="static")

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

if __name__ == "__main__":
    import uvicorn
    print("Starting Manna AI Server...")
    print("Server will be available at: http://localhost:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)

