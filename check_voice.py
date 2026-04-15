import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

print("=== Знайдені голоси в системі ===")
for index, voice in enumerate(voices):
    print(f"Індекс [{index}]: {voice.name}")