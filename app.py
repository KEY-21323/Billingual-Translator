from flask import Flask, render_template, request, jsonify
import requests
import os

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
        response = requests.post(TRANSLATE_URL, data=payload)
        response.raise_for_status()
        translated_text = response.json()['translatedText']
        return jsonify({'translated_text': translated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
