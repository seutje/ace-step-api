from flask import Flask, request, send_file, jsonify
from acestep.pipeline_ace_step import ACEStepPipeline
import os

app = Flask(__name__)

# Initialize the ACE Step pipeline. The checkpoint will be downloaded on first use.
pipeline = ACEStepPipeline()

@app.route('/generate', methods=['POST'])
def generate_song():
    data = request.get_json(force=True)
    prompt = data.get('prompt', '')
    lyrics = data.get('lyrics', '')
    length = float(data.get('length', 60))

    # Call the ACE Step pipeline. It returns a list of generated audio file paths.
    output_paths = pipeline(
        audio_duration=length,
        prompt=prompt,
        lyrics=lyrics,
    )

    if not output_paths:
        return jsonify({'error': 'generation failed'}), 500

    audio_path = output_paths[0]
    return send_file(audio_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
