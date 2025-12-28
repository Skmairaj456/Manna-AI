# sentiment.py

from textblob import TextBlob

def analyze_sentiment(text: str) -> dict:
    """Return polarity and subjectivity of text"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    return {'polarity': polarity, 'subjectivity': subjectivity}

def get_mood(text: str) -> str:
    """Detect user's mood from text"""
    sentiment = analyze_sentiment(text)
    polarity = sentiment['polarity']
    
    # Determine mood based on polarity
    if polarity > 0.3:
        return "happy"
    elif polarity > 0.1:
        return "positive"
    elif polarity < -0.3:
        return "sad"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"

def get_mood_emoji(mood: str) -> str:
    """Get emoji for mood"""
    mood_emojis = {
        "happy": "😊",
        "positive": "🙂",
        "neutral": "😐",
        "negative": "😔",
        "sad": "😢"
    }
    return mood_emojis.get(mood, "😐")

def get_mood_message(mood: str) -> str:
    """Get appropriate message based on mood"""
    mood_messages = {
        "happy": "I'm glad you're feeling happy! 😊",
        "positive": "Great to see you're in a positive mood! 🙂",
        "neutral": "I'm here to help with whatever you need.",
        "negative": "I understand things might be tough. I'm here to help. 💙",
        "sad": "I'm sorry you're feeling down. Would you like to talk about it or hear a joke to cheer you up? 💙"
    }
    return mood_messages.get(mood, "")

