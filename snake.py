import curses 
from random import randint

# set the window

length = 20
width = 60


curses.initscr()
win = curses.newwin(length, width, 0, 0) # y,x
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1) # -1

# initialize snake 
snake = [(4, 10), (4, 9), (4, 8)]
# initialize food
food = (10, 20)

win.addch(food[0], food[1], '#')

# game logic
score = 0

ESC = 27
key = curses.KEY_RIGHT

while key != ESC:
    win.addstr(0, (width//2)-(width//12), 'Score: ' + str(score) + ' ')
    win.timeout(150 - (len(snake)) // 5 + len(snake)//10 % 120) # increase speed

    prev_key = key
    event = win.getch()
    key = event if event != -1 else prev_key

    if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ESC]:
        key = prev_key

	# to not allow 180 degree turn
    if key == curses.KEY_LEFT and prev_key == curses.KEY_RIGHT:
        key = prev_key
    if key == curses.KEY_RIGHT and prev_key == curses.KEY_LEFT:
        key = prev_key
    if key == curses.KEY_UP and prev_key == curses.KEY_DOWN:
        key = prev_key
    if key == curses.KEY_DOWN and prev_key == curses.KEY_UP:
        key = prev_key


    # calculate the next coordinates
    y = snake[0][0]
    x = snake[0][1]
    if key == curses.KEY_DOWN:
        y += 1
    if key == curses.KEY_UP:
        y -= 1
    if key == curses.KEY_LEFT:
        x -= 1
    if key == curses.KEY_RIGHT:
        x += 1

    snake.insert(0, (y, x)) 

    # check if we hit the border
    if y == 0: break
    if y == length-1: break
    if x == 0: break
    if x == width-1: break

    # if snake runs over itself
    if snake[0] in snake[1:]: break

    if snake[0] == food:
        # eat the food
        score += 1
        food = ()
        while food == ():
            food = (randint(1,length-2), randint(1,width-2))
            if food in snake:
                food = ()
        win.addch(food[0], food[1], '#')
    else:
        # move snake
        last = snake.pop()
        win.addch(last[0], last[1], ' ')

    win.addch(snake[0][0], snake[0][1], '*')

curses.endwin()
print(f"Final score = {score}")
