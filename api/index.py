from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import with error handling
try:
    from chatbot import get_response
    from sentiment import get_mood, get_mood_emoji
except Exception as e:
    print(f"Import error: {e}")
    # Fallback functions
    def get_response(user_input: str, user_id: str = "guest") -> str:
        return "Error: Chatbot module not loaded properly. Please check the logs."
    def get_mood(text: str) -> str:
        return "neutral"
    def get_mood_emoji(mood: str) -> str:
        return "😐"

app = FastAPI()

# Handle favicon requests (browsers automatically request this)
@app.get("/favicon.ico")
async def favicon():
    from fastapi.responses import Response
    return Response(status_code=204)  # No content

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok", "message": "Manna AI is running"}

# Root route to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    try:
        html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "Manna.html")
        if not os.path.exists(html_path):
            # Fallback: try alternative path
            html_path = os.path.join(os.path.dirname(__file__), "..", "static", "Manna.html")
        return FileResponse(html_path)
    except Exception as e:
        return HTMLResponse(f"<h1>Error loading page</h1><p>{str(e)}</p>", status_code=500)

# Serve static files
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

class UserMessage(BaseModel):
    message: str
    user_id: str = "guest"

@app.post("/chat")
async def chat_endpoint(user_msg: UserMessage):
    try:
        response = get_response(user_msg.message, user_msg.user_id)
        
        # Detect mood from user message
        try:
            mood = get_mood(user_msg.message)
            mood_emoji = get_mood_emoji(mood)
        except Exception as e:
            print(f"Mood detection error: {e}")
            mood = "neutral"
            mood_emoji = "😐"
        
        return {
            "response": response,
            "mood": mood,
            "mood_emoji": mood_emoji
        }
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        import traceback
        traceback.print_exc()
        return {
            "response": f"Sorry, I encountered an error: {str(e)}",
            "mood": "neutral",
            "mood_emoji": "😐"
        }

# Vercel serverless handler
handler = app

