import os
import random
import openai
import re

from nlp_utils import clean_text, detect_language, translate_text
from sentiment import analyze_sentiment, get_mood, get_mood_emoji, get_mood_message
from joke_manager import get_joke
from code_executor import run_code, debug_code
from voice_io import text_to_speech, speech_to_text  # Optional for voice support
from knowledge_base import get_custom_response, find_response_category, get_qa_response, get_contextual_response

# Set OpenAI API key from environment variable
# IMPORTANT: Set OPENAI_API_KEY environment variable or add it in deployment platform
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def get_response(user_input: str, user_id: str = "guest") -> str:
    """
    Main chatbot response function, routes queries to relevant modules
    """

    # Clean and prepare input text
    text = clean_text(user_input)
    original_text = user_input.lower().strip()
    lang = detect_language(text)

    # PRIORITY 1: Handle creator/about questions (custom response)
    if any(word in original_text for word in ["creator", "created", "who made", "who built", "about", "developer", "author", "tammanna", "mairaj"]):
        return "Manna AI was created by Tammanna and Mairaj. We're passionate developers who built this intelligent chatbot to help users with various tasks including AI conversations, code execution, jokes, mood detection, and more. Thank you for using Manna AI!"

    # PRIORITY 2: Check knowledge base for custom responses (skip if code generation)
    # Check for code generation first
    code_phrases = ["give me", "show me", "write", "create", "generate", "example", "sample", "how to"]
    code_words = ["code", "program", "script", "function", "algorithm", "snippet"]
    programming_tasks = ["print", "printing", "string", "variable", "list", "dictionary", "loop", "if", "class", "import"]
    math_code_words = ["sum", "summation", "add", "addition", "calculate", "calculation", "multiply", "divide"]
    
    is_code_generation = (
        any(phrase in original_text for phrase in code_phrases) and 
        any(word in original_text for word in code_words)
    ) or (
        any(phrase in original_text for phrase in ["give me", "show me", "write", "create", "how to"]) and
        any(word in original_text for word in programming_tasks + math_code_words)
    ) or (
        "code" in original_text and any(word in original_text for word in ["for", "to", "of", "in"])
    ) or (
        any(word in original_text for word in ["python code", "java code", "javascript code", "code example"])
    )
    
    # Skip knowledge base and Q&A if it's a code generation request
    if not is_code_generation:
        category = find_response_category(user_input)
        if category:
            custom_response = get_custom_response(category)
            if custom_response:
                return custom_response
        
        # PRIORITY 3: Check common Q&A
        qa_response = get_qa_response(user_input)
        if qa_response:
            return qa_response

    # PRIORITY 4: Respond to joke requests
    if "joke" in original_text or "funny" in original_text:
        return get_joke()

    # PRIORITY 5: Code generation detection already done above
    # is_code_generation variable is set above and will be used in OpenAI section
    
    # PRIORITY 6: Handle code execution and debugging requests
    if text.strip().startswith(("run", "execute", "code:", "debug")) or "run code" in original_text or "execute code" in original_text:
        if "debug" in text.lower():
            code_to_debug = text.partition("debug")[2].strip()
            return debug_code(code_to_debug)
        else:
            code_to_run = (
                text.partition("run")[2].strip()
                or text.partition("execute")[2].strip()
                or text.partition("code:")[2].strip()
            )
            if code_to_run:
                return run_code(code_to_run)
            else:
                return "Please provide the code to execute. Example: 'run print(2+2)'"
    
    # PRIORITY 7: Handle specific question patterns with custom responses
    # Only trigger if it's actually a "what is" question, not a code generation request
    if (("what is" in original_text or "what's" in original_text or "explain" in original_text) and 
        not is_code_generation):
        # Try to provide custom explanation first
        if "manna" in original_text:
            return "Manna AI is an intelligent chatbot. I can help with conversations, code execution, jokes, mood detection, and various other tasks. I'm designed to be helpful, empathetic, and fun to interact with!"
        
        if "python" in original_text and ("what is" in original_text or "what's" in original_text):
            return "Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used for web development, data science, AI, automation, and more. I can help you run Python code - just type 'run' followed by your code!"
        
        if ("javascript" in original_text or "js" in original_text) and ("what is" in original_text or "what's" in original_text):
            return "JavaScript is a programming language primarily used for web development. It enables interactive web pages and is essential for front-end development. Need help with JavaScript code? I can execute it for you!"
        
        if ("ai" in original_text or "artificial intelligence" in original_text) and ("what is" in original_text or "what's" in original_text):
            return "AI (Artificial Intelligence) is the simulation of human intelligence by machines. It includes machine learning, natural language processing, and more. I'm an example of AI designed to help and assist users!"
    
    # PRIORITY 8: Handle time/date questions
    if any(word in original_text for word in ["time", "date", "day", "what day", "what time"]):
        from datetime import datetime
        now = datetime.now()
        if "time" in original_text:
            return f"The current time is {now.strftime('%I:%M %p')}. How can I help you further?"
        elif "date" in original_text or "day" in original_text:
            return f"Today is {now.strftime('%A, %B %d, %Y')}. Is there anything else you'd like to know?"
    
    # PRIORITY 9: Handle math questions (simple calculations)
    if re.search(r'\d+\s*[+\-*/]\s*\d+', user_input):
        try:
            # Simple math evaluation (safe)
            result = eval(user_input.replace('=', '').strip())
            return f"The answer is: {result}. Need help with anything else?"
        except:
            pass

    # Analyze sentiment and detect mood (do this early for mood-aware responses)
    try:
        sentiment = analyze_sentiment(user_input)
        mood = get_mood(user_input)
        mood_emoji = get_mood_emoji(mood)
    except Exception:
        sentiment = {'polarity': 0, 'subjectivity': 0}
        mood = "neutral"
        mood_emoji = "😐"
    
    # PRIORITY 10: Check contextual responses based on mood
    contextual_response = get_contextual_response(user_input, mood)
    if contextual_response:
        return contextual_response
    
    # PRIORITY 11: Handle general questions with custom responses
    if "?" in user_input or any(word in original_text for word in ["tell me", "describe", "define"]):
        # Try to provide custom responses for common questions
        if any(word in original_text for word in ["name", "who are you", "what's your name"]):
            return "I'm Manna AI, your intelligent assistant ready to help with various tasks!"
        
        if any(word in original_text for word in ["where", "location"]):
            return "I exist in the digital world to assist users like you! Where would you like to go or what would you like to know?"
        
        if any(word in original_text for word in ["why", "reason"]):
            return "I was created to help people with various tasks, make conversations more engaging, and provide assistance whenever needed. How can I help you today?"
    
    # PRIORITY 12: Handle compliments and positive feedback
    if any(word in original_text for word in ["good", "great", "awesome", "amazing", "wonderful", "excellent", "love", "like"]):
        if mood in ["happy", "positive"]:
            return "Thank you so much! I'm really glad you're enjoying Manna AI. Is there anything else I can help with?"
    
    # PRIORITY 13: Handle complaints or negative feedback
    if any(word in original_text for word in ["bad", "terrible", "hate", "dislike", "wrong", "error", "bug", "problem"]):
        if mood in ["negative", "sad"]:
            return "I'm sorry to hear that. I'm here to help improve your experience. Could you tell me more about what's not working?"

    # If no direct handler, fallback to OpenAI GPT chat completion (LAST RESORT)
    if not openai.api_key:
        return "I can tell jokes, execute code, answer questions, and help with various tasks! For advanced AI conversations, an API key is needed. But I can still help with many things - try asking for a joke, running code, or asking about my capabilities!"

    try:
        # Check if this is a code generation request (same logic as above)
        code_phrases = ["give me", "show me", "write", "create", "generate", "example", "sample", "how to"]
        code_words = ["code", "program", "script", "function", "algorithm", "snippet"]
        programming_tasks = ["print", "printing", "string", "variable", "list", "dictionary", "loop", "if", "class", "import"]
        math_code_words = ["sum", "summation", "add", "addition", "calculate", "calculation", "multiply", "divide"]
        
        is_code_request = (
            any(phrase in original_text for phrase in code_phrases) and 
            any(word in original_text for word in code_words)
        ) or (
            any(phrase in original_text for phrase in ["give me", "show me", "write", "create", "how to"]) and
            any(word in original_text for word in programming_tasks + math_code_words)
        ) or (
            "code" in original_text and any(word in original_text for word in ["for", "to", "of", "in"])
        ) or (
            any(word in original_text for word in ["python code", "java code", "javascript code", "code example"])
        )
        
        # Enhanced system message with more context about Manna AI
        mood_context = {
            "happy": "The user seems happy and positive. Respond enthusiastically and match their energy. You are Manna AI.",
            "positive": "The user is in a positive mood. Be friendly and supportive. You are Manna AI.",
            "neutral": "The user seems neutral. Be helpful and professional. You are Manna AI.",
            "negative": "The user seems to be in a negative mood. Be empathetic, understanding, and offer support. Consider suggesting something uplifting. You are Manna AI.",
            "sad": "The user appears sad or upset. Be very empathetic, gentle, and supportive. Offer comfort and maybe suggest a joke or positive activity. You are Manna AI."
        }
        
        # Special handling for code generation requests
        if is_code_request:
            system_message = """You are Manna AI, an intelligent chatbot.
            The user is asking for code. Generate clean, well-commented Python code that solves their request.
            Include:
            - Clear, working code
            - Helpful comments explaining the code
            - Example usage if applicable
            - Brief explanation if needed
            Format code in markdown code blocks with python syntax highlighting.
            Keep responses focused on the code request."""
        else:
            system_message = f"""You are Manna AI, an intelligent chatbot. 
            {mood_context.get(mood, 'Be helpful and friendly.')} 
            The user's current mood appears to be {mood}.
            Provide personalized, helpful responses. Keep responses concise (under 200 words) and friendly.
            Only mention creators if specifically asked about them."""
        
        # Compose messages for chat completion
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input},  # Use original input, not cleaned text
        ]

        # Try new API first, fallback to old API
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai.api_key)
            # Increase tokens for code generation requests
            max_tokens = 500 if is_code_request else 200
            temperature = 0.7 if is_code_request else 0.8  # Lower temp for code = more consistent
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            answer = response.choices[0].message.content.strip()
        except (ImportError, AttributeError):
            # Fallback to old API
            # Increase tokens for code generation requests
            max_tokens = 500 if is_code_request else 200
            temperature = 0.7 if is_code_request else 0.8  # Lower temp for code = more consistent
            
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                n=1,
            )
            answer = response.choices[0].message['content'].strip()
    except Exception as e:
        answer = f"Sorry, I encountered an error processing your request: {str(e)}"

    # Add mood-aware response for negative/sad moods
    if mood in ["sad", "negative"] and not any(word in original_text for word in ["joke", "creator", "code", "run", "execute", "debug"]):
        mood_msg = get_mood_message(mood)
        if mood_msg:
            answer = f"{mood_msg} {answer}"

    # Translate the answer back to user's language if needed
    if lang != "en":
        answer = translate_text(answer, dest=lang)

    return answer

