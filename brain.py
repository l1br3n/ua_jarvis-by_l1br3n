import actions_static
import actions_dynamic
from actions_static import CONFIG, USER_DATA

def process_command(text):
    text = text.lower()
    words = text.split() 

    # 1. ДИНАМІЧНИЙ ТЕЛЕГРАМ
    for i, w in enumerate(words):
        if "напиш" in w or "напис" in w:
            if i + 1 < len(words):
                contact = words[i + 1]
                message = " ".join(words[i + 2:])
                
                if message:
                    actions_dynamic.send_dynamic_telegram(contact, message)
                else:
                    actions_static.play_voice("tg_what.mp3", "Що саме написати, сер?")
                return True 

    # Підтягуємо дані з конфігів
    APPS = CONFIG.get("apps", {})
    PROCESSES = CONFIG.get("processes", {})
    APP_ALIASES = USER_DATA.get("app_aliases", {})

    # 2. ДИНАМІЧНЕ ВІДКРИТТЯ ПРОГРАМ
    if any(trigger in text for trigger in ["відкр", "запуст", "го "]):
        for alias, app_key in APP_ALIASES.items():
            if alias in text:
                path = APPS.get(app_key)
                if path:
                    actions_dynamic.launch_any_program(path, alias.title())
                    return True

    # 3. ДИНАМІЧНЕ ЗАКРИТТЯ ПРОГРАМ
    if any(trigger in text for trigger in ["закр", "вируб", "за край", "за кр"]):
        for alias, app_key in APP_ALIASES.items():
            if alias in text:
                process = PROCESSES.get(app_key)
                if process:
                    actions_dynamic.close_any_program(process, alias.title())
                    return True

    # 4. СТАТИЧНІ КОМАНДИ (Керування ПК, медіа, пошук)
    COMMAND_RULES = [
        {"roots": [["пауз"], ["зупин", "муз"], ["стоп"]], "action": actions_static.pause_media},
        {"roots": [["наступн"], ["скіп"], ["перем", "трек"], ["далі"]], "action": actions_static.next_track},
        {"roots": [["попередн"], ["минул"], ["назад"]], "action": actions_static.previous_track},
        {"roots": [["тих"], ["зменш", "звук"], ["скрут"]], "action": actions_static.volume_down},
        {"roots": [["гучн"], ["збільш", "звук"], ["добав"]], "action": actions_static.volume_up},
        {"roots": [["вимкн", "мікроф"], ["мут"]], "action": actions_static.mute_microphone},
        {"roots": [["знайд"], ["гугл"], ["пошук", "гугл"]], "action": actions_dynamic.search_google_query, "has_text": True},
        {"roots": [["включ"]], "action": actions_dynamic.search_youtube_query, "has_text": True},
        {"roots": [["знай", "пісн"]], "action": actions_dynamic.search_playlist_query, "has_text": True},
        {"roots": [["канал"]], "action": actions_dynamic.join_discord_voice, "has_text": True},
        {"roots": [["надрукуй"], ["напиши", "текст"], ["введи", "текст"]], "action": actions_dynamic.type_dictated_text, "has_text": True},
        
        {"roots": [["дякую"], ["спасиб"], ["дяка"]], "action": actions_static.respond_to_thanks},
        {"roots": [["ти", "тут"], ["тут"]], "action": actions_static.respond_to_greeting},
        {"roots": [["джарвис"], ["джарвіс"], ["привіт"], ["чарльз"], ["через"]], "action": actions_static.respond_to_greeting2},
        {"roots": [["закр", "вікн"], ["закр", "програм"], ["за край", "вікн"]], "action": actions_static.close_active_program},
        {"roots": [["вимкн", "систем"], ["відключ"], ["відбій"]], "action": actions_static.shutdown_jarvis},
        {"roots": [["згорн", "вікн"], ["сховай", "вікн"]], "action": actions_static.minimize_window},
        {"roots": [["встав", "текст"], ["встав"]], "action": actions_static.paste_text},

        # Плейлисти
        {"roots": [["ранд", "плей"], ["випадк", "плейл"]], "action": actions_static.play_custom_playlist, "playlist_key": "random"},
        {"roots": [["робот", "плейлист"], ["музик", "робот"]], "action": actions_static.play_custom_playlist, "playlist_key": "робота"},
        {"roots": [["чіл", "плейлист"], ["для чіла"], ["чл"] ], "action": actions_static.play_custom_playlist, "playlist_key": "чіл"},
        {"roots": [["щасл", "плейлист"], ["для щаст"], ["щасл"] ], "action": actions_static.play_custom_playlist, "playlist_key": "щасливий"}
    ]

    # 5. ВИКОНАННЯ СТАТИЧНИХ КОМАНД
    for rule in COMMAND_RULES:
        for root_combo in rule["roots"]:
            if all(root in text for root in root_combo):
                if "playlist_key" in rule:                     
                    rule["action"](rule["playlist_key"])         
                elif rule.get("has_text"):
                    rule["action"](text) 
                else:
                    rule["action"]() 
                return True