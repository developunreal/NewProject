import subprocess

def transcribe_audio(file_path):
    result = subprocess.run(
        ["whisper", file_path, "--model", "base", "--language", "en", "--output_format", "txt"],
        capture_output=True
    )
    transcript_file = file_path.replace(".wav", ".txt")
    with open(transcript_file, "r") as f:
        return f.read().strip()

