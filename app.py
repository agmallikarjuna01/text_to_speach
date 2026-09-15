from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gtts import gTTS
from pypdf import PdfReader

app=Flask(__name__)

CORS(app)

@app.route('/')
def home():
    return send_from_directory('front', 'index.html')

@app.route('/api/convert', methods=['POST'])
def process():
    uploaded_file = request.files.get('file')

    if uploaded_file and uploaded_file.filename:
        filename = uploaded_file.filename.lower()
        if filename.endswith('.txt'):
            result = uploaded_file.read().decode('utf-8')
        elif filename.endswith('.pdf'):
            reader = PdfReader(uploaded_file.stream)
            result = '\n'.join(page.extract_text() or '' for page in reader.pages)
        else:
            return jsonify({'error': 'Only PDF and TXT files are supported.'}), 400
    else:
        data = request.get_json(silent=True) or {}
        result = request.form.get('name', data.get('name', '')).strip()

    if not result.strip():
        return jsonify({'error': 'The uploaded file does not contain readable text.'}), 400

    tts = gTTS(text=result, lang='en')
    tts.save("output.mp3")
    return send_from_directory('.', 'output.mp3')
if __name__=="__main__":
    app.run(debug=True,port=5000)