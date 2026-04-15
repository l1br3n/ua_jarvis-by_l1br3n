import os
import time
import pyperclip
import keyboard
import webbrowser
import urllib.parse
import random
from actions_static import play_voice, speak, USER_DATA

# ==========================================
# БАЗА КОНТАКТІВ ТЕЛЕГРАМ
# ==========================================
TG_CONTACTS = USER_DATA.get("telegram_contacts", {})

def send_dynamic_telegram(contact_name, message_text):
    if contact_name not in TG_CONTACTS:
        play_voice("tg_not_found.mp3", f"Контакту {contact_name} немає в моїй базі, сер.")
        return

    username = TG_CONTACTS[contact_name]
    play_voice("tg_sms.mp3", f"Надсилаю повідомлення {contact_name}, сер.")
    
    os.system(f"start tg://resolve?domain={username}")
    time.sleep(1.5) 
    pyperclip.copy(message_text.capitalize() + ".")
    keyboard.send('ctrl+v')
    time.sleep(0.2)
    keyboard.send('enter')


# ==========================================
# ЮТУБ ТА ГУГЛ ПОШУК
# ==========================================
def search_youtube_query(text):
    if "включи" in text:
        query = text.split("включи", 1)[1].strip()
    else:
        query = text.strip() 
        
    if not query:
        play_voice("youtube_what.mp3", "Що саме мені найти, сер?")
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


# ==========================================
#  ПОШУК ПЛЕЙЛИСТІВ НА СПОТІФАЙ
# ==========================================

def search_playlist_query(text):
    if "хочу" in text:
        query = text.split("хочу", 1)[1].strip()
    else:
        query = text.strip() 
        
    if not query:
        play_voice("youtube_what.mp3", "Що саме мені найти, сер?")
        return
        
    play_voice("youtube_acr.mp3", "Шукаю, сер.")
    safe_query = urllib.parse.quote(query)
    url = f"spotify:search:{safe_query}"
    webbrowser.open(url)


# ==========================================
# НАДРУКУВАТИ ТЕКСТ
# ==========================================

def type_dictated_text(text):
    trigger_words = ["надрукуй", "напиши", "введи"]
    text_to_type = text
    
    for trigger in trigger_words:
        if trigger in text:
            text_to_type = text.split(trigger, 1)[1].strip()
            break
            
    if not text_to_type:
        play_voice("youtube_what.mp3", "Що саме надрукувати, сер?")
        return
        
    responses = [
        ("your_welcome1.mp3", "Нема за що, сер."),
        ("no_problem.mp3", "Немає проблем, сер."),
        ("glad_help.mp3", "Радий бути корисним, сер.")
    ]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)
    
    pyperclip.copy(text_to_type.capitalize())
    time.sleep(0.2)
    keyboard.send('ctrl+v')


# ==========================================
# ПРИЄДНАТИСЯ ДО ДИСКОРД КАНАЛУ (ЯКЩО В БАЗІ Є ІНФА ПРО НЬОГО)
# ==========================================
DS_CHANNELS = USER_DATA.get("discord_channels", {})

def join_discord_voice(text):
    text = text.replace("каналу", "канал")
    if "канал" in text:
        remainder = text.split("канал", 1)[1].strip()
        channel_name = remainder.split()[0] if remainder else ""
    else:
        channel_name = ""
        
    if not channel_name:
        speak("До якого саме каналу підключитися, сер?")
        return

    if channel_name not in DS_CHANNELS:
        play_voice("channel_not_found.mp3", f"Каналу {channel_name} немає в моїй базі, сер.")
        return
        
    server_id, channel_id = DS_CHANNELS[channel_name]
    if channel_name == "клуб":
        play_voice("ds_club.mp3", f"Підключаюсь до каналу {channel_name}, сер.")
    if channel_name == "робота":
        play_voice("open.mp3", f"Підключаюсь до каналу {channel_name}, сер.")
    
    url = f"discord://discord.com/channels/{server_id}/{channel_id}"
    os.system(f'start "" "{url}"')
    time.sleep(2)
    keyboard.send('enter')


# ==========================================
# ВІДКРИТИ ЛЮБУ ПРОГРАМУ ЗА ЇЇ ШЛЯХОМ АБО СТІМ-ЛІНКОМ
# ==========================================

def launch_any_program(path, name):
    if not path:
        speak(f"Шлях до програми {name} не знайдено в налаштуваннях.")
        return
        
    responses = [
        ("open.mp3", f"Відкриваю {name}, сер."),
        ("sluhayus.mp3", f"Слухаюсь. Запускаю {name}."),
        ("yeah.mp3", f"Так, сер. {name} вже відкривається.")
    ]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)
    
    if path.startswith("steam://"):
        os.system(f"start {path}")
    else:
        os.system(f'start "" "{path}"')


# ==========================================
# ЗАКРИТИ ЛЮБУ ПРОГРАМУ ЗА ЇЇ ІМ'ЯМ ПРОЦЕСУ
# ==========================================

def close_any_program(process_name, name):
    responses = [
        ("close.mp3", f"Закриваю {name}, сер."),
        ("sluhayus.mp3", f"Зрозумів. {name} закрито."),
        ("yeah.mp3", f"Так, сер. Вимикаю {name}.")
    ]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)
    os.system(f"taskkill /f /im {process_name} /t >nul 2>&1")