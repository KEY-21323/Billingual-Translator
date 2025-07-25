from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

TRANSLATE_URL = 'https://ftapi.pythonanywhere.com/translate'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form.get('text', '')
    target_lang = request.form.get('target_lang', 'en')
    source_lang = 'auto'
    translated_text = ""

    try:
        response = requests.get(
            TRANSLATE_URL,
            params={
                'text': text,
                'sl': source_lang,
                'dl': target_lang
            }
        )
        response.raise_for_status()
        json_response = response.json()
        translated_text = json_response.get('translated_text') or json_response.get('translation') or "No translation found."

    except requests.exceptions.RequestException as e:
        translated_text = f"Network Error: {e}"
    except ValueError:
        translated_text = "Error: Unexpected response format."

    return render_template('index.html', translated_text=translated_text)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
