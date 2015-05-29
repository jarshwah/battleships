import random
import os
from sys import exit

#0.5 - changed the way place_ship appends shit to the board list.
#    - built test_ship_gen for testing the for/while loop for building ships
#    - added counter to while loop (20) to keep track of runaway loops until we have better checks on input.

#0.6 - changed check guess legal to work with dict structure
#    - added hits key in ships dict
#    - added store hit and store miss

#0.7 - added guess function, works well so far.
#    - Changed check_guess_hit, as it was pointlessly making things complicated.
#    - Added turns to the board dict so I can track the number of turns the user has had. Missing increments this.

#0.8 - pulled together the guess function into a while loop with exit conditions
#    - Lost track.
#    - Changed guess function so no more errors if guess out of scope.
#    - added OS clear, so no more buildup of boards
#    - changed get_guess so it would catch value errors and ask again for input.
#    - changed a few raw_input calls so it would figure out how long the board is.
#    - added get_int_input function for returning an int value when you pass it a string.
#    - changed test_ship _gen to use the above
#    - changed get_ship_info to do the same
#    - fixed a bug where you could break rand function by entering a ship larger than board.
#    - removed redundant board placement function
#    - changed gen_board and board_dict to just take the param dict.


#Board gen and Ship Placement functions below

def gen_board(param):
    """This function generates the board, accepts the width of the board as an int"""
    board = []
    for i in range(param['boardsize']):		#loop to build board of Os
        board.append(['O'] * param['boardsize'])
    return board

def board_dict(param):
    """This function is to build out the dict for 
    storing boards and ship coords for collision detection"""
    board = {}
    board['field'] = gen_board(param) #for placing ship notation
    board['ships'] = [] #for storing ship tuples for collision detection
    board['turns'] = 0
    return board

def print_board(board):		#function for printing the board out pretty
    """Prints the board pretty with -- as border"""
    print "--" * len(board['field'])
    for i in board['field']:
        print " ".join(i)		#join uses list objects without quotes
    print "--" * len(board['field'])

def get_ship_info(board):
    """Queries the user for information regarding the name of the ship and the length. 
    Also builds the ship dict to be used in later functions"""
    ship = {'length': None, 'name' : None,'coords' : None}
    while True:
        ship['length'] = get_int_input("How long do you want ship to be?: ")
        if ship['length'] <= len(board['field']):
            break
        else:
            print "Ship is longer than the board, try again."
    ship['name'] = raw_input("What's the name of this ship?: ")
    return ship

def get_rand_vector():
    """Randomly assigns a vector for the ship."""
    return random.choice(["vertical","horizontal"])

def get_rand_startpos(board, ship_vector, ship_length):
    """This function is used for generating a random ship start position. It takes 
    board, ship vector and ship length to determine which coords are valid for 
    generation. Returns the ship pos as a set of coordinates in a tuple."""
    if ship_vector == 'vertical':
        ship_pos = [(random.randrange(0, len(board) - ship_length + 1),random.randint(0, len(board) - 1))]
    else:
        ship_pos = [(random.randint(0, len(board) - 1),random.randrange(0, len(board) - ship_length + 1))]
    return ship_pos

def place_ship_coords(board, ship):
    """This function builds out the coordinates for the boat based on the variables it 
    takes, board and ship. ship should contain a dict with at least vector, length 
    and coords. Returns ship with updated coords values."""
    
    # the math here is kind of confusing, anyway to simplify it? perhaps by breaking it down
    # into smaller parts with named variables?
    if ship['vector'] == 'vertical':
        for i in range(ship['length']-1):
            ship['coords'].append((ship['coords'][-1][0]+1,ship['coords'][-1][1]))
    else:
        for i in range(ship['length']-1):
            ship['coords'].append((ship['coords'][-1][0],ship['coords'][-1][1]+1))
    return ship

def check_ship_loc(board, ship):
    """This function is used to check the ship's location against existing ships."""
    for i in ship['coords']:
        if i in board['ships']:
            return False
    return True

def gen_ship(board, ship_info):
    """takes in board and ship_info, returns board and ship_info. Builds out the ship
    variable by getting random vector and startpos, then building out the tuple coords
    then assigns it to the coords key in board for comparison later."""
    #get a random vector, store in vector of dict.
    ship_info['vector'] = get_rand_vector()
    #Send board size, ship vector and ship length to get legal start coords
    ship_info['coords'] = get_rand_startpos(board['field'], ship_info['vector'], ship_info['length'])
    #Send coords and length, get more coords
    ship_info = place_ship_coords(board['field'], ship_info)
    return (ship_info)

