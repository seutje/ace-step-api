# ACE Step Flask API

This repository exposes the [ACE Step](https://github.com/ace-step/ACE-Step) music generation model through a simple Flask server.

## Usage

1. Install dependencies using `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the server (defaults to port 8000):

   ```bash
   python ace_step_server.py
   ```
   
   You can override the port by setting the `PORT` environment variable.
   To choose which GPU to run on, set `DEVICE_ID` (defaults to `0`). If no GPU is
   available the server will fall back to CPU.
   `torch.compile()` and overlapped decoding are enabled by default. Set
   `TORCH_COMPILE=0` or `OVERLAPPED_DECODE=0` to disable these features.

3. Generate music by sending a POST request to `/generate` with a JSON body containing `prompt`, `lyrics` and `length` (in seconds). The server returns the generated audio in FLAC format.

## Endpoint Example

```bash
curl -X POST http://localhost:8000/generate \
     -H 'Content-Type: application/json' \
     -d '{"prompt": "upbeat pop", "lyrics": "[verse]\nHello world", "length": 5}' \
     --output song.flac
```

Alternatively, you can call the server from Python using the provided script:

```bash
python call_api.py --prompt "upbeat pop" --lyrics "[verse]\nHello world" --length 5 --output song.flac
```
