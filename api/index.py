from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sys
import os

# Add parent directory to path to import modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import with comprehensive error handling
get_response = None
get_mood = None
get_mood_emoji = None

try:
    from chatbot import get_response
    print("✓ chatbot imported successfully")
except Exception as e:
    print(f"✗ chatbot import error: {e}")
    import traceback
    traceback.print_exc()
    def get_response(user_input: str, user_id: str = "guest") -> str:
        return f"Error: Chatbot module not loaded. {str(e)}"

try:
    from sentiment import get_mood, get_mood_emoji
    print("✓ sentiment imported successfully")
except Exception as e:
    print(f"✗ sentiment import error: {e}")
    import traceback
    traceback.print_exc()
    def get_mood(text: str) -> str:
        return "neutral"
    def get_mood_emoji(mood: str) -> str:
        return "😐"

app = FastAPI()

# Handle favicon requests (browsers automatically request this)
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(content="", status_code=204)

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok", "message": "Manna AI is running"}

# Root route to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    try:
        # Try multiple paths
        possible_paths = [
            os.path.join(parent_dir, "static", "Manna.html"),
            os.path.join(os.path.dirname(__file__), "..", "static", "Manna.html"),
            os.path.join(os.path.dirname(__file__), "..", "..", "static", "Manna.html"),
        ]
        
        html_path = None
        for path in possible_paths:
            if os.path.exists(path):
                html_path = path
                break
        
        if html_path:
            return FileResponse(html_path)
        else:
            # Return a simple HTML page if file not found
            return HTMLResponse("""
            <!DOCTYPE html>
            <html>
            <head><title>Manna AI</title></head>
            <body>
                <h1>Manna AI Chatbot</h1>
                <p>HTML file not found. Please check the deployment.</p>
                <p>Try accessing: <a href="/health">/health</a></p>
            </body>
            </html>
            """)
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"Error in serve_home: {error_msg}")
        return HTMLResponse(f"<h1>Error loading page</h1><pre>{error_msg}</pre>", status_code=500)

# Serve static files (with error handling)
try:
    static_path = os.path.join(parent_dir, "static")
    if os.path.exists(static_path):
        app.mount("/static", StaticFiles(directory=static_path), name="static")
    else:
        print(f"Warning: Static directory not found at {static_path}")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")

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

