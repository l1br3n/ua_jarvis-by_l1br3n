import json
import pyaudio
from vosk import Model, KaldiRecognizer

def init_recognizer(model_path="model"):
    """Завантажує модель та налаштовує мікрофон."""
    print("Завантаження мовної моделі Vosk...")
    try:
        model = Model(model_path)
        recognizer = KaldiRecognizer(model, 16000)
    except Exception as e:
        print(f"Помилка завантаження моделі (перевір чи є папка '{model_path}'): {e}")
        return None, None

    print("Налаштування мікрофона...")
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8000
    )
    stream.start_stream()
    return recognizer, stream

def listen_microphone(recognizer, stream):
    """Слухає мікрофон і повертає розпізнаний текст."""
    if not recognizer or not stream:
        return ""

    try:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").strip()
            return text.lower()
    except Exception as e:
        print(f"Помилка мікрофона: {e}")
        
    return ""