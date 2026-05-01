import pyperclip
from google import genai
from google.genai import types
from core.config_loader import USER_DATA
from core.speaker import play_voice, speak_neural

def ask_jarvis_gemini(user_request):
    api_key = USER_DATA.get("gemini_api_key")
    if not api_key:
        play_voice("kluch.mp3", "API ключ не знайдено в налаштуваннях, сер.")
        return
    
    jarvis_prompt = USER_DATA.get("jarvis_system_prompt")
    if not jarvis_prompt:
        play_voice("promt.mp3", "Промт Джарвіса не знайдено в налаштуваннях, сер.")
        return
    
    try:
        client = genai.Client(api_key=api_key)
        
        play_voice("loading.mp3", "Обробляю ваш запит, сер.")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=user_request,
            config=types.GenerateContentConfig(
                system_instruction=jarvis_prompt,
            )
        )
        
        if response.text:
            pyperclip.copy(response.text)
            speak_neural(response.text) 
        else:
            play_voice("pomilka.mp3", "Не вдалось отримати відповідь, сер.")
            
    except Exception as e:
        print(f"[Gemini Error]: {e}")
        play_voice("pomilka.mp3", f"Помилка зв'язку, сер.")