import webbrowser
import urllib.parse
from core.speaker import play_voice

def search_youtube_query(text):
    if "включи" in text:
        query = text.split("включи", 1)[1].strip()
    else:
        query = text.strip() 
        
    if not query:
        play_voice("youtube_what.mp3", "Що саме мені знайти на ютуб, сер?")
        return
        
    play_voice("youtube_acr.mp3", "Шукаю, сер.")
    safe_query = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={safe_query}"
    webbrowser.open(url)

def search_google_query(text):
    trigger_words = ["загугли", "знайди в гуглі", "знайди в гугл", "гугл", "знайди"]
    query = text
    for trigger in trigger_words:
        if trigger in text:
            query = text.split(trigger, 1)[1].strip()
            break
            
    if not query:
        play_voice("youtube_what.mp3", "Що саме мені знайти в Гугл, сер?")
        return
        
    play_voice("youtube_acr.mp3", "Шукаю в Гугл, сер.")
    safe_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={safe_query}"
    webbrowser.open(url)

def open_settings():
    play_voice("open.mp3", "Відкриваю налаштування, сер.")
    url = "http://localhost:5000/"
    webbrowser.open(url)
