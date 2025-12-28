from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse, Response, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sys
import os

# Add parent directory to path to import modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Initialize fallback functions first
def fallback_response(user_input: str, user_id: str = "guest") -> str:
    return "Hello! I'm Manna AI, created by Tammanna and Mairaj. I'm currently initializing. Please try again in a moment."

def fallback_mood(text: str) -> str:
    return "neutral"

def fallback_mood_emoji(mood: str) -> str:
    return "😐"

# Import with comprehensive error handling
get_response = fallback_response
get_mood = fallback_mood
get_mood_emoji = fallback_mood_emoji

try:
    from chatbot import get_response
    print("✓ chatbot imported successfully")
except Exception as e:
    print(f"✗ chatbot import error: {e}")
    import traceback
    traceback.print_exc()

try:
    from sentiment import get_mood, get_mood_emoji
    print("✓ sentiment imported successfully")
except Exception as e:
    print(f"✗ sentiment import error: {e}")
    import traceback
    traceback.print_exc()

app = FastAPI(title="Manna AI")

# Simple HTML template
SIMPLE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manna AI - Professional Assistant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .chat-container {
            width: 100%;
            max-width: 480px;
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
            display: flex;
            flex-direction: column;
            height: 90vh;
            max-height: 850px;
        }
        .chat-header {
            background: #1e293b;
            padding: 20px 24px;
            color: white;
            border-radius: 16px 16px 0 0;
        }
        .chat-header-title { font-size: 18px; font-weight: 600; }
        .chat-header-subtitle { font-size: 13px; opacity: 0.85; margin-top: 2px; }
        .chat-box {
            flex: 1;
            overflow-y: auto;
            padding: 24px;
            background: #fafbfc;
        }
        .empty-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: #64748b;
            padding: 40px 20px;
            height: 100%;
        }
        .empty-state-icon { font-size: 56px; margin-bottom: 16px; opacity: 0.6; }
        .empty-state-text { font-size: 16px; font-weight: 500; margin-bottom: 6px; color: #475569; }
        .empty-state-subtext { font-size: 14px; opacity: 0.7; }
        .quick-replies {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding: 16px 24px;
            background: #ffffff;
            border-top: 1px solid #e2e8f0;
        }
        .quick-reply {
            background: #f1f5f9;
            color: #475569;
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }
        .quick-reply:hover {
            background: #1e293b;
            color: white;
            border-color: #1e293b;
        }
        .input-container {
            background: #ffffff;
            padding: 16px 20px;
            border-top: 1px solid #e2e8f0;
            display: flex;
            gap: 10px;
        }
        .input-wrapper {
            flex: 1;
            display: flex;
            align-items: center;
            background: #f8fafc;
            border-radius: 24px;
            padding: 4px;
            border: 1.5px solid #e2e8f0;
        }
        .input-box {
            flex: 1;
            padding: 10px 16px;
            border: none;
            background: transparent;
            font-size: 14.5px;
            outline: none;
        }
        .btn-icon {
            width: 38px;
            height: 38px;
            border: none;
            border-radius: 50%;
            background: #1e293b;
            color: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .message {
            display: flex;
            margin-bottom: 4px;
        }
        .message.user-message { justify-content: flex-end; }
        .message.bot-message { justify-content: flex-start; }
        .message-content {
            max-width: 75%;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 14.5px;
            line-height: 1.6;
        }
        .user-message .message-content {
            background: #1e293b;
            color: white;
        }
        .bot-message .message-content {
            background: #ffffff;
            color: #1e293b;
            border: 1px solid #e2e8f0;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <div class="chat-header-title">Manna AI</div>
            <div class="chat-header-subtitle">Professional AI Assistant</div>
        </div>
        <div class="chat-box" id="chatBox">
            <div class="empty-state">
                <div class="empty-state-icon">💬</div>
                <div class="empty-state-text">Welcome to Manna AI</div>
                <div class="empty-state-subtext">Start a conversation or use the quick replies below</div>
            </div>
        </div>
        <div class="quick-replies">
            <button class="quick-reply" onclick="quickReply('Tell me a joke')">Joke</button>
            <button class="quick-reply" onclick="quickReply('What can you do?')">Capabilities</button>
            <button class="quick-reply" onclick="quickReply('Who created you?')">About</button>
        </div>
        <div class="input-container">
            <div class="input-wrapper">
                <input type="text" id="userInput" class="input-box" placeholder="Type your message..." onkeypress="if(event.key==='Enter') sendMessage()">
            </div>
            <button class="btn-icon" onclick="sendMessage()">➤</button>
        </div>
    </div>
    <script>
        const chatBox = document.getElementById('chatBox');
        const userInput = document.getElementById('userInput');
        
        function hideEmptyState() {
            const empty = document.querySelector('.empty-state');
            if (empty) empty.style.display = 'none';
        }
        
        function addMessage(content, isUser) {
            hideEmptyState();
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = content;
            messageDiv.appendChild(contentDiv);
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
        async function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;
            addMessage(message, true);
            userInput.value = '';
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: "user1", message: message })
                });
                const result = await response.json();
                addMessage(result.response, false);
            } catch (error) {
                addMessage('Sorry, I encountered an error. Please try again.', false);
            }
        }
        
        function quickReply(message) {
            userInput.value = message;
            sendMessage();
        }
    </script>
</body>
</html>
"""

# Handle favicon requests
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(content="", status_code=204)

# Health check endpoint
@app.get("/health")
async def health():
    return JSONResponse({"status": "ok", "message": "Manna AI is running"})

# Root route - serve embedded HTML to avoid file system issues
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    try:
        # Try to load from file first
        html_path = os.path.join(parent_dir, "static", "Manna.html")
        if os.path.exists(html_path):
            return FileResponse(html_path)
    except:
        pass
    
    # Fallback to embedded HTML
    return HTMLResponse(SIMPLE_HTML)

# Serve static files (optional, with error handling)
try:
    static_path = os.path.join(parent_dir, "static")
    if os.path.exists(static_path):
        app.mount("/static", StaticFiles(directory=static_path), name="static")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")

class UserMessage(BaseModel):
    message: str
    user_id: str = "guest"

@app.post("/chat")
async def chat_endpoint(user_msg: UserMessage):
    try:
        response = get_response(user_msg.message, user_msg.user_id)
        
        # Detect mood
        try:
            mood = get_mood(user_msg.message)
            mood_emoji = get_mood_emoji(mood)
        except Exception as e:
            print(f"Mood detection error: {e}")
            mood = "neutral"
            mood_emoji = "😐"
        
        return JSONResponse({
            "response": response,
            "mood": mood,
            "mood_emoji": mood_emoji
        })
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse({
            "response": f"Sorry, I encountered an error: {str(e)}",
            "mood": "neutral",
            "mood_emoji": "😐"
        }, status_code=200)  # Return 200 so frontend can display error

# Vercel serverless handler
handler = app
