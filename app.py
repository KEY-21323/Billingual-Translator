from flask import Flask, render_template, request
import requests
import os
import json

app = Flask(__name__)


TRANSLATE_URL = 'https://libretranslate.de/translate'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    target_lang = request.form['target_lang']
    translated_text = ""

    payload = {
        'q': text,
        'source': 'auto',
        'target': target_lang,
        'format': 'text'
    }

    try:
        response = requests.post(
            TRANSLATE_URL,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            data = response.json()
            translated_text = data.get('translatedText', 'No translation found.')
        else:
            translated_text = f"Error: {response.status_code} - {response.text}"

    except requests.exceptions.RequestException as e:
        translated_text = f"Network Error: {e}"
    except ValueError:
        translated_text = "Error: Could not parse translation response."

    return render_template('index.html', translated_text=translated_text, input_text=text)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
