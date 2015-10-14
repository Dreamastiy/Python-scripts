# "Guess the number" game
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random
rang = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    global rang
    secret_number = random.randrange(0, rang)
    print "New game. Range is [0, " + str(rang) + ")"
    global number_of_tries
    if rang == 100:
        number_of_tries = 7
        print "Number of remaining guesses is " + str(number_of_tries)
    elif rang == 1000:
        number_of_tries = 10
        print "Number of remaining guesses is " + str(number_of_tries)
    else:
        print "Error!"
    print ""
    #print secret_number

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global rang
    rang = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global rang
    rang = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global number_of_tries
    number_of_tries -= 1
    guess_int = int(guess)
    print "Guess was " + guess
    print "Number of remaining guesses is " + str(number_of_tries)
    if guess_int > secret_number:
        print "Lower!"
    elif guess_int < secret_number:
        print "Higher!"
    elif guess_int == secret_number:
        print "Correct!"
        print ""
        new_game()
    else:
        print "Error"
    if number_of_tries == 0:
        print "You ran out of guesses.  The number was " + str(secret_number)
        print ""
        new_game()        
    print ""
    return guess_int

# create frame
frame = simplegui.create_frame('Guess the number', 200, 200)

# register event handlers for control elements and start frame
frame.add_button('Range is [0,100)', range100, 100)
frame.add_button('Range is [0,1000)', range1000, 100)
frame.add_input('Enter number', input_guess, 100)

# call new_game 
new_game()