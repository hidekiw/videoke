import subprocess
import numpy as np
import sounddevice as sd
import pyrubberband as pyrb
import threading

class RealTimeAudio:

    def __init__(self):
        self.pitch = 1.0
        self.tempo = 1.0
        self.running = False

    def set_pitch(self, value):
        self.pitch = value

    def set_tempo(self, value):
        self.tempo = value

    def play(self, file):
        self.running = True

        cmd = [
            "ffmpeg",
            "-i", file,
            "-f", "f32le",
            "-acodec", "pcm_f32le",
            "-ac", "2",
            "-ar", "44100",
            "-"
        ]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

        def stream():
            while self.running:
                data = process.stdout.read(44100 * 2 * 4 // 10)
                if not data:
                    break

                audio = np.frombuffer(data, dtype=np.float32)
                audio = audio.reshape(-1, 2)

                # aplica pitch + tempo
                audio = pyrb.pitch_shift(audio, 44100, self.pitch)
                audio = pyrb.time_stretch(audio, 44100, self.tempo)

                sd.play(audio, 44100)
                sd.wait()

        threading.Thread(target=stream, daemon=True).start()

    def stop(self):
        self.running = False