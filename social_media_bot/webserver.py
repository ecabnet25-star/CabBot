from flask import Flask, render_template, request, jsonify
from scheduler import schedule_post
from poster import post_to_platforms
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/schedule', methods=['POST'])
def api_schedule():
    data = request.json
    text = data.get('text')
    platforms = data.get('platforms', [])
    dt = data.get('datetime')
    if not text or not platforms or not dt:
        return jsonify({'success': False, 'error': 'Missing fields'}), 400
    schedule_post(text, platforms, dt)
    return jsonify({'success': True})

@app.route('/api/post', methods=['POST'])
def api_post():
    data = request.json
    text = data.get('text')
    platforms = data.get('platforms', [])
    if not text or not platforms:
        return jsonify({'success': False, 'error': 'Missing fields'}), 400
    post_to_platforms(text, platforms)
    return jsonify({'success': True})

# Start Flask in a thread so it doesn't block the desktop app

def run_flask():
    app.run(debug=False, port=5000)

def start_web_server():
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

# To use: import and call start_web_server() from your main app
