import random
from core.listener import init_recognizer, listen_microphone
from core.speaker import play_voice
from logic.session_manager import SessionManager
from logic.intent_parser import IntentParser

def main():
    print("Ініціалізація Джарвіса...")
    
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
    
    print("Джарвіс перейшов у режим очікування. Скажіть 'джарвіс', щоб активувати.")

    while True:
        text = listen_microphone(recognizer, stream)
        
        # === ПЕРЕВІРКА СНУ ===
        if session.check_sleep_state():
            print("==> ЧАС ВИЙШОВ. ДЖАРВІС ЗАСНУВ <==")
            
            sleep_sounds = ["close.mp3", "out.mp3"] 
            
            stream.stop_stream() 
            play_voice(random.choice(sleep_sounds))
            stream.start_stream() 
        
        if text:
            if "джарвіс" in text:
                print("==> ДЖАРВІС АКТИВОВАНИЙ <==")
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