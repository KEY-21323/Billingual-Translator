from flask import Flask, render_template, request
import requests
import os
import json

app = Flask(__name__)

# Use a more reliable LibreTranslate instance
TRANSLATE_URL = 'https://translate.argosopentech.com/translate'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form.get('text')
    target_lang = request.form.get('target_lang')
    translated_text = ""

    try:
        response = requests.post(
            TRANSLATE_URL,
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                'q': text,
                'source': 'auto',
                'target': target_lang,
                'format': 'text'
            })
        )
        print("Status Code:", response.status_code)
        print("Response:", response.text)

        response.raise_for_status()
        translated_text = response.json().get('translatedText', 'No translation returned.')

    except requests.exceptions.RequestException as e:
        print("Translation error:", e)
        translated_text = f"Translation error: {e}"

    return render_template('index.html', translated_text=translated_text)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
