import json
import pyaudio
import os
from vosk import Model, KaldiRecognizer
from brain import process_command 
import actions_static
import random
import time
from actions_static import speak, play_voice

MODEL_PATH = "model"

if not os.path.exists(MODEL_PATH):
    print(f"\n[ПОМИЛКА]: Не знайдено папку '{MODEL_PATH}'. Переконайтеся, що вона лежить поруч з main.py.")
    exit(1)

print("Завантаження мовної моделі... (Це займе пару секунд)")
model = Model(MODEL_PATH)
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, 
                channels=1, 
                rate=16000, 
                input=True, 
                frames_per_buffer=8000)
stream.start_stream()

print("\n========================================")
print("[Джарвіс]: Режим очікування (WWD). Скажіть 'Джарвіс', щоб активувати.")
print("========================================\n")

is_awake = False
WAKE_WORDS = ["джарвіс", "чарльз", "через"]
ACTIVE_TIMEOUT = 45  # Секунди безперервного слухання
activation_time = None  # Час активації 

def is_wake_word_spoken(text):
    for wake_word in WAKE_WORDS:
        if wake_word in text:
            return True
    return False

def is_active_session_valid():
    """Перевіряє чи ще тривает активна сесія (45 секунд)"""
    global activation_time
    if activation_time is None:
        return False
    elapsed = time.time() - activation_time
    return elapsed < ACTIVE_TIMEOUT

def process_voice_command(recognized_text):
    global is_awake, activation_time
    text = recognized_text.strip().lower()
    if not text:
        return

    # Режим очікування (WWD) - чекаємо на слово активації
    if not is_awake:
        if is_wake_word_spoken(text):
            is_awake = True
            activation_time = time.time()
            print("\n[Джарвіс]: Системи активовано. Слухаю команди...")
            responses = [("online.mp3", "Системи онлайн, чекаю вказівок."), ("yeah.mp3", "Так точно."), ("what_need.mp3", "Що потрібно зробити?")]
            chosen_sound, chosen_text = random.choice(responses)
            actions_static.play_voice(chosen_sound, chosen_text)
            rec.Reset()
        return

    # Режим активної сесії - обробляємо команди
    if is_awake and is_active_session_valid():
        print(f"[Почув команду]: {text}")
        stream.stop_stream()
        
        command_executed = process_command(text)
        
        if not command_executed:
            print("[Джарвіс]: Команду не розпізнано.")
        
        rec.Reset()
        stream.start_stream()
        return
    
    # Сесія закінчилась - повертаємось в режим очікування
    if is_awake and not is_active_session_valid():
        is_awake = False
        activation_time = None
        print("\n[Джарвіс]: Час активної сесії закінчився. Переходжу в режим очікування...")
        rec.Reset()

try:
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            recognized_text = result.get("text", "")
            process_voice_command(recognized_text)
            
except KeyboardInterrupt:
    print("\n[Джарвіс]: Відключаю системи. До побачення!")
    stream.stop_stream()
    stream.close()
    p.terminate()