def place_ship(board, ship):
    """places the ship after we've confirmed the coords don't overlap"""
    for i in ship['coords']:
        board['ships'].append(i)
    return board


#Get Functions

def get_game_params():
    param = {}
    param['boardsize'] = get_int_input('How large do you want the board? ')
    param['ships'] = get_int_input('How many ships? ')
    return param

def get_int_input(string):  # good work on making this into a function
    while True:
        try:
            intput = int(raw_input(string))
            return intput 
        except ValueError:
            print "Please enter a positive integer."

def get_guess(board):
    """Retrieve the guess from the user"""
    guess_row = guess_col = None
    while True:
        try:
            guess_col = int(raw_input("Guess your col (0 - %s): " % (len(board['field']) - 1)))
            break
        except ValueError:
            print "Please enter a number from 0 to %s: " % (len(board['field']) - 1)
    while True:
        try:
            guess_row = int(raw_input("Guess your row (0 - %s): " % (len(board['field']) - 1)))
            break
        except ValueError:
            print "Please enter a number from 0 to %s: " % (len(board['field']) - 1)
    # this is sort of dangerous, because guess_col/row are assigned in "inner blocks" above,
    # so *may* not exist at this point. your logic above ensures they do, but it's still nicer
    # to define "defaults" in the same indentation (or higher..) than where you use them
    guess = (guess_row,guess_col)
    return guess



#Check Functions Here

def check_guess_legal(board, guess):
    """Function to check if guess is legal, returns True or false."""
    guess = [guess] # why are you creating a single element list here?
    return guess[0][0] in range(0,len(board['field'])) and guess[0][1] in range(0,len(board['field'])):
        
def check_guess_hit(board, guess):
    return guess in board['ships']:
        
def check_cell_guessed(board, guess):
    guess_row, guess_col = guess
    return board['field'][guess_row][guess_col] == '/' or board['field'][guess_row][guess_col] == 'X':

def check_game_over(board, ships):
    if ships['hits'] == len(board['ships']):
        print_board(board)
        print "Congrats. You sunk My Battleship in %s turns" % board['turns']
        exit()
    else:
        return False


        
#Store Functions:

def store_miss(board, guess):
    guess_row, guess_col = guess
    board['field'][guess_row][guess_col] = '/'
    return board

def store_hit(board, ships, guess):    ##TEST THIS BEFORE USING - TEST HITS INCREMENTS PROPERLY
    guess_row, guess_col = guess
    board['field'][guess_row][guess_col] = 'X'
    ships['hits'] += 1
    return (board, ships)



#Parent Functions Below, pulls together most of the above

def guess(board, ships):
    while True:
        guess = get_guess(board)
        os.system('clear')  # clever
        if check_guess_legal(board, guess):  # no need to compare against explicit True/False
            if not check_cell_guessed(board, guess):
                if check_guess_hit(board, guess):
                    print "Hit!"
                    board, ships = store_hit(board, ships, guess)
                    break
                else:  # it either Hit or Miss right?
                    print "Miss!"
                    board = store_miss(board, guess)
                    board['turns'] += 1
                    break
            else:
                print "You already guessed that!"
                print_board(board)
        else:
            print "Sorry, guess out of scope of board, try again."
            print_board(board)
    return (board, ships)

def test_ship_gen():  #  ultimately part of battleships()
    # you should rename this function to something like "generate_board()"
    param = get_game_params()
    board = board_dict(param)
    
    ships = {'hits' : 0}
    counter = 0
    for i in range(1, param['ships'] + 1):
        ship_info = get_ship_info(board)
        while True:
            counter += 1
            ships['ship' + str(i)] = gen_ship(board, ship_info)
            if check_ship_loc(board, ships['ship' + str(i)]) == True:
                board = place_ship(board, ships['ship' + str(i)])
                break
            elif counter == 20:
                exit("Counter on placement loop reached 20, maybe something is borken.")
    
    return (board, ships, param)
        
def battleships():
    # main functions are usually at the top of the file, even though
    # the __name__ == '__main__' check is at the bottom
    board, ships, param = test_ship_gen()
    
    while True:
        print "You have had %s turns!" % (board['turns'])
        print_board(board)
        guess(board, ships)
        if check_game_over(board, ships):  # No need to compare to True explicitly if it returns a bool 
            exit("Debug Exit")

if __name__ == '__main__':
    battleships()
