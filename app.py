from flask import Flask, render_template, request, jsonify
import requests
import os
import json

app = Flask(__name__)

TRANSLATE_URL = 'https://libretranslate.com/translate'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    target_lang = request.form['target_lang']

    payload = {
        'q': text,
        'source': 'auto',
        'target': target_lang,
        'format': 'text'
    }

    try:
        response = requests.post(
    'https://libretranslate.com/translate',
    headers={'Content-Type': 'application/json'},
    data=json.dumps({
        'q': text,
        'source': source_lang,
        'target': target_lang,
        'format': 'text'
    })
)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
