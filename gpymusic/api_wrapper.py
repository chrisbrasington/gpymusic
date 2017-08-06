import gmusicapi

from . import music_objects as mo

class NotSubscribed(Exception):
    pass

class API:
    """Wrapper around some gmusicapi functionality."""
    def __init__(self, email, password, device_id):
        """Log in to Google Play Music."""
        self.mc = gmusicapi.Mobileclient()
        self.mm = gmusicapi.Musicmanager()
        if not self.mc.login(email, password, device_id):
            pass  # TODO: Deal with credentials.
        if not self.mm.login():
            pass  # TODO: Deal with OAuth.

    def is_subscribed(self):
        return self.mc.is_subscribed

    def logout(self):
        """Logout of Google Play Music."""
        self.mc.logout()
        self.mm.logout()

    def search(self, query):
        """Search Google Play for a query."""
        if not self.mc.is_subscribed:
            raise NotSubscribed()

        results = self.mc.search(query, max_results=100)
        return {
            "songs": [mo.Song(s["track"]) for s in results["song_hits"]],
            "artists": [mo.Artist(a["artist"]) for a in results["artist_hits"]],
            "albums": [mo.Album(a["album"]) for a in results["album_hits"]],
        }

    def lookup_song(self, id):
        return mo.Song(self.mc.get_track_info(id))

    def lookup_artist(self, id):
        return mo.Artist(self.mc.get_artist_info(id, max_top_tracks=100))

    def lookup_album(self, id):
        return mo.Album(self.mc.get_album_info(id))

    def get_stream(self, id):
        return self.mc.get_stream_url(id)
