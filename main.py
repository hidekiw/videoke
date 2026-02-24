import sys, os
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
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
        self.control_buttons = []
        self.numpad_buttons = []

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # VIDEO
        self.video_frame = QFrame()
        self.video_frame.setStyleSheet("background:black;")
        layout.addWidget(self.video_frame, 3)

        # SIDE
        side_widget = QWidget()
        side = QVBoxLayout(side_widget)
        side.setContentsMargins(5, 5, 5, 5)
        side.setSpacing(5)

        self.display = QLineEdit()
        self.display.setMinimumHeight(60)
        side.addWidget(self.display)

        self.queue_list = QListWidget()
        self.queue_list.itemDoubleClicked.connect(self.play_selected)
        side.addWidget(self.queue_list, 2)

        # CONTROLS
        ctrl = QGridLayout()
        ctrl.setSpacing(3)

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
            btn.setMinimumHeight(50)
            btn.setStyleSheet("background:#ff66cc; color:white; font-weight:bold; border-radius:5px;")
            btn.clicked.connect(func)
            self.control_buttons.append(btn)
            ctrl.addWidget(btn,r,c)
            c+=1
            if c>1:
                c=0;r+=1

        side.addLayout(ctrl, 1)

        # NUMPAD
        grid = QGridLayout()
        grid.setSpacing(3)
        nums = ['1','2','3','4','5','6','7','8','9','0','ADD']

        pos=0
        for r in range(4):
            for c in range(3):
                if pos>=len(nums): break
                b = QPushButton(nums[pos])
                b.setMinimumHeight(60)
                b.setStyleSheet("background:#33ccff; color:black; font-weight:bold; border-radius:5px;")
                b.clicked.connect(self.handle)
                self.numpad_buttons.append(b)
                grid.addWidget(b,r,c)
                pos+=1

        side.addLayout(grid, 1)
        layout.addWidget(side_widget, 1)

        self.player = VideoPlayer(int(self.video_frame.winId()), self.song_finished)
        self.update_fonts()

    def resizeEvent(self, event):
        """Atualiza os tamanhos das fontes quando a janela é redimensionada"""
        super().resizeEvent(event)
        self.update_fonts()

    def update_fonts(self):
        """Ajusta tamanhos de fonte baseado no tamanho da janela"""
        # Verifica se os widgets já foram criados
        if not hasattr(self, 'display') or not hasattr(self, 'control_buttons'):
            return
        
        width = self.width()
        font_size_display = max(16, width // 50)
        font_size_controls = max(14, width // 70)
        font_size_numpad = max(16, width // 60)

        # Display
        font = QFont()
        font.setPointSize(font_size_display)
        font.setBold(True)
        self.display.setFont(font)

        # Control buttons
        font = QFont()
        font.setPointSize(font_size_controls)
        font.setBold(True)
        for btn in self.control_buttons:
            btn.setFont(font)

        # Numpad buttons
        font = QFont()
        font.setPointSize(font_size_numpad)
        font.setBold(True)
        for btn in self.numpad_buttons:
            btn.setFont(font)

        # Queue list
        font = QFont()
        font.setPointSize(max(12, width // 80))
        self.queue_list.setFont(font)

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
            self.player.stop()  # Para a música anterior antes de tocar a nova
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