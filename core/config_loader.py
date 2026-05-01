import json
import os

def load_json(filepath):
    """Універсальна функція для читання JSON файлів."""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Помилка читання {filepath}: {e}")
    else:
        print(f"Помилка: Файл {filepath} не знайдено!")
    return {}

# Завантажуємо наші конфіги у глобальні змінні
CONFIG = load_json("config.json")
USER_DATA = load_json("user_data.json")