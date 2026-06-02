import os
import tempfile
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from audio_processor import AudioProcessor
from transcriber import Transcriber
from summarizer import Summarizer
from email_generator import EmailGenerator

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = tempfile.mkdtemp()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

audio_processor = AudioProcessor()
transcriber = Transcriber()
summarizer = Summarizer()
email_generator = EmailGenerator()


@app.route('/api/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        return jsonify({
            'message': 'File uploaded successfully',
            'filename': filename,
            'filepath': filepath
        }), 200


@app.route('/api/process', methods=['POST'])
def process_audio():
    data = request.json
    filepath = data.get('filepath')
    teacher_name = data.get('teacher_name', '老师')

    if not filepath or not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    cleaned_audio = audio_processor.remove_tapping_noise(filepath)
    diarization = transcriber.diarize_speakers(cleaned_audio)
    teacher_segments = transcriber.extract_teacher_segments(diarization, teacher_name)
    transcription = transcriber.transcribe_segments(cleaned_audio, teacher_segments)
    summary = summarizer.generate_summary(transcription)
    tutorial = summarizer.generate_tutorial(summary)
    materials = summarizer.generate_materials_list(summary)
    markdown_email = email_generator.generate_markdown_email(
        teacher_name, transcription, summary, tutorial, materials
    )

    return jsonify({
        'transcription': transcription,
        'summary': summary,
        'tutorial': tutorial,
        'materials': materials,
        'markdown_email': markdown_email
    }), 200


@app.route('/api/patterns/<pattern_name>')
def get_pattern(pattern_name):
    patterns_dir = os.path.join(os.path.dirname(__file__), '../shared/patterns')
    return send_from_directory(patterns_dir, pattern_name)


@app.route('/api/patterns')
def list_patterns():
    patterns_dir = os.path.join(os.path.dirname(__file__), '../shared/patterns')
    patterns = []
    for f in os.listdir(patterns_dir):
        if f.endswith('.svg'):
            patterns.append({
                'name': f.replace('.svg', ''),
                'file': f
            })
    return jsonify(patterns)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
