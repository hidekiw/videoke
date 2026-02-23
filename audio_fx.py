import subprocess

def apply_pitch(input_file, output_file, pitch=1.0, tempo=1.0):
    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-af", f"rubberband=pitch={pitch}:tempo={tempo}",
        output_file
    ]
    subprocess.run(cmd)