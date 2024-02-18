import curses


screen = curses.initscr()
curses.curs_set(0)
screen.keypad(True)
curses.noecho()
curses.cbreak()


height, width = screen.getmaxyx()

WIN_TITLE = "[o] Goppai"

GOPPAI_START = [
    "Play games",
    "History",
    "Quit",
]

GOPPAI_GAMES = [
    "2048",
]


def __display_title_bar(title, screen, line=0):
    _, w = screen.getmaxyx()
    screen.addstr(line, 0, "-" * w)
    line += 1
    screen.addstr(line, 0, title)
    line += 1
    screen.addstr(line, 0, "-" * w)
    line += 1
    return line


def goppai_window():
    selection = 0

    while True:
        screen.clear()
        line = __display_title_bar(WIN_TITLE, screen)

        screen.addstr(line, 0, "Goppai Start!")

        line += 1

        for index, option in enumerate(GOPPAI_START):
            item = f"[-] {option}" if selection == index else f" -  {option}"

            screen.addstr(line, 0, item)

            line += 1

        screen.refresh()

        key = screen.getch()

        if key == curses.KEY_UP and selection > 0:
            selection -= 1
        # If the key is down, move the selection down
        elif key == curses.KEY_DOWN and selection < len(GOPPAI_START) - 1:
            selection += 1
        elif (key == curses.KEY_ENTER or key in [10, 13]) and selection == 2:
            break


curses.nocbreak()
curses.echo()
curses.curs_set(1)
screen.keypad(False)
curses.endwin()
