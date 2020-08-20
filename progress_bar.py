import curses


class ProgressBar:
    def __init__(self, n, max_count=100, padding=0):
        """
        The init function for the ProgressBar setting up the window and size.
        :param n: The n-th progress bar, if you want multiple progress bars, this will rise it up n
        lines.
        :param max_count: The number of items for the progress bar to fill up to.
        :param padding: If padding is wanted around the progress bar for some reason, will pad
        the progress bar with `padding` columns either side of the progress bar.
        """
        self.max_count = max_count
        self.count = 0
        self.padding = padding
        y_pos = MAX_ROWS - n
        x_pos = 0 + self.padding
        self.cols = MAX_COLS - 1 - 2 * self.padding
        self.mc_len = len(str(self.max_count))
        self.p_cols = self.cols - 5 - 2 * self.mc_len
        self.perc = int(self.p_cols / self.max_count)
        self.incre = 0
        self.window = curses.newwin(1, self.cols, y_pos, x_pos)
        self.move(True)

    def move(self, first=False):
        if not first:
            self.count += 1
        self.incre = int(self.p_cols / self.max_count * self.count)

        if self.count == self.max_count:
            line = "[%s%s%s] %d/%d" \
                   % ('=' * (int(self.incre / 2) - 4),
                      'COMPLETE',
                      '=' * (int(self.incre / 2) - 4),
                      self.count,
                      self.max_count)

        else:
            line = "[%s>%s] {number:0{width}d}/%d".format(width=self.mc_len, number=self.count) \
                   % ('=' * self.incre,
                      ' ' * (self.p_cols - self.incre - 1),
                      self.max_count)
        line += ' ' * (self.cols - len(line) - 1)

        self.print(line)

    def print(self, message):
        self.window.addstr(0, 0, message)
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

rest = Pad(MAX_ROWS - 1, MAX_COLS)
num = 100
bar = ProgressBar(1, max_count=num)

for i in range(num):
    rest.print("This is line %d\n" % i)
    bar.move()
    curses.napms(100)


rest.print("Press q to quit...")
while 1:
    c = rest.pad.getch()
    if chr(c) == 'q':
        curses.endwin()
        break
