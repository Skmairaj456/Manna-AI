# nlp_utils.py

import re

# Try to import TextBlob, but make it optional
try:
    from textblob import TextBlob
    # Download NLTK data if needed
    try:
        import nltk
        nltk.download('punkt', quiet=True)
    except:
        pass
except Exception:
    TextBlob = None

# Try to import translator, but make it optional
translator = None
try:
    from googletrans import Translator
    translator = Translator()
except Exception:
    translator = None

def clean_text(text: str) -> str:
    """Basic cleaning: remove special chars, lower case, strip spaces"""
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.lower().strip()

def detect_language(text: str) -> str:
    """Detect language code of text"""
    if translator is None:
        return 'en'  # default fallback if translator not available
    try:
        lang = translator.detect(text).lang
        return lang
    except Exception:
        return 'en'  # default fallback

def translate_text(text: str, dest: str = 'en') -> str:
    """Translate text to destination language"""
    if dest == 'en' or translator is None:
        return text
    try:
        translation = translator.translate(text, dest=dest)
        return translation.text
    except Exception:
        return text

