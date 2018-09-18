"""
Another attempt at Hangman

14 JUL 2018
BoxTurtle488

(ADDED COMMENT: This was my attempt at Pseudo-Coding it first.)
IMPORT RANDOM LIBRARY
DEFINE FUNCTIONS
MORE?

MAIN():
    PLAY
        SINGLE PLAYER
            PLAY
                SP GAME():
                    GIVE OPTION TO CONTINUE PLAYING OR GO BACK TO MAIN MENU
                    RESET/DEFINE VARIABLES
                    LIST OF WORDS
                    RANDOMLY SELECT A WORD
                    PLAYER SELECTS PENALTY LIMIT
                    DEF DISPLAY():
                        ->WORD: *********
                        ->CATEGORY: "XXXXXX"
                        ->PENALTIES: X/Y
                    TURN LOOP:
                        IF VICTORY OR GAME OVER:
                            DISPLAY VICTORY/GAME OVER SCREEN
                            BREAK
                        PLAYER SELECTS A LETTER
                        IF RIGHT:
                            UPDATE SCORE -> VICTORY IF COMPLETE
                            DISPLAY()
                        IF WRONG:
                            UPDATE SCORE -> GAME OVER IF PENALTY LIMIT REACHED
                            DISPLAY()
            BACK
        TWO PLAYER
            PLAY
                2P GAME():
                    GIVE OPTION TO CONTINUE OR GO BACK TO MAIN MENU
                    RESET/DEFINE VARIABLES
                    RECURSIVE WORD SELECTION FUNCTION (IF POSSIBLE?)
                        PLAYER INPUTS WORD (a function that returns true or false)
                        IF WORD INVALID:
                            RE-ENTER WORD (call the function again)
                        ELSE WORD IS DEFINED AS A VARIABLE
                    PLAYER INPUTS PENALTY LIMIT
                    DEF DISPLAY():
                        ->WORD: ************
                        ->PENALTIES: X/Y
                    TURN LOOP:
                        IF VICTORY OR GAME OVER:
                            DISPLAY VICTORY/GAME OVER SCREEN
                            BREAK
                        PLAYER SELECTS A LETTER
                        IF RIGHT:
                            UPDATE SCORE -> VICTORY IF COMPLETE
                            DISPLAY()
                        IF WRONG:
                            UPDATE SCORE -> GAME OVER IF PENALTY LIMIT REACHED
                            DISPLAY()
            BACK
    QUIT

STATUS 14 JUL 2018:
    SP() COMPLETE:
        CAN EXPAND BY ADDING NEW WORDS TO THE CATEGORIES OR EVEN ADDING NEW CATEGORIES
        CAN FINE-TUNE THE BALANCE BY CHANGING DEFAULT PENALTIES
        PRETTY SWEET. I SHOULD EXPAND THIS, IF ONLY SO I CAN HAVE FUN WITH IT
        I COULD EVEN ADD SOME KIND OF GAMEIFIED MODE THAT WOULD BE A LITTLE MORE FUN
    2P() COMPLETE WITH BUGS
        BUG 1: AN EMPTY SPACE COUNTS AS A LETTER AND WILL PENALIZE THE PLAYER
    MAIN() COMPLETE w/ BUGS
        BUG 1: PRESSING Q TO EXIT OFTEN TAKES MULTIPLE ATTEMPTS


"""


import random

def mpGame():
    #Okay, maybe I should make this one more readable than the single player one
    word = None #Variables at the top!
    penalty_limit = 5
    current_penalties = 0
    already_guessed_mp = []
    display_word_mp = []
    vic_points_mp = 0
    vic_limit_mp = 0
    mp_menu_input = str(input("Two-player mode! Continue?\nY to continue or Q to go back\n"))
    if mp_menu_input.upper() == "Q": 
        main()
    elif mp_menu_input.upper() == "Y":
        def word_sel(): #function to have one player select a word for the other player to guess
            sel_word = str(input("One player type in a word for the other to guess: "))
            sel_word = sel_word.upper()
            word_good_q = str(input("Your chosen word is: " + str(sel_word) + "\nIs that acceptable? Y to accept, N to retry"))
            if word_good_q.upper() == "Y":
                return str(sel_word)
            elif word_good_q.upper() == "N":
                word_sel()
            else:
                print("Invalid input! Try again?\n")
                word_sel()
        def pen_q_mp(): #function to have the player select how many penalties before game over
            pen_q_input_mp = str(input("The default penalties before game over is 5. Is that acceptable?\n\
Press Y to continue or N to change: "))
            if pen_q_input_mp.upper() == "Y":
                return 5
            elif pen_q_input_mp.upper() == "N":
                pen_num_mp = int(input("How many penalties do you wish?"))
                return pen_num_mp
            else:
                print("Invalid Input! Try again?")
                pen_q_mp()
        def display_mp(): #function to display the board state
            print("======================")
            print("Word: " + str(display_word_mp))
            print("Penalties: " + str(current_penalties) + "/" + str(penalty_limit))
            print("Guessed: " + str(already_guessed_mp))
            print("======================")
        #Functions are defined, game process begins
        word = word_sel()
        vic_limit_mp = len(word)
        penalty_limit = pen_q_mp()
        for n in range(0,len(word)):
            display_word_mp.append("*")
        turn_loop_mp = True
        while turn_loop_mp: #The main loop that determines the flow of the game in mp mode
            #Gonna open up with some DEBUG commands
            #print("Penalty Limit: " + str(penalty_limit))
            print("Word: " + str(word))
            ################
            display_mp()
            potential_point_mp = False
            penalty_this_turn = False
            good_guess_mp = False
            #vic check here
            if vic_points_mp >= vic_limit_mp:
                print("You win!")
                break
            elif current_penalties >= penalty_limit:
                print("You lose!")
                break
            player_guess_mp = str(input("Guess a letter: "))
            if player_guess_mp.upper() not in already_guessed_mp:
                already_guessed_mp.append(player_guess_mp.upper())
                potential_point_mp = True
            for n in range(0,len(word)):
                if player_guess_mp.upper() == word[n]:
                    display_word_mp[n] = word[n]
                    if potential_point_mp == True:
                        vic_points_mp += 1
                        good_guess_mp = True
            if good_guess_mp == False and potential_point_mp == True:
                current_penalties += 1
    else:
        mpGame()



    
