# template for "Stopwatch: The Game"
import simplegui

# define global variables
time = 0
scoreWin = 0
scoreTotal = 0
T_X = 100
T_Y = 110

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    decSec = t % 10
    minutes = t // 600
    dSec = (t % 600) // 100
    sec = ((t % 600) % 100) // 10
    return str(minutes) + ":" + str(dSec) + str(sec) + "." + str(decSec)    
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
    
def stop():
    global scoreWin, scoreTotal
    if timer.is_running():
        timer.stop()
        scoreTotal += 1
        if time % 10 == 0:
            scoreWin += 1
    
def reset():
    global time, scoreWin, scoreTotal
    timer.stop()
    time = 0
    scoreWin = 0
    scoreTotal = 0


# define event handler for timer with 0.1 sec interval
def tick():
    global time
    time += 1
    format(time)

# define draw handler
def draw_handler(canvas):
    
    global scoreWin, scoreTotal, T_X, T_Y
    canvas.draw_text(format(time), 
                     [T_X,T_Y], 
                     40, 
                     "White")
    canvas.draw_text(str(scoreWin)+"/"+str(scoreTotal), 
                     [250,30], 
                     20, 
                     "Green")

# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 300, 200)

# register event handlers
timer = simplegui.create_timer(100, tick)
frame.add_button("Start", start)
frame.add_button("Stop", stop)
frame.add_button("Reset", reset)
frame.set_draw_handler(draw_handler)

# start frame
# timer.start()
frame.start()

# Please remember to review the grading rubric
