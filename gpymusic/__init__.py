import curses

from . import api_wrapper
from . import gpm
from . import ui

def main(stdscr, config):
    """Set up the UI and log into Google Play Music."""
    curses.curs_set(0)
    maxy, maxx = stdscr.getmaxyx()
    content = ui.ContentWindow(maxy - 1, maxx)
    bar = ui.BarWindow(1, maxx, maxy - 1)
    screen = ui.UI(content, bar)
    screen.banner("Welcome to Google Py Music! Logging in...")
    api = api_wrapper.API(config["email"], config["password"], config["deviceid"])
    screen.banner("Logged in.")
    screen.bar_notification("Enter '/h' for help.")
    gpm.loop(screen, api)
