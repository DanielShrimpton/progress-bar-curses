import curses


class Window:
    def __init__(self, lines, cols, y_pos, x_pos):
        self.window = curses.newwin(lines, cols, y_pos, x_pos)

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
            self.pad.resize(self.size, max_cols)
        self.pad.addstr(message)
        if self.row >= max_rows - 1:
            self.pad.refresh(self.row - (max_rows - 1), 0, 0, 0, max_rows-2, max_cols - 1)
        else:
            self.pad.refresh(0, 0, 0, 0, max_rows-2, max_cols-1)


screen = curses.initscr()
max_rows, max_cols = screen.getmaxyx()
bar = Window(1, max_cols, max_rows - 1, 0)

rest = Pad(max_rows - 1, max_cols)
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
