# Rock-paper-scissors-lizard-Spock game

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

def name_to_number(name):
    # Converts name (Rock-paper-scissors-lizard-Spock) to number (0-4)
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        return "Invalid name"

def number_to_name(number):
	# Converts number to name
	
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        return "Invalid number"

def rpsls(player_choice): 
    # game logic
    print ""
    print "Player chooses " + player_choice
    player_number = name_to_number(player_choice)
    comp_number = random.randrange(0, 5)
    comp_choice = number_to_name(comp_number)
    print "Computer chooses " + comp_choice
    result_number = (comp_number - player_number) % 5
    if (result_number > 0) and (result_number < 3):
        result = "Computer wins!"
    elif (result_number > 2) and (result_number < 5):
        result = "Player wins!"
    elif (result_number == 0):
        result = "Player and computer tie!"
    else:
        result = "Error!!!!"
    print result
    print comp_number, player_number, result_number
    return result_number
	
	rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")