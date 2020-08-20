import curses


class ProgressBar:
    def __init__(self, n, padding=0):
        """
        The init function for the ProgressBar setting up the window and size.
        :param n: The n-th progress bar, if you want multiple progress bars, this will rise it up n
        lines.
        :param padding: If padding is wanted around the progress bar for some reason, will pad
        the progress bar with `padding` columns either side of the progress bar.
        """
        y_pos = MAX_ROWS - n
        x_pos = 0 + padding
        cols = MAX_COLS - 2 * padding
        self.window = curses.newwin(1, cols, y_pos, x_pos)

    def print(self, message):
        self.window.addstr(message)
        self.window.refresh()


class Pad:
    def __init__(self, lines, cols):
        self.size = lines
        self.pad = curses.newpad(lines, cols)
        self.row = 0

    def print(self, message):
        self.row += 1
        if self.row >= self.size:
            self.size += 10
            self.pad.resize(self.size, MAX_COLS)
        self.pad.addstr(message)
        if self.row >= MAX_ROWS - 1:
            self.pad.refresh(self.row - (MAX_ROWS - 1), 0, 0, 0, MAX_ROWS - 2, MAX_COLS - 1)
        else:
            self.pad.refresh(0, 0, 0, 0, MAX_ROWS - 2, MAX_COLS - 1)


screen = curses.initscr()
MAX_ROWS, MAX_COLS = screen.getmaxyx()
bar = ProgressBar(1)

rest = Pad(MAX_ROWS - 1, MAX_COLS)
bar.print("[===>         ]")

for i in range(25):
    rest.print("This is line %d\n" % i)
    curses.napms(400)


rest.print("Press q to quit...")
while 1:
    c = rest.pad.getch()
    if chr(c) == 'q':
        curses.endwin()
        break
