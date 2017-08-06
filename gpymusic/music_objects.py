import datetime
import pickle
import vlc

class MusicObject:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def dump(self, f):
        pickle.dump(self, f)

    def dumps(self):
        return pickle.dumps(self)

class Song(MusicObject):
    """A song from Google Play Music."""
    def __init__(self, data):
        """
        data can come from three sources:
          - Search results:
            - Artist name is in data["artist"].
          - Song lookup
            - Artist name is in data["artist"].
          - Artist constructor
            - Artist name is in data["albumArtist"].
          - Album constructor
            - Artist name is in data["albumArtist"].
        data["artistId"] is always a list.
        A Song is always playable.
        """
        super().__init__(data["storeId"], data["title"])
        self.artist = Artist({
            "name": data["artist"] if "artist" in data else data["albumArtist"],
            "artistId": data["artistId"][0],
        })
        self.album = Album({
            "name": data["album"],
            "albumId": data["albumId"],
            "artist": data["artist"],
            "artistId": data["artistId"],
        })
        seconds = int(data["durationMillis"]) // 1000
        self.length = datetime.timedelta(seconds=seconds)
        self.playable = True

    def __str__(self):
        return "%s - %s - %s (%s)" % (self.name, self.artist.name, self.album.name, self.length)

class Artist(MusicObject):
    """An artist from Google Play Music."""
    def __init__(self, data):
        """
        data can come from four sources:
          - Song constructor:
            - data["topTracks"] does not exist.
            - data["albums"] does not exist.
          - Album constructor:
            - data["topTracks"] does not exist.
            - data["albums"] does not exist.
          - Search results:
            - data["topTracks"] does not exist.
            - data["albums"] does not exist.
          - Artist lookup:
            - data["topTracks"] is fully populated.
            - data["albums"] is fully populated.
        data["artistId"] is always a string.
        An Artist is playable if it contains any songs or albums.
        """
        super().__init__(data["artistId"], data["name"])
        self.songs = [Song(s) for s in data["topTracks"]] if "topTracks" in data else []
        self.albums = [Album(a) for a in data["albums"]] if "albums" in data else []
        self.playable = bool(self.songs) or bool(self.albums)

    def __str__(self):
        return self.name

class Album(MusicObject):
    """An album from Google Play Music."""
    def __init__(self, data):
        """
        data can come from four sources:
          - Song constructor:
            - data["tracks"] does not exist.
          - Artist constructor:
            - data["tracks"] does not exist.
          - Search results:
            - data["tracks"] does not exist.
          - Album lookup:
            - data["tracks"] is fully populated.
        data["artistId"] is always a list.
        An Album is playable if it contains any songs.
        """
        super().__init__(data["albumId"], data["name"])
        self.artist = Artist({
            "artistId": data["artistId"][0],
            "name": data["artist"],
        })
        self.songs = [Song(s) for s in data["tracks"]] if "tracks" in data else []
        self.length = sum([s.length for s in self.songs], datetime.timedelta())
        self.playable = bool(self.songs)

    def __str__(self):
        return "%s - %s" % (self.artist.name, self.name)

# TODO

class Playlist(MusicObject):
    pass

class RadioStation(MusicObject):
    pass

def load(f):
    return pickle.load(f)

def loads(s):
    return pickle.loads(s)
