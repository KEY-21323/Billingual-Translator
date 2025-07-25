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
    target_lang = 'fr'  # French
    translated_text = ""

    try:
        response = requests.get(
            TRANSLATE_URL,
            params={'text': text, 'dl': target_lang}
        )
        response.raise_for_status()
        data = response.json()

        translated_text = data.get('destination-text') or data.get('translation') or "No translation found"

    except requests.exceptions.RequestException as e:
        translated_text = f"Network Error: {e}"
    except ValueError:
        translated_text = "Error: Invalid response format."

    return render_template('index.html', translated_text=translated_text)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
