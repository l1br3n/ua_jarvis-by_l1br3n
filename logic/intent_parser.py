from core.config_loader import CONFIG, USER_DATA
from core.speaker import play_voice
from skills import system_tools, web_search, media_control, chat_actions, communication, ai_handler

class IntentParser:
    def __init__(self):
        self.COMMAND_RULES = [
            {"roots": [["пауз"], ["зупин", "муз"], ["стоп"]], "action": media_control.pause_media},
            {"roots": [["наступн"], ["скіп"], ["перем", "трек"], ["далі"]], "action": media_control.next_track},
            {"roots": [["попередн"], ["минул"], ["назад"]], "action": media_control.previous_track},
            {"roots": [["тих"], ["зменш", "звук"], ["скрут"]], "action": system_tools.volume_down},
            {"roots": [["гучн"], ["збільш", "звук"], ["добав"]], "action": system_tools.volume_up},
            {"roots": [["вимкн", "мікроф"], ["мут"]], "action": system_tools.mute_microphone},
            {"roots": [["знайд"], ["гугл"], ["пошук", "гугл"]], "action": web_search.search_google_query, "has_text": True},
            {"roots": [["включ"]], "action": web_search.search_youtube_query, "has_text": True},
            {"roots": [["знай", "пісн"]], "action": media_control.search_playlist_query, "has_text": True},
            {"roots": [["канал"]], "action": communication.join_discord_voice, "has_text": True},
            {"roots": [["надрукуй"], ["напиши", "текст"], ["введи", "текст"], ["напиш"], ["надрукуй"]], "action": system_tools.type_dictated_text, "has_text": True},
            
            {"roots": [["відкрий", "чат"], ["відкрий", "чат"], ["чат"], ["чад"]], "action": lambda: system_tools.open_website(CONFIG["websites"]["чат"])},
            {"roots": [["дякую"], ["спасиб"], ["дяка"]], "action": chat_actions.respond_to_thanks},
            {"roots": [["що", "за", "фіг"], ["фіг"]], "action": chat_actions.respond_to_chzh},
            {"roots": [["ти", "тут"], ["тут"]], "action": chat_actions.respond_to_greeting},
            {"roots": [["Тато", "дома"], ["дома"]], "action": chat_actions.dady_home},
            {"roots": [["джарвис"], ["джарвіс"], ["привіт"], ["чарльз"], ["через"]], "action": chat_actions.respond_to_greeting2},
            {"roots": [["закр", "вікн"], ["закр", "програм"], ["за край", "вікн"]], "action": system_tools.close_active_program},
            {"roots": [["вимкн", "систем"], ["відключ"], ["відбій"]], "action": system_tools.shutdown_jarvis},
            {"roots": [["згорн", "вікн"], ["сховай", "вікн"]], "action": system_tools.minimize_window},
            {"roots": [["встав", "текст"], ["встав"]], "action": system_tools.paste_text},
            {"roots": [["запус", "проект"], ["проект"]], "action": system_tools.open_project, "has_text": True},
            
            # Плейлисти
            {"roots": [["ранд", "плей"], ["випадк", "плейл"]], "action": media_control.play_custom_playlist, "playlist_key": "random"},
            {"roots": [["робот", "плейлист"], ["музик", "робот"]], "action": media_control.play_custom_playlist, "playlist_key": "робота"},
            {"roots": [["чіл", "плейлист"], ["для чіла"], ["чл"] ], "action": media_control.play_custom_playlist, "playlist_key": "чіл"},
            {"roots": [["щасл", "плейлист"], ["для щаст"], ["щасл"] ], "action": media_control.play_custom_playlist, "playlist_key": "щасливий"},
            {"roots": [["крутий", "плейлист"], ["крутий"]], "action": media_control.play_custom_playlist, "playlist_key": "крутий"},

            {"roots": [["розка"]], "action": ai_handler.ask_jarvis_gemini, "has_text": True}
        ]

    def analyze_and_execute(self, text):
        text = text.lower()
        words = text.split() 

        # 1. ДИНАМІЧНИЙ ТЕЛЕГРАМ
        for i, w in enumerate(words):
            if "напиш" in w or "напис" in w:
                if i + 1 < len(words):
                    contact = words[i + 1]
                    message = " ".join(words[i + 2:])
                    
                    if message:
                        communication.send_dynamic_telegram(contact, message)
                    else:
                        play_voice("tg_what.mp3") 
                    return True 

        # Підтягуємо дані з конфігів
        APPS = CONFIG.get("apps", {})
        PROCESSES = CONFIG.get("processes", {})
        APP_ALIASES = USER_DATA.get("app_aliases", {})

        # 2. ДИНАМІЧНЕ ВІДКРИТТЯ ПРОГРАМ
        trigger_open = ["відкр", "запуст", "го"]
        if any(any(trig in w for w in words) for trig in trigger_open):
            for alias, app_key in APP_ALIASES.items():
                if alias in text:
                    path = APPS.get(app_key)
                    if path:
                        system_tools.launch_any_program(path, alias.title())
                        return True

        # 3. ДИНАМІЧНЕ ЗАКРИТТЯ ПРОГРАМ
        trigger_close = ["закр", "вируб", "за край", "за кр"]
        if any(any(trig in w for w in words) for trig in trigger_close):
            for alias, app_key in APP_ALIASES.items():
                if alias in text:
                    process = PROCESSES.get(app_key)
                    if process:
                        system_tools.close_any_program(process, alias.title())
                        return True

        # 5. ВИКОНАННЯ СТАТИЧНИХ КОМАНД (Стандартний пошук)
        for rule in self.COMMAND_RULES:
            for root_combo in rule["roots"]:
                match_all = True
                
                for root in root_combo:
                    root_matched = False
                    # Обробка складених коренів, які мають пробіл
                    if " " in root:
                        if root in text:
                            root_matched = True
                    else:
                        for w in words:
                            if root in w:  # Проста перевірка на входження
                                root_matched = True
                                break
                                
                    if not root_matched:
                        match_all = False
                        break
                        
                if match_all:
                    if "playlist_key" in rule:                     
                        rule["action"](rule["playlist_key"])          
                    elif rule.get("has_text"):
                        rule["action"](text) 
                    else:
                        rule["action"]() 
                    return True
                    
        return False