def spGame():
    menuInput_sp = str(input("Single Player! Continue?\nY to continue or Q to go back\n"))
    if menuInput_sp.upper() == "Q":
       main()
    elif menuInput_sp.upper() == "Y":
       category_list = ["Vehicles","Animals","Food","Activities","Army Ranks","Countries","Geography"]
       category_vehicles = ["Car","Boat","Truck","Plane","Train","Tank","Bus","Coach","Buggy","Ship","Rocket","Glider"]
       category_animals = ["Cat","Dog","Cow","Ferret","Monkey","Shark","Whale","Raccoon","Otter","Lion","Rat","Bat"]
       category_food = ["Pizza","Apple","Banana","Burger","Soda","Taco","Burrito","Orange","Bread","Pear","Peach","Apricot"]
       category_activities = ["Running","Gaming","Swimming","Eating","Sleeping","Sitting","Jumping",\
                              "Playing","Writing","Learning","Coding","Teaching"]
       category_army_ranks = ["Private","Specialist","Corporal","Sergeant","Lieutenant","Captain","Major","Colonel","General"]
       #Army ranks wouldn't work with ranks that are more than one word long, or at least it wouldn't be very fun
       category_countries = ["America","Mexico","Canada","Britain","Brazil","France","Germany","India","Russia","China","Korea","Japan"]
       category_geography = ["Peninsula","Gulf","Ocean","River","Mountain","Plains","Swamp","Forest","Depression","Hill","Valley","Saddle"]
       random.shuffle(category_list)
       #print(category_list[0]) #DEBUG
       active_category = category_list[0]
       active_word = None
       if active_category == "Vehicles":
           random.shuffle(category_vehicles)
           active_word = category_vehicles[0]
       elif active_category == "Animals":
           random.shuffle(category_animals)
           active_word = category_animals[0]
       elif active_category == "Food":
           random.shuffle(category_food)
           active_word = category_food[0]
       elif active_category == "Activities":
           random.shuffle(category_activities)
           active_word = category_activities[0]
       elif active_category == "Army Ranks":
           random.shuffle(category_army_ranks)
           active_word = category_army_ranks[0]
       elif active_category == "Countries":
           random.shuffle(category_countries)
           active_word = category_countries[0]
       elif active_category == "Geography":
           random.shuffle(category_geography)
           active_word = category_geography[0]
       active_word = active_word.upper()    
       #print(active_word) #DEBUG
       penalty_limit = None
       print("\nThe default penalty limit is 5, would you like to change that?")
       def pen_q():
           pen_q_input = str(input("\n Y for yes, N for no: "))
           if pen_q_input.upper() == "Y":
               pen_q_input_change = int(input("\nEnter a number of penalties for your limit: "))
               return pen_q_input_change
           elif pen_q_input.upper() == "N":
               return 5
           else:
               pen_q()
       penalty_limit = pen_q()
       #print(penalty_limit)#DEBUG
       display_word = []
       for n in active_word:
           display_word.append("*")   
       current_penalties = 0
       already_guessed = []       
       def display():
           print("=========================")
           print("Word: " + str(display_word))
           print("Category: " + active_category)
           print("Penalties: " + str(current_penalties) + "/" + str(penalty_limit))
           print("GUESSED: " + str(already_guessed))
           #print("guess_num: " + str(guess_num)) #DEBUG
           print("=========================")
       #Now for the turn cycle
       turn_loop_sp = True
       guess_num = 0
       while turn_loop_sp:
           display()
           #VIC CHECK HERE
           vic_num = len(active_word)
           if current_penalties >= penalty_limit:
               print("Game over! The word was: " + str(active_word))
               break
           elif guess_num >= vic_num:
               print("You win!\n")
               break
           good_guess = False
           player_guess = str(input("\nSelect a letter: "))
           player_guess = player_guess.upper()
           possible_point_this_turn = False
           if player_guess not in already_guessed:
               already_guessed.append(player_guess)
               possible_point_this_turn = True
           #print(player_guess) #DEBUG
           for n in range(0,len(active_word)):
               if active_word[n] == player_guess:
                   display_word[n] = player_guess
                   good_guess = True
                   if possible_point_this_turn == True:
                       guess_num += 1
           if good_guess == False:
               current_penalties += 1
    else:
        spGame()



        
def main():
    main_loop = True
    while main_loop:
        print("Welcome to Hangman!\nPress 1 for Single Player!\nOr 2 for 2-player!\n\
Or Q to quit!\n")
        main_menu_input = str(input("Select: "))
        if main_menu_input == "1":
            spGame()
        elif main_menu_input == "2":
            mpGame()
        elif main_menu_input.upper() == "Q":
            break
        else:
            main()

main()
