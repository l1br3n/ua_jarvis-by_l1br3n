import random
from core.speaker import play_voice

def respond_to_greeting():
    responses = [("always_here.mp3", "Я тут, сер."), ("online.mp3", "Системи в онлайні, чекаю вказівок.")]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)

def dady_home():
    responses = [("dady_here.mp3", "З поверненням, сер."), ("dady_home.mp3", "Вітаю дома, сер.")]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)

def respond_to_greeting2():
    responses = [("yeah.mp3", "Так, сер."), ("what_need.mp3", "Що потрібно зробити?")]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)

def respond_to_thanks():
    responses = [("your_welcome1.mp3", "Нема за що, сер."), ("no_problem.mp3", "Немає проблем, сер."), ("glad_help.mp3", "Радий бути корисним, сер.")]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)

def respond_to_chzh():
    responses = [("ya_che.mp3", "Я що ебу?."), ("da_ti.mp3", "Та ти що, базару нет")]
    chosen_sound, chosen_text = random.choice(responses)
    play_voice(chosen_sound, chosen_text)