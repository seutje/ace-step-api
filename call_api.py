import argparse
import base64
import requests


def main():
    parser = argparse.ArgumentParser(description="Call the ACE Step service")
    parser.add_argument(
        "--prompt",
        default="upbeat pop",
        help="text prompt for style (defaults to 'upbeat pop')",
    )
    parser.add_argument("--lyrics", default="", help="lyrics in ACE Step format")
    parser.add_argument(
        "--length",
        type=float,
        default=5,
        help="song length in seconds (defaults to 5)",
    )
    parser.add_argument("--output", default="song.flac", help="output audio filename")
    parser.add_argument(
        "--url",
        default="http://localhost:8000/generate",
        help="URL of the /generate endpoint",
    )
    args = parser.parse_args()

    payload = {"prompt": args.prompt, "lyrics": args.lyrics, "length": args.length}
    r = requests.post(args.url, json=payload)
    if r.status_code != 200:
        raise SystemExit(f"Request failed: {r.status_code} {r.text}")

    data = r.json()
    audio_b64 = data.get("audio_base64")
    if not audio_b64:
        raise SystemExit("Response missing audio data")

    audio_bytes = base64.b64decode(audio_b64)
    with open(args.output, "wb") as f:
        f.write(audio_bytes)
    print(f"Saved song to {args.output}")


if __name__ == "__main__":
    main()
