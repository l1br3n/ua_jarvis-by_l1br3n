import json
import pyaudio
import os
from vosk import Model, KaldiRecognizer
from brain import process_command 

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
print("[Джарвіс]: Асистент активний. Готовий слухати.")
print("========================================\n")

def process_voice_command(recognized_text):
    text = recognized_text.strip()
    if not text:
        return

    for name in ["джарвіс", "чарльз", "через"]:
        if text.startswith(name):
            text = text.replace(name, "", 1).strip()
            break

    print(f"[Почув]: {text}")
    
    stream.stop_stream()
    process_command(text)
    rec.Reset()
    stream.start_stream()

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