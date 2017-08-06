import curses

ENTER = 10  # Enter key.
UP = (259, 16)  # Up arrow or C-p.
DOWN = (258, 14)  # Down arrow or C-n.

HELP = """\
    Up/Down: - - - - - Move the cursor
    Enter: - - - - - - Select an item
    /search query: - - Search for query
    h: - - - - - - - - Show this help message\
"""

def loop(ui, api):
    search = api.search if api.is_subscribed() else local_search
    while True:
        refresh = False  # Only refresh the screen if necessary.
        ch = ui.keypress()

        if ch == curses.ERR:
            ui.error("Something went wrong.")

        elif ch == ENTER:
            item = ui.select()
            ui.bar_notification("Press p to play, q to queue or c to cancel.")
            if chr(ui.keypress()) == "p":
                pass
            elif chr(ui.keypress()) == "q":
                pass

        elif ch in UP:
            ui.move_cursor(-1)
            refresh = True

        elif ch in DOWN:
            ui.move_cursor(1)
            refresh = True

        elif chr(ch) == "h":
            ui.block_msg(HELP)
            refresh = True

        elif chr(ch) == "/":
            try:
                _, cmd, args = ui.get().split(" ", 2)  # First split is ">".
            except ValueError:
                continue

            cmd = cmd.lower().strip()
            args = args.lower().strip()

            if cmd == "search":
                if not args:
                    ui.error("Search requires a query")
                else:
                    ui.bar_notification("Searching for: %s" % args)
                    ui.update(search(args))
                    refresh = True

            elif cmd == "goto":
                try:
                    ui.move_cursor(int(args) - 1, absolute=True)
                except ValueError:
                    if args in ["songs", "artists", "albums"]:
                        ui.goto(args)
                    else:
                        ui.error("Argument must be a number or a section")
            else:
                ui.error("Command not recognized")

        ui.refresh()

def local_search(query):
    # TODO
    return {"songs": [], "artists": [], "albums": []}
