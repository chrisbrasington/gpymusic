import vlc

class Player:
    """Responsible for playing streams or local MP3 files."""
    def __init__(self):
        self.player = None

    def play(self, media):
        """
        Start a stream.
        media should be a url or a file path.
        """
        self.player = vlc.MediaPlayer(media)
        self.player.play()

    def pause(self):
        """Pause playback."""
        if self.player:
            self.player.pause()

    def stop(self):
        """Stop playback."""
        if self.player:
            self.player.stop()
