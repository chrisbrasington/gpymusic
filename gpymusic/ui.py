import curses
import curses.textpad

class BarWindow:
    """
    A window for user input and notifications.
    Should generally contain only one row.
    """
    def __init__(self, nlines, ncols, begin_y, begin_x=0):
        self.nlines = nlines
        self.ncols = ncols
        self.win = curses.newwin(nlines, ncols, begin_y, begin_x)
        self.input = curses.textpad.Textbox(self.win)
        self.song = None  # Currently playing song.

    def get(self):
        """Get some user input."""
        prompt = "> "
        addstr(self.win, prompt)
        self.win.move(0, len(prompt))
        curses.curs_set(2)
        text = self.input.edit()
        curses.curs_set(0)
        self.win.clear()
        return text

class ContentWindow:
    """Window for displaying content."""
    def __init__(self, nlines, ncols, begin_y=0, begin_x=0):
        self.nlines = nlines
        self.ncols = ncols
        self.win = curses.newwin(nlines, ncols, begin_y, begin_x)
        self.content = {}
        self.range = range(1, 1)  # The range of lines currently on screen.

class UI:
    """Container for the two windows and interface to most display ops."""
    def __init__(self, content, bar):
        self.nlines = content.nlines + bar.nlines
        self.ncols = content.ncols + bar.ncols
        self.content = content
        self.bar = bar
        self.cursor = 0

    def get(self):
        return self.bar.get()

    def banner(self, s):
        """Add a string to the center of the content window."""
        y = self.content.nlines // 2
        x = self.content.ncols // 2 - (len(s) // 2)
        addstr(self.content.win, s, y=y, x=x)

    def bar_notification(self, s):
        """Add a string to the bar."""
        addstr(self.bar.win, s)

    def error(self, s):
        """Display an error message on the bar."""
        addstr(self.bar.win, "Error: %s. Enter '/h' for help." % s)

    def now_playing(self):
        """Display the currently playing song."""
        if self.bar.song is None:
            addstr(self.bar.win, "Nothing playing")
        else:
            addstr(self.bar.win, "Playing: %s", song)

    def block_msg(self, s):
        """display a multi-line banner."""
        self.content.win.clear()
        lines = s.split("\n")
        y = self.content.nlines // 2 - len(lines) // 2
        for i, line in enumerate(lines):
            addstr(self.content.win, line, y=y + i, x=10, clear=False)

    def select(self):
        """Get the element underneath the cursor."""
        content = self.content.content
        flattened = []
        for k in ["songs", "artists", "albums"]:
            if k in content:
                flattened.append(None)
                flattened.extend(content[k])
        return flattened[self.cursor]

    def keypress(self):
        """Get a keypress."""
        return self.bar.win.getch()

    def move_cursor(self, n, absolute=False):
        """Move the cursor n places, or set it to n is absolute is True."""
        if absolute:
            self.cursor = n
        else:
            self.cursor += n
        # Make sure we're still in bounds.
        content = self.content.content
        length = sum(len(content[k]) for k in content)
        self.cursor = min(length - 1, self.cursor)
        self.cursor = max(0, self.cursor)

    def goto(self, section):
        """Move the cursor to a section."""
        content = self.content.content
        songs = 0
        artists = len(content["songs"]) + 1 if "songs" in content else songs + 1
        albums = artists + len(content["artists"]) + 1 if "artists" in content else artists + 1
        if section == "songs":
            self.move_cursor(songs, absolute=True)
        elif section == "artists":
            self.move_cursor(artists, absolute=True)
        elif section == "albums":
            self.move_cursor(albums, absolute=True)

    def update(self, content):
        """Replace the contents of the main window."""
        self.content.content = content

    def refresh(self):
        """Draw the content to screen and refresh the main window."""
        self.content.win.clear()
        content = self.content.content
        lines = []
        if "songs" in content and content["songs"]:
            lines.append(" ==== Songs (%d) ====" % len(content["songs"]))
            lines.extend(str(song) for song in content["songs"])
        if "artists" in content and content["artists"]:
            lines.append(" ==== Artists (%d) ====" % len(content["artists"]))
            lines.extend(str(artist) for artist in content["artists"])
        if "albums" in content and content["albums"]:
            lines.append(" ==== Albums (%d) ====" % len(content["albums"]))
            lines.extend(str(album) for album in content["albums"])

        if self.cursor not in self.content.range:
            length = min(sum(len(content[l]) for l in content), self.content.nlines)
            if self.cursor < self.content.range.start:
                self.content.range = range(self.cursor + 1, self.cursor + 1 + length)
            elif self.cursor >= self.content.range.stop:
                self.content.range = range(self.cursor + 2 - length, self.cursor + 2)

        for y, i in enumerate(self.content.range):
            s = "%d: %s" % (i, lines[i-1])
            if self.cursor == i - 1:
                addstr(self.content.win, s, y=y, clear=False, attr=curses.A_REVERSE)
            else:
                addstr(self.content.win, s, y=y, clear=False)

        self.content.win.refresh()

def addstr(win, s, y=0, x=0, clear=True, attr=None):
    """Add a string to a single line in a given window."""
    # if len(s) >= win.getmaxyx()[1] - 1:
    #     s = s[:-9] + " ..."  # No idea why 9 is the magic number.
    if clear:
        win.clear()
    if attr is None:
        win.insstr(y, x, s)
    else:
        win.insstr(y, x, s, attr)
    win.refresh()
