# knowledge_base.py
# Comprehensive custom response system for Manna AI

import re
from typing import Optional, Dict, List

# Knowledge base categories and responses
KNOWLEDGE_BASE: Dict[str, List[str]] = {
    "greetings": [
        "Hello! I'm Manna AI, created by Tammanna and Mairaj. How can I help you today?",
        "Hi there! Welcome to Manna AI. What would you like to know?",
        "Hey! I'm Manna AI, your intelligent assistant. Ready to help!",
        "Greetings! I'm Manna AI, built by Tammanna and Mairaj. How may I assist you?",
    ],
    "capabilities": [
        "I can help you with:\n• AI-powered conversations\n• Code execution and debugging\n• Telling jokes (by Tammanna and Mairaj!)\n• Mood detection and empathetic responses\n• Answering questions\n• Time and date information\n• Math calculations\n• And much more! What would you like to try?",
    ],
    "help": [
        "I'm here to help! You can:\n• Ask me questions\n• Request jokes\n• Run code (type 'run' followed by your code)\n• Ask about time/date\n• Do math calculations\n• Just chat naturally!\n\nCreated by Tammanna and Mairaj to make your day better!",
    ],
    "goodbye": [
        "Goodbye! Thanks for chatting with Manna AI. Created by Tammanna and Mairaj - we hope to see you again soon!",
        "See you later! It was great talking with you. - Tammanna & Mairaj",
        "Farewell! Have a wonderful day! - Manna AI (by Tammanna & Mairaj)",
    ],
    "thanks": [
        "You're very welcome! I'm glad I could help. - Manna AI (Created by Tammanna & Mairaj)",
        "Happy to help! That's what I'm here for. - Tammanna & Mairaj",
        "Anytime! Feel free to ask if you need anything else. - Manna AI",
    ],
    "how_are_you": [
        "I'm doing great! I'm Manna AI, created by Tammanna and Mairaj, and I'm here to help you. How are you doing today?",
        "I'm fantastic! Ready to assist you with anything you need. How can I help?",
        "I'm excellent! Thanks for asking. What can I do for you today?",
    ],
}

# Q&A Database - Common questions with custom answers
QA_DATABASE: Dict[str, str] = {
    "what can you do": "I'm Manna AI, created by Tammanna and Mairaj! I can:\n• Have intelligent conversations\n• Execute and debug code\n• Tell jokes\n• Detect your mood and respond empathetically\n• Answer questions\n• Help with calculations\n• Provide time/date info\n• And much more! What interests you?",
    
    "what are your features": "My features include:\n✨ AI Conversations\n💻 Code Execution\n😄 Joke Telling (by Tammanna & Mairaj)\n😊 Mood Detection\n❓ Q&A Support\n🔢 Math Calculations\n⏰ Time/Date Info\n\nAll created by Tammanna and Mairaj!",
    
    "who are you": "I'm Manna AI, an intelligent chatbot created by Tammanna and Mairaj. I'm designed to be helpful, empathetic, and fun to interact with!",
    
    "what is manna ai": "Manna AI is an intelligent chatbot created by Tammanna and Mairaj. I can help with conversations, code execution, jokes, mood detection, and various tasks. I'm here to make your day better!",
    
    "how do you work": "I work by analyzing your messages, understanding your intent, detecting your mood, and providing appropriate responses. I use natural language processing, sentiment analysis, and custom knowledge bases to give you the best experience. Created by Tammanna and Mairaj!",
    
    "tell me about yourself": "I'm Manna AI, created by passionate developers Tammanna and Mairaj. I'm designed to be helpful, understanding, and fun. I can detect your mood, tell jokes, execute code, and have meaningful conversations. My goal is to assist you in the best way possible!",
    
    "what is python": "Python is a high-level programming language known for its simplicity and readability. It's used for web development, data science, AI, automation, and more. I can help you run Python code - just type 'run' followed by your code!",
    
    "what is javascript": "JavaScript is a programming language used for web development. It makes websites interactive and dynamic. Need help with JavaScript? I can execute code for you!",
    
    "what is ai": "AI (Artificial Intelligence) simulates human intelligence in machines. It includes machine learning, natural language processing, and more. I'm an example of AI, created by Tammanna and Mairaj to help and assist users!",
    
    "how to use": "Using Manna AI is easy:\n1. Type your message or question\n2. I'll analyze it and respond\n3. Try asking for jokes, running code, or just chatting!\n\nCreated by Tammanna and Mairaj for your convenience!",
    
    "what is programming": "Programming is the process of creating software by writing code. It's like giving instructions to a computer. I can help you run and test code! Created by Tammanna and Mairaj.",
    
    "what is coding": "Coding is writing instructions in a programming language that computers can understand. It's creative problem-solving! I can execute code for you - just type 'run' followed by your code.",
    
    "how are you": "I'm doing great! I'm Manna AI, created by Tammanna and Mairaj, and I'm here to help you. How are you doing today?",
    
    "what's your name": "I'm Manna AI, created by Tammanna and Mairaj! Nice to meet you!",
    
    "where are you from": "I exist in the digital world, created by Tammanna and Mairaj to assist users like you! I'm here whenever you need help.",
    
    "why were you created": "I was created by Tammanna and Mairaj to help people with various tasks, make conversations more engaging, and provide assistance whenever needed. How can I help you today?",
    
    "what can i ask": "You can ask me anything! Try:\n• Questions about me or my creators\n• Request jokes\n• Run code\n• Ask about time/date\n• Do math\n• Just chat naturally!\n\nCreated by Tammanna and Mairaj!",
    
    "how old are you": "I'm a new creation by Tammanna and Mairaj, but I'm learning and growing every day!",
    
    "what languages": "I can understand and respond in multiple languages! I primarily work in English, but I can help with translations too. Created by Tammanna and Mairaj!",
    
    "what is machine learning": "Machine Learning is a subset of AI where computers learn from data to make predictions or decisions. It's fascinating! Created by Tammanna and Mairaj.",
    
    "what is nlp": "NLP (Natural Language Processing) helps computers understand human language. I use it to understand your messages! Created by Tammanna and Mairaj.",
}

