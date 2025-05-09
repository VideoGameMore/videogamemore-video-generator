
from flask import Flask, request, jsonify, send_from_directory
from moviepy.editor import *
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

# ✅ Create the static folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/generate', methods=['POST'])
def generate_video():
    data = request.get_json()
    script = data.get('script')
    voice_url = data.get('voice_url')

    if not script or not voice_url:
        return jsonify({'error': 'Missing script or voice_url'}), 400

    try:
        # Download the voice file
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'voice.mp3')
        with open(audio_path, 'wb') as f:
            f.write(requests.get(voice_url).content)

        # Create a background video clip
        background = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=15)
        audio = AudioFileClip(audio_path)
        background = background.set_audio(audio).set_duration(audio.duration)

        # Generate unique output filename
        output_filename = f"factopia_short.mp4"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        background.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

        return jsonify({'video_url': f"{request.url_root}static/{output_filename}"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)
