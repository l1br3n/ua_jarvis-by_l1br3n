import os
import time
import json
import random
import pyperclip
import keyboard
from core.config_loader import USER_DATA
from core.speaker import play_voice

TG_CONTACTS = USER_DATA.get("telegram_contacts", {})
DS_CHANNELS = USER_DATA.get("discord_channels", {})

SUCCESS_SOUNDS = ["sluhayus.mp3", "done.mp3", "yeah.mp3", "uspishno.mp3"]

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

def join_discord_voice(text):
    text = text.replace("каналу", "канал")
    if "канал" in text:
        remainder = text.split("канал", 1)[1].strip()
        channel_name = remainder.split()[0] if remainder else ""
    else:
        channel_name = ""
        
    if not channel_name:
        play_voice("error.mp3", "До якого саме каналу підключитися, сер?")
        return

    if channel_name not in DS_CHANNELS:
        play_voice("channel_not_found.mp3", f"Каналу {channel_name} немає в моїй базі, сер.")
        return
        
    server_id, channel_id = DS_CHANNELS[channel_name]
    
    # Вибираємо рандомний звук замість хардкоду конкретного файлу
    voice_file = random.choice(SUCCESS_SOUNDS)
    play_voice(voice_file, f"Підключаюсь до каналу {channel_name}, сер.")
    
    url = f"discord://discord.com/channels/{server_id}/{channel_id}"
    os.system(f'start "" "{url}"')
    time.sleep(2)
    keyboard.send('enter')