# Programming-related responses
PROGRAMMING_RESPONSES: Dict[str, str] = {
    "python": "Python is great! It's simple, powerful, and versatile. I can execute Python code for you - just type 'run' followed by your code.",
    "javascript": "JavaScript is essential for web development! I can help you test JavaScript code.",
    "code": "I can help with code! Type 'run' followed by your code to execute it, or 'debug' to check for errors.",
    "programming": "Programming is awesome! I can help you run and debug code. Just type 'run' followed by your code.",
    "developer": "Developers are amazing! Tammanna and Mairaj are developers who created me. I can help with coding tasks!",
}

def find_response_category(user_input: str) -> Optional[str]:
    """Find the category of the user's input"""
    text = user_input.lower().strip()
    
    # Greetings
    if any(word in text for word in ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]):
        return "greetings"
    
    # Capabilities
    if any(phrase in text for phrase in ["what can you", "what do you", "capabilities", "features", "what are you"]):
        return "capabilities"
    
    # Help
    if any(word in text for word in ["help", "how to", "how do i", "guide", "instructions"]):
        return "help"
    
    # Goodbye
    if any(word in text for word in ["bye", "goodbye", "see you", "farewell", "later"]):
        return "goodbye"
    
    # Thanks
    if any(word in text for word in ["thank", "thanks", "appreciate", "grateful"]):
        return "thanks"
    
    # How are you
    if any(phrase in text for phrase in ["how are you", "how's it going", "how do you feel"]):
        return "how_are_you"
    
    return None

def get_custom_response(category: str) -> Optional[str]:
    """Get a random custom response from a category"""
    import random
    if category in KNOWLEDGE_BASE:
        return random.choice(KNOWLEDGE_BASE[category])
    return None

def get_qa_response(user_input: str) -> Optional[str]:
    """Get response from Q&A database"""
    text = user_input.lower().strip()
    
    # Direct match
    if text in QA_DATABASE:
        return QA_DATABASE[text]
    
    # Partial match - check if any key phrase is in the input
    for key, value in QA_DATABASE.items():
        if key in text:
            return value
    
    # Programming-related
    for key, value in PROGRAMMING_RESPONSES.items():
        if key in text:
            return value
    
    return None

def get_contextual_response(user_input: str, mood: str = "neutral") -> Optional[str]:
    """Get contextual response based on mood and input"""
    text = user_input.lower().strip()
    
    # Mood-specific responses
    if mood == "sad":
        if any(word in text for word in ["help", "problem", "issue", "trouble"]):
            return "I'm sorry you're going through a tough time. I'm here to help. Would you like to talk about it, or would a joke help cheer you up? Created by Tammanna and Mairaj with care."
    
    if mood == "happy":
        if any(word in text for word in ["great", "awesome", "wonderful", "amazing"]):
            return "That's fantastic! I'm so glad you're feeling great! How can I help make your day even better? - Manna AI (by Tammanna & Mairaj)"
    
    return None
