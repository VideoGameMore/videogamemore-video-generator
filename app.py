
from flask import Flask, request, jsonify, send_from_directory
from moviepy.editor import *
import requests
import os
import uuid
import tempfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/generate', methods=['POST'])
def generate_video():
    data = request.get_json()
    script = data.get('script')
    voice_url = data.get('voice_url')

    if not script or not voice_url:
        return jsonify({'error': 'Missing script or voice_url'}), 400

    try:
        # Download the audio file into a temporary file
        response = requests.get(voice_url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to download voice file'}), 400

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_audio_file:
            tmp_audio_file.write(response.content)
            tmp_audio_path = tmp_audio_file.name

        # Load audio from the temp file
        audio = AudioFileClip(tmp_audio_path)

        # Create background video
        background = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=audio.duration)
        background = background.set_audio(audio).set_duration(audio.duration)

        output_filename = "factopia_short.mp4"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        background.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

        # Cleanup temp audio
        os.remove(tmp_audio_path)

        return jsonify({'video_url': f"{request.url_root}static/{output_filename}"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)
