# nlp_utils.py

import re

# Lazy loading - don't import until needed
TextBlob = None
translator = None

def _get_textblob():
    """Lazy load TextBlob"""
    global TextBlob
    if TextBlob is None:
        try:
            from textblob import TextBlob as TB
            TextBlob = TB
        except Exception:
            pass
    return TextBlob

def _get_translator():
    """Lazy load translator"""
    global translator
    if translator is None:
        try:
            from googletrans import Translator
            translator = Translator()
        except Exception:
            translator = False  # Use False to indicate failed import
    return translator

def clean_text(text: str) -> str:
    """Basic cleaning: remove special chars, lower case, strip spaces"""
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.lower().strip()

def detect_language(text: str) -> str:
    """Detect language code of text"""
    trans = _get_translator()
    if not trans:
        return 'en'  # default fallback if translator not available
    try:
        lang = trans.detect(text).lang
        return lang
    except Exception:
        return 'en'  # default fallback

def translate_text(text: str, dest: str = 'en') -> str:
    """Translate text to destination language"""
    if dest == 'en':
        return text
    trans = _get_translator()
    if not trans:
        return text
    try:
        translation = trans.translate(text, dest=dest)
        return translation.text
    except Exception:
        return text

