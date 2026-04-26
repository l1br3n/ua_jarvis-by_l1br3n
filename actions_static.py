import os
import sys
import json
import keyboard
import pyttsx3
import spotipy
import pygame
import time
import random
import subprocess
import webbrowser
import edge_tts
import asyncio
import tempfile
import re
import os
from spotipy.oauth2 import SpotifyOAuth

# ==========================================
# ЗАВАНТАЖЕННЯ НАЛАШТУВАНЬ JSON
# ==========================================
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"[УВАГА]: Файл {filename} не знайдено! Створіть його з {filename.replace('.json', '.example.json')}")
        return {}

CONFIG = load_json('config.json')
USER_DATA = load_json('user_data.json')

# ==========================================
# ГОЛОСОВИЙ РУШІЙ (ЯДРО)
# ==========================================
engine = pyttsx3.init()
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id) 
elif len(voices) > 0:
    engine.setProperty('voice', voices[0].id)

def speak(text):
    print(f"[Джарвіс]: {text}")
    engine.say(text)
    engine.runAndWait()
    engine.stop()

pygame.mixer.init()

def play_voice(file_name, backup_text):
    file_path = f"sounds/{file_name}"
    if os.path.exists(file_path):
        print(f"[Джарвіс]: (Аудіо) {backup_text}")
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    else:
        speak(backup_text)

# ==========================================
# SPOTIFY API
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

# ==========================================
# РЕАКЦІЯ НА ПРИВІТАННЯ, ВДЯЧНІСТЬ, ВІДКЛЮЧЕННЯ
# ==========================================
def respond_to_greeting():
    responses = [("always_here.mp3", "Я тут, сер."), ("online.mp3", "Системи в онлайні, чекаю вказівок.")]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)

def dady_home():
    responses = [("dady_here.mp3", "З поверненням, сер."), ("dady_home.mp3", "Вітаю дома, сер.")]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)

def respond_to_greeting2():
    responses = [("yeah.mp3", "Так, сер."), ("what_need.mp3", "Що потрібно зробити?")]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)

def shutdown_jarvis():
    play_voice("out.mp3", "Вимикаю системи. До побачення, сер.")
    sys.exit()

def respond_to_thanks():
    responses = [("your_welcome1.mp3", "Нема за що, сер."), ("no_problem.mp3", "Немає проблем, сер."), ("glad_help.mp3", "Радий бути корисним, сер.")]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)

def respond_to_chzh():
    responses = [("ya_che.mp3", "Я че ебу?."), ("da_ti.mp3", "Да ты че, базару нет")]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)

# ==========================================
# ЗАКРТИ ПОТОЧНЕ ВІКНО
# ==========================================

def close_active_program():
    responses = [("close.mp3", "Закриваю поточне вікно, сер."), ("done.mp3", "Готово, вікно закрито.")]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)
    keyboard.send('alt+f4')


# ==========================================
# ЗГОРНЕННЯ ВІКНА
# ==========================================

def minimize_window():
    responses = [("close.mp3", "Згортаю вікно, сер."), ("sluhayus.mp3", "Слухаюсь. Вікно згорнуто.")]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)
    keyboard.send('windows+down')
    time.sleep(0.1)
    keyboard.send('windows+down')


# ==========================================
# ВСТАВИТИ ТЕКСТ З БУФЕРА ОБМІНУ
# ==========================================

def paste_text():
    responses = [("paste.mp3", "Вставляю текст, сер."), ("uspishno.mp3", "Готово.")]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)
    keyboard.send('ctrl+v')

# ==========================================
# МЕДІА ТА ЗВУК
# ==========================================
def mute_microphone():
    speak("Мікрофон вимкнено.")
    keyboard.send('ctrl+shift+m')

def pause_media():
    play_voice("zupinayu.mp3", "Зупиняю, сер.")
    keyboard.send('play/pause media')

def volume_up():
    play_voice("volume_up.mp3", "Збільшую гучність на 10%")
    for _ in range(5): keyboard.send('volume up')

def volume_down():
    play_voice("volume_down.mp3", "Зменшую гучність на 10%")
    for _ in range(5): keyboard.send('volume down')

