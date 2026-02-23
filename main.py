import sys, os
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from player import VideoPlayer
from queue_manager import QueueManager
from audio_engine import process_audio

class KaraokeUI(QWidget):

    def __init__(self):
        super().__init__()
        self.showFullScreen()

        self.pitch = 1.0
        self.tempo = 1.0
        self.volume = 100  # Volume inicial (0-100)

        self.queue = QueueManager()

        layout = QHBoxLayout(self)

        # VIDEO
        self.video_frame = QFrame()
        self.video_frame.setStyleSheet("background:black;")
        layout.addWidget(self.video_frame, 3)

        # SIDE
        side = QVBoxLayout()

        self.display = QLineEdit()
        self.display.setStyleSheet("font-size:40px;")
        side.addWidget(self.display)

        self.queue_list = QListWidget()
        self.queue_list.itemDoubleClicked.connect(self.play_selected)
        side.addWidget(self.queue_list)

        # CONTROLS
        ctrl = QGridLayout()

        buttons = [
            ("TOM +", self.pitch_up),
            ("TOM -", self.pitch_down),
            ("VEL +", self.tempo_up),
            ("VEL -", self.tempo_down),
            ("VOZ FEM", self.female),
            ("VOZ MASC", self.male),
            ("VOL +", self.volume_up),
            ("VOL -", self.volume_down),
        ]

        r=0;c=0
        for text,func in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet("font-size:20px;height:60px;background:#ff66cc;")
            btn.clicked.connect(func)
            ctrl.addWidget(btn,r,c)
            c+=1
            if c>1:
                c=0;r+=1

        side.addLayout(ctrl)

        # NUMPAD
        grid = QGridLayout()
        nums = ['1','2','3','4','5','6','7','8','9','0','ADD']

        pos=0
        for r in range(4):
            for c in range(3):
                if pos>=len(nums): break
                b = QPushButton(nums[pos])
                b.setStyleSheet("font-size:30px;height:80px;background:#33ccff;")
                b.clicked.connect(self.handle)
                grid.addWidget(b,r,c)
                pos+=1

        side.addLayout(grid)
        layout.addLayout(side,1)

        self.player = VideoPlayer(int(self.video_frame.winId()), self.song_finished)

    # -------- VOLUME CONTROLS --------
    def volume_up(self):
        self.volume = min(100, self.volume + 10)
        self.player.set_volume(self.volume)

    def volume_down(self):
        self.volume = max(0, self.volume - 10)
        self.player.set_volume(self.volume)

    # -------- AUDIO CONTROLS --------

    def pitch_up(self): self.pitch+=0.1
    def pitch_down(self): self.pitch-=0.1
    def tempo_up(self): self.tempo+=0.1
    def tempo_down(self): self.tempo-=0.1
    def female(self): self.pitch=1.3
    def male(self): self.pitch=0.8

    # -------- QUEUE --------

    def handle(self):
        t = self.sender().text()
        if t == "ADD":
            num = self.display.text()
            self.queue.add(num)
            self.queue_list.addItem(num)
            self.display.clear()
            # Se não houver música tocando, tocar a primeira
            if not self.player.player.is_playing():
                self.play_next()
        else:
            self.display.setText(self.display.text() + t)

    def play_selected(self, item):
        # Toca a música selecionada na lista ao dar duplo clique
        song = item.text()
        filename = f"{int(song):05d}.mp4" if song.isdigit() else song
        path = os.path.join("songs", filename)
        if os.path.exists(path):
            processed = process_audio(path, self.pitch, self.tempo)
            self.player.play(processed)

    def play_next(self):
        song = self.queue.next()
        if song:
            path = os.path.join("songs", song)
            if os.path.exists(path):
                self.player.play(path)

        processed=process_audio(path,self.pitch,self.tempo)
        self.player.play(processed)

    def song_finished(self,event):
        self.play_next()

app=QApplication(sys.argv)
w=KaraokeUI()
w.show()
sys.exit(app.exec())