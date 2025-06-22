from flask import Flask, request, jsonify
from acestep.pipeline_ace_step import ACEStepPipeline
import os
import base64

app = Flask(__name__)

# Initialize the ACE Step pipeline. The checkpoint will be downloaded on first use.
# If a GPU device is available, you can choose which one to use via the
# DEVICE_ID environment variable (defaults to 0).
def env_flag(name: str, default: str = "0") -> bool:
    return os.environ.get(name, default).lower() in ("1", "true", "yes")

device_id = int(os.environ.get("DEVICE_ID", 0))
torch_compile = env_flag("TORCH_COMPILE", default="1")
overlapped_decode = env_flag("OVERLAPPED_DECODE", default="1")

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
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    return jsonify({"audio_base64": audio_b64})

if __name__ == '__main__':
    # Use PORT env var if provided, otherwise default to 8000 to avoid
    # clashing with other local services that may use port 5000.
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
