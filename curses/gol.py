import curses
from curses import wrapper
import random
from curses.textpad import Textbox, rectangle

def next_state(board):
    state = {}
    rows = len(board)
    if rows == 0:
        return
    cols = len(board[0])
    
    for i in range(rows):
        for j in range(cols):
            an = 0
            cs = board[i][j]
            if i-1 >=0 and j-1 >= 0 and board[i-1][j-1] == 1:
                an += 1
            if i-1 >= 0 and board[i-1][j] == 1:
                an += 1
            if i-1 >= 0 and j+1 < cols and board[i-1][j+1] == 1:
                an += 1
            if i+1 < rows and j-1 >= 0 and board[i+1][j-1] == 1:
                an += 1
            if i+1 < rows and board[i+1][j] == 1:
                an += 1
            if i+1 < rows and j+1 < cols and board[i+1][j+1] == 1:
                an += 1
            if j-1 >= 0 and board[i][j-1] == 1:
                an += 1
            if j+1 < cols and board[i][j+1] == 1:
                an += 1
            
            if an < 2 and cs == 1:
                state[(i, j)] = 0
            elif an > 3 and cs == 1:
                state[(i, j)] = 0
            elif an == 3 and cs == 0:
                state[(i, j)] = 1
                
    for k, v in state.items():
        board[k[0]][k[1]] = v

def get_screen():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLUE)

    return stdscr

def exit_screen(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def get_rows(stdscr):
    stdscr.addstr(3, 2, "Enter rows : (max : {})".format(curses.LINES-1))
    stdscr.addstr(4, 2, "Ctrl-G/Enter to submit")

    editwin = curses.newwin(1, 12, 7, 3) # rows, cols, y, x
    rectangle(stdscr, 6, 2, 8, 15) # win, uly, ulx, lry, lrx
    stdscr.refresh()

    box = Textbox(editwin)
    # Let the user edit until Ctrl-G is struck.
    box.edit()

    # Get resulting contents
    message = box.gather()

    try:
        rows = int(message)
        if rows > curses.LINES-1:
            return curses.LINES-1
        else:
            return rows
    except:
        return 10

def get_cols(stdscr):
    stdscr.addstr(3, 2, "Enter cols : (max : {})".format(curses.COLS-1))
    stdscr.addstr(4, 2, "Ctrl-G/Enter to submit")

    editwin = curses.newwin(1, 12, 7, 3) # rows, cols, y, x
    rectangle(stdscr, 6, 2, 8, 15) # win, uly, ulx, lry, lrx
    stdscr.refresh()

    box = Textbox(editwin)
    # Let the user edit until Ctrl-G is struck.
    box.edit()

    # Get resulting contents
    message = box.gather()

    try:
        cols = int(message)
        if cols > curses.COLS-1:
            return curses.COLS-1
        else:
            return cols
    except:
        return 10

def setup_game(stdscr, rows, cols):
    stdscr.clear()  
    stdscr.addstr(1, 2, "Random game of life", curses.A_REVERSE)
    stdscr.addstr(2, 2, "move cursor using arrow keys and press 's' to set life")
    stdscr.refresh()
    board = []
    for i in range(rows):
        board.append(cols*[0])

    y_offset = 4
    x_offset = 2

    cx = [y_offset, x_offset]

    key = ''
    while key != ord('q'):

        if key == ord('s'):
            board[cx[0]-y_offset][cx[1]-x_offset] = 1 - board[cx[0]-y_offset][cx[1]-x_offset]
        elif key == curses.KEY_UP:
            if cx[0] > y_offset:
                cx[0] -= 1
        elif key == curses.KEY_DOWN:
            if cx[0] < y_offset+rows-1:
                cx[0] += 1
        elif key == curses.KEY_LEFT:
            if cx[1] > x_offset:
                cx[1] -= 1
        elif key == curses.KEY_RIGHT:
            if cx[1] < x_offset+cols-1:
                cx[1] += 1

        for i in range(rows):
            for j in range(cols):
                if board[i][j]:
                    stdscr.addch(y_offset+i, x_offset+j, "X", curses.color_pair(1))
                else:
                    stdscr.addch(y_offset+i, x_offset+j, "-")
        stdscr.addch(cx[0], cx[1], "X", curses.color_pair(2))

        stdscr.refresh()
        key = stdscr.getch()

    return board  

def start_game(stdscr, rows, cols, board):
    
    stdscr.clear()  
    stdscr.refresh()
    x_offset = 0
    y_offset = 0

    key = ''
    while key != ord('q'):

        for i in range(rows):
            for j in range(cols):
                if board[i][j]:
                    stdscr.addch(x_offset+i, y_offset+j, "X", curses.color_pair(1))
                else:
                    stdscr.addch(x_offset+i, y_offset+j, "-")
        
        stdscr.refresh()
        key = stdscr.getch()
        next_state(board)

    exit_screen(stdscr)

def init_game():
    stdscr = get_screen()

    stdscr.clear()
    stdscr.addstr(1, 2, "Random game of life", curses.A_REVERSE)

    rows = get_rows(stdscr)
    cols = get_cols(stdscr)

    board = setup_game(stdscr, rows, cols)
    start_game(stdscr, rows, cols, board)

init_game()