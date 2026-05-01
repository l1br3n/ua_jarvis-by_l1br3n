import os
import sys
import time
import random
import subprocess
import keyboard
import pyperclip
from core.config_loader import CONFIG
from core.speaker import play_voice

def shutdown_jarvis():
    play_voice("out.mp3", "Вимикаю системи. До побачення, сер.")
    sys.exit()

def close_active_program():
    responses = [("close.mp3", "Закриваю поточне вікно, сер."), ("done.mp3", "Готово, вікно закрито.")]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)
    keyboard.send('alt+f4')

def minimize_window():
    responses = [("close.mp3", "Згортаю вікно, сер."), ("sluhayus.mp3", "Слухаюсь. Вікно згорнуто.")]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)
    keyboard.send('windows+down')
    time.sleep(0.1)
    keyboard.send('windows+down')

def paste_text():
    responses = [("paste.mp3", "Вставляю текст, сер."), ("uspishno.mp3", "Готово.")]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)
    keyboard.send('ctrl+v')

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

def mute_microphone():
    play_voice("done.mp3", "Мікрофон вимкнено.")
    keyboard.send('ctrl+shift+m')

def volume_up():
    play_voice("volume_up.mp3", "Збільшую гучність на 10%")
    for _ in range(5): keyboard.send('volume up')

def volume_down():
    play_voice("volume_down.mp3", "Зменшую гучність на 10%")
    for _ in range(5): keyboard.send('volume down')

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

def launch_any_program(path, name):
    if not path:
        play_voice("error.mp3", f"Шлях до програми {name} не знайдено.")
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

def close_any_program(process_name, name):
    responses = [
        ("close.mp3", f"Закриваю {name}, сер."),
        ("sluhayus.mp3", f"Зрозумів. {name} закрито."),
        ("yeah.mp3", f"Так, сер. Вимикаю {name}.")
    ]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)
    os.system(f"taskkill /f /im {process_name} /t >nul 2>&1")