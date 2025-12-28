# voice_io.py

import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
recognizer = sr.Recognizer()

def text_to_speech(text: str):
    """Convert text to speech"""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass  # Fail silently if voice is not available

def speech_to_text() -> str:
    """Convert speech to text"""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                return ""
    except Exception:
        return ""

