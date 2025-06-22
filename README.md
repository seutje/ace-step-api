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

3. Generate music by sending a POST request to `/generate` with a JSON body containing `prompt`, `lyrics` and `length` (in seconds). The server returns the generated audio file.

## Endpoint Example

```bash
curl -X POST http://localhost:8000/generate \
     -H 'Content-Type: application/json' \
     -d '{"prompt": "upbeat pop", "lyrics": "[verse]\nHello world", "length": 5}' \
     --output song.flac
```
