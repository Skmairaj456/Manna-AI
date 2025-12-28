# joke_manager.py

import random

jokes = [
    "Why don't scientists trust atoms? Because they make up everything! - Brought to you by Tammanna and Mairaj 😄",
    "Why did the computer show up at work late? It had a hard drive! - Courtesy of Tammanna and Mairaj 🚀",
    "Why do programmers prefer dark mode? Because light attracts bugs! - From Tammanna and Mairaj 💻",
    "What do you call a programmer from Finland? Nerdic! - Joke by Tammanna and Mairaj 🎯",
    "How do you comfort a JavaScript bug? You console it! - Thanks to Tammanna and Mairaj 🐛",
    "Why did Tammanna and Mairaj become developers? Because they wanted to make the world a better place, one line of code at a time! 💡",
]

def get_joke() -> str:
    return random.choice(jokes)

