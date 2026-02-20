#!/usr/bin/env python3
"""Transcribe a BiP session recording using Deepgram's Nova-3 model.

Usage: /usr/bin/python3 scripts/transcribe.py <session-dir>
Example: /usr/bin/python3 scripts/transcribe.py 2-13-26

Reads DEEPGRAM_API_KEY from .env.local at the project root.
If only an .mp4 exists in the session directory, extracts audio to .mp3 first.
Saves the full Deepgram response as deepgram.json in the session directory,
then auto-runs the analyze script.
"""

import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent


def load_api_key():
    """Load DEEPGRAM_API_KEY from .env.local at the project root."""
    env_file = PROJECT_DIR / ".env.local"
    if not env_file.exists():
        print(f"Error: .env.local not found at {env_file}")
        sys.exit(1)

    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("DEEPGRAM_API_KEY="):
            value = line.split("=", 1)[1].strip()
            # Strip surrounding quotes if present
            if len(value) >= 2 and value[0] in ('"', "'") and value[-1] == value[0]:
                value = value[1:-1]
            if not value:
                print("Error: DEEPGRAM_API_KEY is empty in .env.local")
                sys.exit(1)
            return value

    print("Error: DEEPGRAM_API_KEY not found in .env.local")
    sys.exit(1)


def find_audio(session_dir):
    """Find or extract an mp3 from the session directory."""
    mp3_files = list(session_dir.glob("*.mp3"))
    if mp3_files:
        print(f"Found audio: {mp3_files[0].name}")
        return mp3_files[0]

    mp4_files = list(session_dir.glob("*.mp4"))
    if not mp4_files:
        print(f"Error: no .mp3 or .mp4 found in {session_dir}")
        sys.exit(1)

    mp4_path = mp4_files[0]
    mp3_path = mp4_path.with_suffix(".mp3")
    print(f"No mp3 found. Extracting audio from {mp4_path.name}...")

    result = subprocess.run(
        [
            "ffmpeg", "-i", str(mp4_path),
            "-vn", "-codec:a", "libmp3lame", "-q:a", "4",
            "-y", str(mp3_path),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"Error: ffmpeg failed:\n{result.stderr}")
        sys.exit(1)

    size_mb = mp3_path.stat().st_size / (1024 * 1024)
    print(f"Extracted: {mp3_path.name} ({size_mb:.1f} MB)")
    return mp3_path


def transcribe(api_key, audio_path):
    """Send audio to Deepgram and return the response."""
    try:
        from deepgram import DeepgramClient
        from deepgram.core.api_error import ApiError
    except ImportError:
        print("Error: deepgram-sdk not installed.")
        print("Install with: pip install deepgram-sdk")
        sys.exit(1)

    file_size_mb = audio_path.stat().st_size / (1024 * 1024)
    print(f"\nSending {audio_path.name} ({file_size_mb:.1f} MB) to Deepgram Nova-3...")
    print("This may take 2-5 minutes for a 50-minute recording.")

    client = DeepgramClient(api_key=api_key)
    start_time = time.time()

    try:
        with open(audio_path, "rb") as f:
            response = client.listen.v1.media.transcribe_file(
                request=f.read(),
                model="nova-3",
                smart_format=True,
                diarize=True,
                utterances=True,
                paragraphs=True,
            )
    except ApiError as e:
        print(f"\nError: Deepgram API error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: transcription failed: {e}")
        sys.exit(1)

    elapsed = time.time() - start_time
    print(f"Transcription complete in {elapsed:.0f}s.")
    return response


def save_response(response, output_path):
    """Save Deepgram response as JSON."""
    output_path.write_text(response.model_dump_json(indent=2))
    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"\nSaved: {output_path} ({size_mb:.1f} MB)")


def print_summary(response):
    """Print a summary of the transcription results."""
    metadata = response.metadata
    results = response.results

    duration_secs = metadata.duration
    minutes = int(duration_secs // 60)
    seconds = int(duration_secs % 60)

    word_count = 0
    speaker_set = set()
    for channel in results.channels:
        for alt in channel.alternatives:
            if alt.words:
                for word in alt.words:
                    word_count += 1
                    if word.speaker is not None:
                        speaker_set.add(word.speaker)

    print(f"\n--- Summary ---")
    print(f"  Duration:  {minutes}m {seconds}s")
    print(f"  Words:     {word_count:,}")
    print(f"  Speakers:  {len(speaker_set)}")


def run_analyze(session_dir):
    """Auto-run the analyze script if it exists."""
    analyze_script = SCRIPT_DIR / "analyze-speakers.py"
    if not analyze_script.exists():
        print(f"\nNote: analyze script not found at {analyze_script}, skipping.")
        return

    print(f"\nRunning analyze script...")
    result = subprocess.run(
        ["/usr/bin/python3", str(analyze_script), str(session_dir)],
    )
    if result.returncode != 0:
        print("Warning: analyze script exited with errors.")


def main():
    if len(sys.argv) != 2:
        print("Usage: /usr/bin/python3 scripts/transcribe.py <session-dir>")
        print("Example: /usr/bin/python3 scripts/transcribe.py 2-13-26")
        sys.exit(1)

    session_dir = PROJECT_DIR / sys.argv[1]
    if not session_dir.is_dir():
        print(f"Error: session directory not found: {session_dir}")
        sys.exit(1)

    output_path = session_dir / "deepgram.json"

    # Check for existing output
    if output_path.exists():
        if sys.stdin.isatty():
            answer = input(f"{output_path.name} already exists. Overwrite? [y/N] ")
            if answer.lower() not in ("y", "yes"):
                print("Aborted.")
                sys.exit(0)
        else:
            print(f"{output_path.name} already exists, overwriting.")

    api_key = load_api_key()
    audio_path = find_audio(session_dir)
    response = transcribe(api_key, audio_path)
    save_response(response, output_path)
    print_summary(response)
    run_analyze(session_dir)

    print("\nDone.")


if __name__ == "__main__":
    main()
