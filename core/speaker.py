import os
import time
import random
import re
import asyncio
import tempfile
import edge_tts

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

pygame.mixer.init()

# Налаштування голосу
VOICE = "uk-UA-OstapNeural"
SPEED = "+9%"              
PITCH = "+1Hz"             

def play_voice(file_name, backup_text=""):
    """
    Програє MP3. Якщо файлу немає, можна зробити фолбек на speak_neural(backup_text).
    """
    file_path = f"resources/sounds/{file_name}"
    
    if os.path.exists(file_path):
        if backup_text:
            print(f"[Джарвіс]: (Аудіо) {backup_text}")
            
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Помилка відтворення {file_path}: {e}")
    else:
        print(f"[Помилка]: Файл {file_path} не знайдено!")
        if backup_text:
            speak_neural(backup_text)

def speak_neural(text):
    """Якісна озвучка чоловічим голосом із налаштуваннями"""
    if not text:
        return

    # Очищуємо текст від технічних символів Gemini
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

    asyncio.run(_generate())