def next_track():
    play_voice("perekl.mp3", "Переключаю, сер.")
    keyboard.send('next track')

def previous_track():
    play_voice("povert.mp3", "Повертаю, сер.")
    keyboard.send('previous track')



# ==========================================
# SPOTIFY ПЛЕЙЛИСТИ
# ==========================================
# Зчитуємо плейлисти з user_data.json
SPOTIFY_PLAYLISTS = USER_DATA.get("spotify_playlists", {})

def play_playlist_logic(playlist_uri, voice_file, backup_text):
    if not sp:
        speak("Помилка доступу до Спотіфай, сер.")
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
             speak("Не знайшов пристрою для відтворення. Відкрийте Спотіфай.")
             return
        sp.start_playback(device_id=device_id, context_uri=playlist_uri)
        print("-> [Spotify API]: Плейлист успішно запущено.")
    except Exception as e:
        print(f"[Помилка]: {e}")
        speak("Не вдалося запустити плейлист.")


def play_custom_playlist(playlist_key):
    if not SPOTIFY_PLAYLISTS:
        speak("У вашій базі немає збережених плейлистів, сер.")
        return

    if playlist_key == "random":
        playlist_key = random.choice(list(SPOTIFY_PLAYLISTS.keys()))
        voice_file, backup_text = "have_luck.mp3", "Запускаю випадковий плейлист, сер."
    else:
        if playlist_key not in SPOTIFY_PLAYLISTS:
            speak(f"Плейлиста {playlist_key} немає в базі, сер.")
            return
        #В залежності від ключа вибираємо відповідний звук та текст для озвучки
        voice_map = {
            "чіл": ("spot_chill.mp3", "Запускаю chill музику, сер."),
            "щасливий": ("open.mp3", "Відкриваю, сер."),
            "робота": ("spot_tony.mp3", "Запускаю робочу музику, сер."),
            "крутий": ("spot_cool.mp3", "Запускаю круту музику, сер.")
        }
        voice_file, backup_text = voice_map.get(playlist_key, ("open.mp3", f"Запускаю плейлист, сер."))

    playlist_uri = SPOTIFY_PLAYLISTS[playlist_key]
    play_playlist_logic(playlist_uri, voice_file, backup_text)


def open_website(url):
    play_voice("open.mp3", "Відкриваю, сер.")
    os.system(f'start "" "{url}"')


def open_project(project_name):
    projects = CONFIG.get("projects", {})
    
    if project_name in projects:
        path = projects[project_name]
        play_voice("open.mp3", f"Відкриваю проект {project_name}, сер.")
        
        try:
            subprocess.Popen(['code', path], shell=True)
            print(f"-> [Система]: Проект відкрито за шляхом {path}")
        except Exception as e:
            print(f"[Помилка]: Не вдалося відкрити проект. Деталі: {e}")
            play_voice("error.mp3", "Виникла помилка при відкритті проекту, сер.")
    else:
        play_voice("error.mp3", "Я не знайшов такого проекту в базі, сер.")



#==========================================
# Налаштування голосу
#==========================================
VOICE = "uk-UA-OstapNeural" # Чоловічий голос
SPEED = "+9%"               # Швидкість (+/-)
PITCH = "+1Hz"              # Висота голосу (зробимо трохи нижчим для солідності)
#==========================================


def speak_neural(text):
    """Якісна озвучка чоловічим голосом із налаштуваннями"""
    if not text:
        return

    # Очищуємо текст від технічних символів Gemini (зірочки, решітки)
    clean_text = re.sub(r'[*#_`-]', '', text)
    print(f"[Джарвіс]: {clean_text}")

    async def _generate():
        communicate = edge_tts.Communicate(
            text=clean_text, 
            voice=VOICE,
            rate=SPEED,
            pitch=PITCH
        )
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            await communicate.save(tmp_path)
            
            # Відтворення через твій pygame
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            pygame.mixer.music.unload()
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except:
                    pass

    # Запускаємо асинхронну функцію в звичайному коді
    asyncio.run(_generate())