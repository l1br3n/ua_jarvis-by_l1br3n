import keyboard
import random
import webbrowser
import urllib.parse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from core.config_loader import CONFIG, USER_DATA
from core.speaker import play_voice

# ==========================================
# ІНІЦІАЛІЗАЦІЯ SPOTIFY API
# ==========================================
SPOTIPY_CLIENT_ID = CONFIG.get("spotify", {}).get("client_id", "")
SPOTIPY_CLIENT_SECRET = CONFIG.get("spotify", {}).get("client_secret", "")
SPOTIPY_REDIRECT_URI = CONFIG.get("spotify", {}).get("redirect_uri", "")

try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="user-modify-playback-state user-read-playback-state"
    ))
except Exception as e:
    print(f"[Помилка]: Не вдалося підключитися до Spotify API. Деталі: {e}")
    sp = None

SPOTIFY_PLAYLISTS = USER_DATA.get("spotify_playlists", {})

def pause_media():
    play_voice("zupinayu.mp3", "Зупиняю, сер.")
    keyboard.send('play/pause media')

def next_track():
    play_voice("perekl.mp3", "Переключаю, сер.")
    keyboard.send('next track')

def previous_track():
    play_voice("povert.mp3", "Повертаю, сер.")
    keyboard.send('previous track')

def search_playlist_query(text):
    if "хочу" in text:
        query = text.split("хочу", 1)[1].strip()
    else:
        query = text.strip() 
        
    if not query:
        play_voice("youtube_what.mp3", "Що саме мені знайти, сер?")
        return
        
    play_voice("youtube_acr.mp3", "Шукаю, сер.")
    safe_query = urllib.parse.quote(query)
    url = f"spotify:search:{safe_query}"
    webbrowser.open(url)

def play_playlist_logic(playlist_uri, voice_file, backup_text):
    if not sp:
        play_voice("error.mp3", "Помилка доступу до Спотіфай, сер.")
        return
        
    play_voice(voice_file, backup_text)
    try:
        devices = sp.devices()
        device_id = None
        if devices['devices']:
            for d in devices['devices']:
                if d['is_active']:
                    device_id = d['id']
                    break
            if not device_id:
                device_id = devices['devices'][0]['id']
                
        if not device_id:
             play_voice("error.mp3", "Не знайшов пристрою для відтворення. Відкрийте Спотіфай.")
             return
             
        sp.start_playback(device_id=device_id, context_uri=playlist_uri)
        print("-> [Spotify API]: Плейлист успішно запущено.")
    except Exception as e:
        print(f"[Помилка]: {e}")
        play_voice("error.mp3", "Не вдалося запустити плейлист.")

def play_custom_playlist(playlist_key):
    if not SPOTIFY_PLAYLISTS:
        play_voice("error.mp3", "У вашій базі немає збережених плейлистів, сер.")
        return

    if playlist_key == "random":
        playlist_key = random.choice(list(SPOTIFY_PLAYLISTS.keys()))
        voice_file, backup_text = "have_luck.mp3", "Запускаю випадковий плейлист, сер."
    else:
        if playlist_key not in SPOTIFY_PLAYLISTS:
            play_voice("error.mp3", f"Плейлиста {playlist_key} немає в базі, сер.")
            return
            
        voice_map = {
            "Назва плейлиста": ("озвучка для конкретного плейлиста", "Запускаю плейлист, сер.")
        }
        voice_file, backup_text = voice_map.get(playlist_key, ("open.mp3", f"Запускаю плейлист, сер."))

    playlist_uri = SPOTIFY_PLAYLISTS[playlist_key]
    play_playlist_logic(playlist_uri, voice_file, backup_text)