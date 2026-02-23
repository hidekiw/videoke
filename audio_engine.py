import subprocess, os, uuid

TEMP_DIR = "temp"

def process_audio(input_file, pitch=1.0, tempo=1.0):
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    output = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.mp4")

    cmd = [
        "ffmpeg","-y",
        "-i", input_file,
        "-filter_complex",
        f"[0:a]rubberband=pitch={pitch}:tempo={tempo}[a]",
        "-map","0:v","-map","[a]",
        "-c:v","copy",
        output
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output