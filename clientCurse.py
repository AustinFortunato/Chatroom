import curses

screen = curses.initscr()

my_window = curses.newwin(30, 30, 0, 0)
my_window.clear()

def menuSelector(options, window, current):
	window.keypad(True)
	rows, cols = window.getmaxyx()

	for enum, i in enumerate(options):
		row = int(rows/2)-int(len(options)/2)+enum
		col = int(cols/2)-int(len(i)/2)
		if i == current:
			window.addstr(row, col, i, curses.A_STANDOUT)
		else:
			window.addstr(row, col, i)

	while True:
		c = window.getch()
		if c == curses.KEY_UP:
			return menuSelector(options, window, options[(options.index(current))-1])
			break
		elif c == curses.KEY_DOWN:
			return menuSelector(options, window, options[((options.index(current))+1)%len(options)])
			break
		elif c == curses.KEY_ENTER or c == 10 or c == 13:
			return current
			break

	window.clear()
	window.refresh()

curses.endwin()
