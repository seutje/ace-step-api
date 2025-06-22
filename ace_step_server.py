from flask import Flask, request, send_file, jsonify
from acestep.pipeline_ace_step import ACEStepPipeline
import os

app = Flask(__name__)

# Initialize the ACE Step pipeline. The checkpoint will be downloaded on first use.
# If a GPU device is available, you can choose which one to use via the
# DEVICE_ID environment variable (defaults to 0).
def env_flag(name: str) -> bool:
    return os.environ.get(name, "0").lower() in ("1", "true", "yes")

device_id = int(os.environ.get("DEVICE_ID", 0))
torch_compile = env_flag("TORCH_COMPILE")
overlapped_decode = env_flag("OVERLAPPED_DECODE")

pipeline = ACEStepPipeline(
    device_id=device_id,
    torch_compile=torch_compile,
    overlapped_decode=overlapped_decode,
)

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
    # Use PORT env var if provided, otherwise default to 8000 to avoid
    # clashing with other local services that may use port 5000.
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
