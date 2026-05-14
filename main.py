import random
import os
import threading
import queue
from web_manager.app import app

from core.listener import init_recognizer, listen_microphone
from core.speaker import play_voice
from logic.session_manager import SessionManager
from logic.intent_parser import IntentParser


# Створюємо чергу для зв'язку між Веб-сайтом і Голосовим ядром
command_queue = queue.Queue()
app.config['COMMAND_QUEUE'] = command_queue

def run_web_manager():
    # Змінили порт на 5050!
    app.run(debug=False, port=5050, use_reloader=False)

def main():
    print("Ініціалізація Джарвіса...")
    
    # ЗАПУСК ВЕБ-ІНТЕРФЕЙСУ У ФОНІ
    threading.Thread(target=run_web_manager, daemon=True).start()
    
    play_voice("porces_start.mp3")
    
    recognizer, stream = init_recognizer("resources/model")
    
    if not recognizer or not stream:
        print("Критична помилка: Не вдалося запустити мікрофон або модель.")
        play_voice("error.mp3")
        return

    session = SessionManager()
    parser = IntentParser()
    
    stream.stop_stream()
    play_voice("online.mp3")
    stream.start_stream() 
    
    print("Джарвіс перейшов у режим очікування. Скажіть 'джарвіс', щоб активувати або використовуйте WEB HUD.")

    while True:
        # === 1. ПЕРЕВІРКА КОМАНД З ВЕБ-ІНТЕРФЕЙСУ ===
        while not command_queue.empty():
            web_cmd = command_queue.get()
            print(f"==> WEB-КОМАНДА: {web_cmd}")
            
            # Прокидаємо Джарвіса, якщо він спав
            if not session.is_awake:
                session.wake_up()
                stream.stop_stream()
                play_voice("online.mp3") # Або інший звук активації
                stream.start_stream()
            else:
                session.wake_up() # Оновлюємо таймер сну
                
            stream.stop_stream()
            parser.analyze_and_execute(web_cmd)
            stream.start_stream()

        # === 2. ПЕРЕВІРКА СНУ ===
        if session.check_sleep_state():
            print("==> ЧАС ВИЙШОВ. ДЖАРВІС ЗАСНУВ <==")
            sleep_sounds = ["close.mp3", "out.mp3"] 
            stream.stop_stream() 
            play_voice(random.choice(sleep_sounds))
            stream.start_stream() 
        
        # === 3. ГОЛОСОВИЙ ВВІД ===
        text = listen_microphone(recognizer, stream)
        
        if text:
            if "джарвіс" in text:
                print("==> ДЖАРВІС АКТИВОВАНИЙ ГОЛОСОМ <==")
                session.wake_up()
                wake_sounds = ["dady_here.mp3", "yeah.mp3", "what_need.mp3", "always_here.mp3"]
                stream.stop_stream()
                play_voice(random.choice(wake_sounds))
                stream.start_stream()
                text = text.replace("джарвіс", "").strip()
            
            if session.is_awake and text:
                print(f"Команда: {text}")
                stream.stop_stream()
                parser.analyze_and_execute(text)
                stream.start_stream()

if __name__ == "__main__":
    main()