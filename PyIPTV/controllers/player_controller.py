import sys
import vlc

class PlayerController:
    def __init__(self, video_widget, status_callback=None):
        self.status_callback = status_callback or (lambda text: None)
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self._set_video_output(video_widget)
        self.events = self.player.event_manager()
        self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self._on_end)
        self.events.event_attach(vlc.EventType.MediaPlayerEncounteredError, self._on_error)

    def _set_video_output(self, widget):
        win_id = widget.winId()
        if sys.platform.startswith('win'):
            self.player.set_hwnd(int(win_id))
        elif sys.platform.startswith('linux'):
            self.player.set_xwindow(int(win_id))
        elif sys.platform.startswith('darwin'):
            self.player.set_nsobject(int(win_id))
        else:
            self.status_callback('OS non supporté pour vidéo')

    def play(self, url):
        if not url.strip():
            self.status_callback("URL invalide")
            return
        media = self.instance.media_new(url.strip())
        self.player.set_media(media)
        result = self.player.play()
        if result == -1:
            self.status_callback("Erreur de lecture")
        else:
            self.status_callback(f"Lecture : {url}")

    def pause(self):
        self.player.pause()
        self.status_callback("Statut : Pause")

    def stop(self):
        self.player.stop()
        self.status_callback("Statut : Arrêté")

    def is_playing(self):
        return self.player.is_playing()

    def set_volume(self, level):
        level = max(0, min(100, level))
        self.player.audio_set_volume(level)
        self.status_callback(f"Volume : {level}%")

    def mute(self):
        self.player.audio_toggle_mute()
        self.status_callback("Son coupé (toggle mute)")

    def seek(self, position):
        if self.player.is_seekable():
            length = self.player.get_length()
            if length > 0:
                self.player.set_time(int(length * position))
                self.status_callback(f"Position : {int(position * 100)}%")
        else:
            self.status_callback("Média non seekable")

    def seek_relative(self, seconds):
        """Seek relatif en secondes."""
        cur = self.player.get_time()
        if cur is not None and self.player.is_seekable():
            length = self.player.get_length()
            new_time = max(0, min(cur + seconds * 1000, length))
            self.player.set_time(int(new_time))

    def _on_end(self, event):
        self.status_callback("Lecture terminée")

    def _on_error(self, event):
        self.status_callback("Erreur de lecture VLC")