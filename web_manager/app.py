from flask import Flask, request, render_template, redirect, url_for, jsonify
import json
import os
import logging  

app = Flask(__name__)

# Вимикаємо логування
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USER_DATA_FILE = os.path.join(BASE_DIR, 'user_data.json')
CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')

def load_json(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    data_user = load_json(USER_DATA_FILE)
    data_config = load_json(CONFIG_FILE)
    return render_template('index.html', data_user=data_user, data_config=data_config)

@app.route('/update', methods=['POST'])
def update():
    data_user = load_json(USER_DATA_FILE)
    data_config = load_json(CONFIG_FILE)

    # Універсальна функція для звичайних списків (словників)
    def process_lists(names_key, values_key):
        names = request.form.getlist(names_key)
        values = request.form.getlist(values_key)
        return {n.strip(): v.strip() for n, v in zip(names, values) if n.strip() and v.strip()}

    def process_discord():
        names = request.form.getlist('discord_names')
        ids_raw = request.form.getlist('discord_ids')
        result = {}
        for n, ids in zip(names, ids_raw):
            n = n.strip()
            if n and ids.strip():
                id_list = [i.strip() for i in ids.split(',')]
                result[n] = id_list
        return result

    # --- Оновлюємо дані user_data.json ---
    def process_playlists():
        names = request.form.getlist('playlist_names')
        links = request.form.getlist('playlist_links')
        voices = request.form.getlist('playlist_voices')
        result = {}
        for n, l, v in zip(names, links, voices):
            n = n.strip()
            if n and l.strip():
                result[n] = {
                    "uri": l.strip(),
                    "voice": v.strip()
                }
        return result

    data_user['spotify_playlists'] = process_playlists()

    data_user['telegram_contacts'] = process_lists('tg_names', 'tg_users')
    data_user['app_aliases'] = process_lists('alias_names', 'alias_targets')
    data_user['discord_channels'] = process_discord()
    

    data_user['gemini_api_key'] = request.form.get('gemini_api_key', '').strip()
    data_user['jarvis_system_prompt'] = request.form.get('jarvis_system_prompt', '').strip()


    data_config['apps'] = process_lists('app_names', 'app_paths')
    data_config['projects'] = process_lists('proj_names', 'proj_paths')


    if 'spotify' not in data_config:
        data_config['spotify'] = {}
    data_config['spotify']['client_id'] = request.form.get('spotify_client_id', '').strip()
    data_config['spotify']['client_secret'] = request.form.get('spotify_client_secret', '').strip()
    data_config['spotify']['redirect_uri'] = request.form.get('spotify_redirect_uri', '').strip()

    # Зберігаємо все назад у файли
    save_json(USER_DATA_FILE, data_user)
    save_json(CONFIG_FILE, data_config)

    return redirect(url_for('index'))

# ===================================================
# НОВИЙ КОД: РОУТ ДЛЯ ГОЛОВНОГО ІНТЕРФЕЙСУ JARVIS
# ===================================================
@app.route('/jarvis')
def jarvis_ui():
    return render_template('jarvis.html')
# ===================================================

# Зберігаємо історію команд для відображення в HUD
command_history = []

@app.route('/api/command', methods=['POST'])
def receive_command():
    data = request.get_json()
    command = data.get('command')
    
    if command:
        # Додаємо в історію
        command_history.append(f"> {command}")
        
        # Передаємо команду в main.py через чергу
        if 'COMMAND_QUEUE' in app.config:
            app.config['COMMAND_QUEUE'].put(command)
            
        return jsonify({"status": "success", "command": command})
    return jsonify({"status": "error"}), 400

@app.route('/api/history', methods=['GET'])
def get_history():
    # Повертаємо останні 5 команд
    return jsonify(command_history[-5:])
if __name__ == '__main__':
    print("=====================================================")
    print("🌐 Менеджер Джарвіса запущено!")
    print("Відкрий посилання у браузері: http://127.0.0.1:5050") # ТУТ
    print("=====================================================\n")
    app.run(debug=True, port=5050) # І ТУТ