import os
from flask import Flask, render_template, request, jsonify
import requests

# Konfiguracja API OpenAI
api_key = "__________________________________________________________________"
whisper_url = "https://api.openai.com/v1/audio/transcriptions"
gpt_url = "https://api.openai.com/v1/chat/completions"
model_name = "gpt-4o"
max_tokens = 4096

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Endpoint główny dla wyświetlania strony HTML
@app.route('/')
def index():
    app.logger.debug("Wyświetlanie strony głównej.")
    return render_template('index.html')

# Funkcja do transkrypcji audio za pomocą Whisper i wykrycia języka
def transcribe_audio(file_path):
    app.logger.debug(f"Rozpoczęcie transkrypcji pliku audio: {file_path}")
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    with open(file_path, 'rb') as audio_file:
        files = {
            'file': (file_path, audio_file),
            'model': (None, 'whisper-1'),
            'language': (None, 'pl')  # Dodanie parametru języka polskiego
        }
        response = requests.post(whisper_url, headers=headers, files=files)
    
    if response.status_code == 200:
        response_json = response.json()
        transcription = response_json.get("text", "")
        detected_language = response_json.get("language", "Nieznany język")
        app.logger.debug(f"Transkrypcja zakończona: {transcription}")
        app.logger.debug(f"Wykryty język: {detected_language}")
        return transcription, detected_language
    else:
        app.logger.error(f"Błąd transkrypcji. Status code: {response.status_code}, Treść: {response.text}")
        return None, None


# Funkcja do komunikacji z GPT-4 i uzyskania odpowiedzi
def get_gpt_response(transcribed_text, temperature=0.1):  # Parametr kreatywności (możliwy zakres 0 - 1), czym większa temperatura tym wyższa kreatywność i losowość transkrypcji
    app.logger.debug(f"Wysyłanie tekstu do GPT-4: {transcribed_text}")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": transcribed_text
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature  # Ustawienie temperatury
    }
    
    response = requests.post(gpt_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        response_json = response.json()
        gpt_output = response_json['choices'][0]['message']['content']
        app.logger.debug(f"Odpowiedź GPT-4: {gpt_output}")
        return gpt_output
    else:
        app.logger.error(f"Błąd GPT-4. Status code: {response.status_code}, Treść: {response.text}")
        return None


# Endpoint do przesyłania plików audio i przetwarzania
@app.route('/upload', methods=['POST'])
def upload():
    app.logger.debug("Rozpoczęto przesyłanie pliku.")
    
    if 'file' not in request.files:
        app.logger.error("Brak pliku w żądaniu.")
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        app.logger.error("Nie wybrano pliku.")
        return jsonify({"error": "No selected file"}), 400
    
    # Obsługa formatów audio, w tym MP4
    if not (file.filename.lower().endswith(('.mp3', '.wav', '.mp4'))):
        app.logger.error(f"Nieobsługiwany format pliku: {file.filename}")
        return jsonify({"error": "Unsupported file format"}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    app.logger.debug(f"Plik zapisany: {filepath}")

    # Transkrypcja audio za pomocą Whisper oraz wykrycie języka
    transcribed_text, detected_language = transcribe_audio(filepath)
    
    if transcribed_text:
        # Odpowiedź GPT-4 na transkrybowany tekst
        gpt_output = get_gpt_response(transcribed_text)
        
        if gpt_output:
            # Zapis odpowiedzi do pliku
            output_file_path = os.path.splitext(filepath)[0] + ".txt"
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(gpt_output)
            app.logger.debug(f"Odpowiedź zapisana w pliku: {output_file_path}")
            return jsonify({"response": gpt_output, "detected_language": detected_language})
        else:
            app.logger.error("Błąd podczas przetwarzania odpowiedzi GPT-4.")
            return jsonify({"error": "Error processing GPT-4 response"}), 500
    else:
        app.logger.error("Błąd podczas transkrypcji pliku audio.")
        return jsonify({"error": "Error processing audio file"}), 500

if __name__ == '__main__':
    app.run(debug=True)
