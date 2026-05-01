import subprocess
import os

#Вкажи повний шлях до твого головного файлу

path_to_main = r"D:\jarvikkkkkkkkkkk\recomposition\main.py"

project_folder = os.path.dirname(path_to_main)

try:
    print(f"Запускаю файл: {path_to_main}...")

    subprocess.run(["python", path_to_main], cwd=project_folder, check=True)

except FileNotFoundError:
    print("Помилка: Не вдалося знайти інтерпретатор Python або вказаний файл.")
except subprocess.CalledProcessError:
    print("Помилка: Програма завершилася з помилкою.")
except Exception as e:
    print(f"Виникла непередбачена помилка: {e}")