# voice_io.py
# Voice features are optional and may not work in serverless environments

def text_to_speech(text: str):
    """Convert text to speech (optional - not available in serverless)"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass  # Fail silently if voice is not available

def speech_to_text() -> str:
    """Convert speech to text (optional - browser-based only in serverless)"""
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
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

