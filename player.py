import vlc

class VideoPlayer:
    def __init__(self, widget_id, callback):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.player.set_hwnd(widget_id)

        events = self.player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerEndReached, callback)

    def play(self, path):
        media = self.instance.media_new(path)
        self.player.set_media(media)
        self.player.play()

    def set_volume(self, volume):
        # volume: 0-100
        self.player.audio_set_volume(volume)

    def stop(self):
        self.player.stop()