"""
19 AUG 2018
Sam Gibson

Graphical Hangman with PyGame - Rough Draft

Missing Features: High Score List and Options Menu

All other features complete. Hangman game works, animations work, sound works, can play games back to back to back
to back without issue. Can skip ahead of the sound and animations and the game will play along nicely, despite
my sloppy coding.

Using the vocab.py file it is relatively easy to add new words to the existing categories or add entirely new
categories. One area I want to polish is in creating a streamlined system for adding words.

"""

# imports:
import random
import pygame
import vocab

# CONSTANTS
SCREEN_SIZE = (640, 360)  # for now. I've heard 640 x 360 is a good place to start
FPS = 30  # Doesn't even need to be this high, but it's good practice
BG_COLOR = (118, 171, 145)  # A much lighter green
FG_COLOR = (26, 87, 57)  # a sort of dark green
TEXT_COLOR = (255, 255, 255)  # white

# Stuff for the options menu
PENALTY_LIMIT = 8  # The default penalty limit. I intend to make this adjustable in the options.
MUSIC_ENABLED = True  # I intend to make this adjustable in the options
PLAYER_NAME = "PLAYER 1"  # I intend to make this adjustable in the options

# PYGAME INIT and MAIN DISPLAY SURFACES
pygame.mixer.init()  # init the mixer
pygame.init()  # init PyGame
MAIN_SURFACE = pygame.display.set_mode(SCREEN_SIZE)  # init the MAIN SURFACE
FG_SURFACE = pygame.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1] * (1 / 3)))  # for all intents and purposes, a DIV
G0_SURFACE = pygame.Surface(SCREEN_SIZE)  # Just a game over screen
MENU_POINTER = pygame.Surface((7, 7))  # Just a little menu cursor
pygame.display.set_caption("GRAPHICAL HANGMAN")  # Might change this to something witty later
icon_graphic = pygame.image.load("res/G_Hangman_Icon.png").convert_alpha()  # I like this icon, it is morbid and simple
pygame.display.set_icon(icon_graphic)  # set the icon
GAME_CLOCK = pygame.time.Clock()  # init the GAME CLOCK
# will probably use some custom timers and some more stuff here
# Timer for the title animation
pygame.time.set_timer(pygame.USEREVENT+1, 280)

# LOAD SOUND (just effects and warbles, no looping music for this one)

# Some sounds to play during Hangsprite's animations
sound_shuffle = pygame.mixer.Sound("res/shufflestep.wav")
sound_rope_lower = pygame.mixer.Sound("res/rope_lower.wav")
sound_horn = pygame.mixer.Sound("res/hangsprite_trumpet.wav")
sound_drop = pygame.mixer.Sound("res/drop.wav")

# Some little warbles to play during the splash screens:
sound_victory_warble = pygame.mixer.Sound("res/victory_warble.wav")
sound_defeat_womp = pygame.mixer.Sound("res/loser_womp.wav")

# A short title tune
sound_title_tune = pygame.mixer.Sound("res/entry_warble.wav")


# LOAD ART (not yet)
# Title Screen (totally a placeholder)
game_over_sheet = pygame.image.load("res/graphical_hangman_menu_graphic_bigsheet.png").convert_alpha()
hangsprite_bigsheet = pygame.image.load("res/graphical_hangman_hangsprite_bigsheet.png").convert_alpha()


# STRUCTURES AND CLASSES
# The categories and the words they contain. Just some basic stuff for testing to start.
class Category:
    def __init__(self, name):
        self.word_list = []
        self.name = name

    def add_word(self, c_word):
        self.word_list.append(str(c_word).upper())


cat_animals = Category("animals")  # ANIMALS
for word in range(0, len(vocab.animals)):
    cat_animals.add_word(vocab.animals[word])

cat_food = Category("food")  # FOOD
for word in range(0, len(vocab.food)):
    cat_food.add_word(vocab.food[word])

cat_geography = Category("geography")  # GEOGRAPHIC VOCAB
for word in range(0, len(vocab.geography)):
    cat_geography.add_word(vocab.geography[word])

cat_military = Category("military")  # MILITARY VOCAB
for word in range(0, len(vocab.military)):
    cat_military.add_word(vocab.military[word])

cat_space = Category("space")  # SPACE VOCAB
for word in range(0, len(vocab.space)):
    cat_space.add_word(vocab.space[word])

cat_nature = Category("nature")  # NATURE VOCAB
for word in range(0, len(vocab.nature)):
    cat_nature.add_word(vocab.nature[word])

cat_vehicles = Category("vehicles")  # VEHICLE RELATED
for word in range(0, len(vocab.vehicles)):
    cat_vehicles.add_word(vocab.vehicles[word])

cat_music = Category("music")  # MUSIC RELATED
for word in range(0, len(vocab.music)):
    cat_music.add_word(vocab.music[word])

cat_instruments = Category("instruments")  # INSTRUMENT RELATED
for word in range(0, len(vocab.instruments)):
    cat_instruments.add_word(vocab.instruments[word])

cat_household = Category("household")  # HOUSEHOLD RELATED
for word in range(0, len(vocab.household)):
    cat_household.add_word(vocab.household[word])

cat_history = Category("history")  # HISTORY RELATED, SORT OF
for word in range(0, len(vocab.history)):
    cat_history.add_word(vocab.history[word])

cat_technology = Category("technology")  # TECHNOLOGY RELATED
for word in range(0, len(vocab.technology)):
    cat_technology.add_word(vocab.technology[word])

cat_politics = Category("politics")  # POLITICS RELATED
for word in range(0, len(vocab.parties)):
    cat_politics.add_word(vocab.politics[word])

cat_fantasy = Category("fantasy")  # FANTASY RELATED
for word in range(0, len(vocab.fantasy)):
    cat_fantasy.add_word(vocab.fantasy[word])

cat_gaming = Category("gaming")  # GAMING RELATED
for word in range(0, len(vocab.gaming)):
    cat_gaming.add_word(vocab.gaming[word])

cat_school = Category("school")  # SCHOOL RELATED
for word in range(0, len(vocab.school)):
    cat_school.add_word(vocab.school[word])

cat_internet = Category("internet")  # INTERNET RELATED
for word in range(0, len(vocab.internet)):
    cat_internet.add_word(vocab.internet[word])

cat_parties = Category("parties")  # PARTYING RELATED
for word in range(0, len(vocab.parties)):
    cat_parties.add_word(vocab.parties[word])

cat_math = Category("math")  # MATH RELATED
for word in range(0, len(vocab.math)):
    cat_math.add_word(vocab.math[word])

cat_challenge = Category("challenge")  # CHALLENGE WORDS
for word in range(0, len(vocab.challenge)):
    cat_challenge.add_word(vocab.challenge[word])


# and many more


class CategoryList:
    def __init__(self):
        self.category_list = []

    def add_category(self, category):
        self.category_list.append(category)


# Spawn the main instance of the category master list
category_master_list = CategoryList()

# Each category has to be added to the master list here:
category_master_list.add_category(cat_animals)
category_master_list.add_category(cat_food)
category_master_list.add_category(cat_geography)
category_master_list.add_category(cat_military)
category_master_list.add_category(cat_space)
category_master_list.add_category(cat_nature)
category_master_list.add_category(cat_vehicles)
category_master_list.add_category(cat_music)
category_master_list.add_category(cat_instruments)
category_master_list.add_category(cat_household)
category_master_list.add_category(cat_history)
category_master_list.add_category(cat_technology)
category_master_list.add_category(cat_politics)
category_master_list.add_category(cat_fantasy)
category_master_list.add_category(cat_gaming)
category_master_list.add_category(cat_school)
category_master_list.add_category(cat_internet)
category_master_list.add_category(cat_parties)
category_master_list.add_category(cat_math)
category_master_list.add_category(cat_challenge)


class HangSprite:  # The animated sprite which is the hanged man
    def __init__(self):
        self.sheet = hangsprite_bigsheet
        self.cell_width = 500
        self.cell_height = 100
        self.frame_x = 0
        self.frame_y = 0
        self.frame_max = 37
        self.frame_counter = 0
        self.animation_finished = False
        self.cell_list = []
        for y in range(0, 13):
            for x in range(0, 3):
                self.cell_list.append((x * 500, y * 100, 500, 100))
        # animation phases:
        # 0 = No Penalties, starts on frame 0 and sticks on frame 3
        # 1 = Some Penalties, starts on frame 3 and sticks on frame 20 (walks to noose)
        # 2 = More Penalties, starts on frame 20 and sticks on frame 32 (rope lowers and goes around his neck)
        # 3 = Even More Penalties, starts on frame 32 and sticks on frame 34 (executioner raises arm)
        # 4 = Max penalties, starts on frame 34 and sticks on frame 37 (hangsprite gets hanged)
        self.phase = 0
        self.dt = 0

    # I am going to attempt a delta time animation here instead of the pygame.USEREVENT timer I usually use
    def update_hangsprite(self):
        # Blit the appropriate rect from the sprite sheet
        MAIN_SURFACE.blit(self.sheet, (0, SCREEN_SIZE[1] * .15), self.cell_list[self.frame_counter])
        if self.dt >= 800:                        # if it has been more than 800ms since the last animation frame:
            if self.phase is 0:                   # and it is in phase 0:
                if self.frame_counter < 3:        # if the frame counter is less than 3
                    self.frame_counter += 1       # add 1 to the frame counter
                    self.dt = 0                   # Reset the delta time variable
            elif self.phase is 1:                 # Or if it is in phase 1
                if self.frame_counter < 20:       # and the frame counter is less than 20
                    self.frame_counter += 1       # add 1 to the frame counter
                    self.dt = 0                   # and reset the delta time variable
                    sound_shuffle.play()          # And play a "footsteps" sound effect I made with bfxr
            elif self.phase is 2:                 # or if it is in phase 2
                if self.frame_counter < 32:       # and the frame counter is at less than 32
                    self.frame_counter += 1       # add 1 to the frame counter
                    self.dt = 0                   # reset the delta time variable
                    sound_rope_lower.play()       # play a "ropey" sound effect I made with bfxr
            elif self.phase is 3:                 # or if it is in phase 3
                if self.frame_counter < 34:       # and the frame counter is less than 34
                    self.frame_counter += 1       # add 1 to the frame counter
                    self.dt = 0                   # reset the delta time variable
                    if self.frame_counter is 33:  # If it is specifically on frame 33
                        sound_horn.play()         # Play a little trumpet blare warble I made with bosca ceoil
            elif self.phase is 4:                 # or if it is phase 4
                if self.frame_counter < 37:       # and the frame counter is less than 37
                    self.frame_counter += 1       # add 1 to the frame counter
                    self.dt = 0                   # reset the delta time variable
                    if self.frame_counter is 36:  # If the frame counter is specifically on frame 36
                        sound_drop.play()         # Play the "drop" sound effect I made in bfxr


# The animated title screen
class TitleScreen:  # The class that governs the title screen animation and functionality
    def __init__(self):
        # Whether or not the menu is toggled on
        self.menu_on = True
        # Whether or not the game is in active play or not
        self.game_over = True
        self.space_to_continue = False  # A switch for use in the game over and vic screens
        # The image sprite sheet
        self.sheet = game_over_sheet
        self.cell_width = 640  # Cell width
        self.cell_height = 358  # Cell height
        self.frame_x = 0  # Which X-axis the frame tracker is at
        self.frame_y = 0  # Which y-axis the frame tracker is at
        self.frame_max = 22  # How many frames total in the sprite sheet
        self.frame_counter = 0  # Which frame we are currently on
        self.animation_finished = False  # Whether or not the animation is finished playing
        self.font = pygame.font.Font(None, 30)  # Font

        # Menu Options:
        self.text_0 = self.font.render("NEW GAME", False, TEXT_COLOR)
        self.text_1 = self.font.render("HIGH SCORES", False, TEXT_COLOR)  # not implemented yet
        self.text_2 = self.font.render("OPTIONS", False, TEXT_COLOR)  # not implemented yet
        self.text_3 = self.font.render("QUIT", False, TEXT_COLOR)

        # the pointer
        self.pointer_position = 0
        # A list of possible pointer positions
        self.pointer_pos_list = [(SCREEN_SIZE[0] * .60, SCREEN_SIZE[1] * .47), (SCREEN_SIZE[0] * .60, SCREEN_SIZE[1] * .57), (SCREEN_SIZE[0] * .60, SCREEN_SIZE[1] * .67), (SCREEN_SIZE[0] * .60, SCREEN_SIZE[1] * .77)]

    def draw_title(self):
        # display main menu
        G0_SURFACE.fill(0)
        MAIN_SURFACE.blit(G0_SURFACE, (0, 0))
        if self.animation_finished is False:
            # Play the title animation by frame:
            MAIN_SURFACE.blit(game_over_sheet, (0, 0), (self.frame_x * 640, self.frame_y * 358, 640, 358))
        elif self.animation_finished is True:
            # Reset the "gears" for the next play of the animation
            self.frame_y = 0
            self.frame_x = 0
            self.frame_counter = 0
            # Stick to the last frame of the intro animation
            MAIN_SURFACE.blit(game_over_sheet, (0, 0), (2 * 640, 5 * 358, 640, 358))
            # And display the menu options
            MAIN_SURFACE.blit(self.text_0, (SCREEN_SIZE[0] * .66, SCREEN_SIZE[1] * .45))
            MAIN_SURFACE.blit(self.text_1, (SCREEN_SIZE[0] * .66, SCREEN_SIZE[1] * .55))
            MAIN_SURFACE.blit(self.text_2, (SCREEN_SIZE[0] * .66, SCREEN_SIZE[1] * .65))
            MAIN_SURFACE.blit(self.text_3, (SCREEN_SIZE[0] * .66, SCREEN_SIZE[1] * .75))
            MENU_POINTER.fill(TEXT_COLOR)
            MAIN_SURFACE.blit(MENU_POINTER, self.pointer_pos_list[self.pointer_position])

    def title_animation_speeds(self):
        # This is a jerry-rigged method of doing time-based animation that uses pygame.USEREVENT timers that tick off
        # regularly at the desired speed rather than the simpler delta time method. Only reason it's still in here
        # is because it works even though I used delta time for the hangsprite.
        if self.frame_x is 3:
            self.frame_y += 1
            self.frame_x = 0
        elif self.frame_x < 3:
            self.frame_x += 1
        self.frame_counter += 1
        if self.frame_counter > self.frame_max:
            self.animation_finished = True


# The new game object
class NewGame:
    def __init__(self, player=PLAYER_NAME, penalty_limit=PENALTY_LIMIT):  # Will change these later in the options
        self.player = player
        self.penalty_limit = penalty_limit
        self.penalties = 0  # How many wrong guesses the player has made
        self.category = None  # The category
        self.word = None  # The word
        self.word_as_list = []  # the word in the form of a list
        self.letters_guessed = []  # the letters guessed so far during this playthrough
        self.points_to_win = 0  # How many correct guesses are required to win
        self.points_so_far = 0  # How many correct guesses so far
        self.display_word_as_list = []  # The display word that the player sees
        self.font = pygame.font.Font(None, 30)  # A font
        self.display_word_font = pygame.font.Font(None, 24)  # a smaller font
        self.has_warbled = False  # A boolean switch for keeping track of the victory/defeat warble sounds
        self.turn_taken = False  # Whether or not the player has taken their turn

    # Choose a new word at the beginning of the session
    def choose_word(self):
        # Clear the variables in question, like a re-initialization of the object
        self.word = None
        self.word_as_list = []
        self.letters_guessed = []
        self.display_word_as_list = []
        # A list for keeping track of letters
        letters = []
        # Choose a category from the master list
        self.category = random.choice(category_master_list.category_list)
        # Choose a word from the category's word list
        self.word = random.choice(self.category.word_list)
        # Add an amount of underscores to the display word string that is equal to the length of the chosen word
        for n in range(len(self.word)):
            self.display_word_as_list.append("_")

        for letter in self.word:
            self.word_as_list.append(letter)  # Add the correct letters to the "list" version of the word
            if letter not in letters:  # If the letter has not already been added (prevents double-counting the same letter)
                letters.append(letter)  # add it to the list
                self.points_to_win += 1  # And add a point required for winning

    def draw_game(self):
        # clear display surface
        # MAIN_SURFACE.fill(0)
        # update background
        MAIN_SURFACE.fill(BG_COLOR)
        # update foreground and text
        FG_SURFACE.fill(FG_COLOR)
        MAIN_SURFACE.blit(FG_SURFACE, (0, SCREEN_SIZE[1] * (2 / 3)))

        # update animations (no animations yet)

        # Display the chosen word and category:
        display_word = self.display_word_font.render("Your word: " + str(self.display_word_as_list), False, TEXT_COLOR)
        chosen_category = self.font.render("From category: " + str(self.category.name).upper(), False, TEXT_COLOR)
        player_penalties = self.font.render("Penalties: " + str(self.penalties) + "/" + str(self.penalty_limit), False, TEXT_COLOR)
        prompt_for_letter = self.font.render("Pick a letter!", False, TEXT_COLOR)
        MAIN_SURFACE.blit(display_word, (SCREEN_SIZE[0] * .1, SCREEN_SIZE[1] * .7))
        MAIN_SURFACE.blit(chosen_category, (SCREEN_SIZE[0] * .1, SCREEN_SIZE[1] * .85))
        MAIN_SURFACE.blit(player_penalties, (SCREEN_SIZE[0] * .6, SCREEN_SIZE[1] * .85))
        MAIN_SURFACE.blit(prompt_for_letter, (SCREEN_SIZE[0] * .6, SCREEN_SIZE[1] * .55))

        # DEBUG CHEAT, remove this when finished
        # debug_word = self.font.render("THE WORD: " + str(self.word), False, TEXT_COLOR)
        # MAIN_SURFACE.blit(debug_word, (10, 10))
        # debug_points = self.font.render("Points to win: " + str(self.points_to_win), False, TEXT_COLOR)
        # MAIN_SURFACE.blit(debug_points, (10, 25))


# FUNCTIONS


# MAIN
def main():
    title_screen = TitleScreen()  # init the title screen object
    game_loop = True
    new_game = NewGame()  # init the game object
    hangsprite = HangSprite()  # init the hangsprite animation object

    def reset_game():  # this function resets the game in between words by resetting multiple variables found elsewhere.
        title_screen.game_over = True
        # Reset stuff
        title_screen.menu_on = True
        new_game.points_so_far = 0
        new_game.points_to_win = 0
        new_game.penalties = 0
        hangsprite.frame_counter = 0
        new_game.has_warbled = False

    # Game loop starts
    while game_loop:

        # Check event queue
        for event in pygame.event.get():

            # Check for quit functionality
            if event.type is pygame.QUIT:
                game_loop = False

            # Animation speed limits for the title animation (NOT delta time)
            if event.type is pygame.USEREVENT+1:
                title_screen.title_animation_speeds()

            # Check for key-presses. Eventually I'll need to go through every key.
            if event.type is pygame.KEYUP:

                # "space to continue"
                if event.key is pygame.K_SPACE:  # if they press space
                    if title_screen.space_to_continue is True:  # and the "space to continue" message is showing
                        reset_game()  # then reset the game
                        title_screen.space_to_continue = False  # and remove the "space to continue" flag

                # If the main menu is on
                if title_screen.menu_on is True:
                    # For now this will double as the "up" key
                    if event.key is pygame.K_w:
                        if title_screen.pointer_position is not 0:
                            title_screen.pointer_position -= 1

                    # For now this will double as the "down" key
                    if event.key is pygame.K_s:
                        if title_screen.pointer_position is not 3:
                            title_screen.pointer_position += 1

                    # The enter key, of course
                    if event.key is pygame.K_RETURN:
                        # New Game
                        if title_screen.pointer_position is 0:
                            # A whole bunch of game resetting stuff
                            title_screen.game_over = False  # Change the game state
                            title_screen.menu_on = False
                            title_screen.animation_finished = False  # Reset the title animation for later use
                            hangsprite.animation_finished = False
                            hangsprite.dt = 0
                            hangsprite.phase = 0
                            new_game.choose_word()
                            sound_title_tune.play()  # Play the title warble I made with bosca ceoil

                        # High Scores
                        elif title_screen.pointer_position is 1:
                            pass  # NOT IMPLEMENTED YET

                        # Options (penalty limits, maybe music)
                        elif title_screen.pointer_position is 2:
                            pass  # NOT IMPLEMENTED YET

                        # Quit
                        elif title_screen.pointer_position is 3:
                            game_loop = False

                # If the main menu or game over screen is not active
                # Loop through each letter and use a function to check and apply points or penalties
                elif title_screen.menu_on is False:
                    if new_game.turn_taken is False:

                        # if the letter is in the chosen word
                        def letter_checker(letter):
                            if letter in new_game.word:
                                # Swap out the display letters so the player can see what they got
                                for let in range(0, len(new_game.word_as_list)):
                                    if new_game.word_as_list[let] is letter:
                                        new_game.display_word_as_list[let] = letter
                                # And it hasn't already been guessed
                                if letter not in new_game.letters_guessed:
                                    # Add it to the list of letters guessed
                                    new_game.letters_guessed.append(letter)
                                    # And add some victory points to the counter
                                    new_game.points_so_far += 1
                                    # Mark the turn as over
                                    new_game.turn_taken = True
                            # Otherwise, if the letter is not in the chosen word
                            else:
                                if letter not in new_game.letters_guessed:
                                    # Add it to the list of letters guessed
                                    new_game.letters_guessed.append(letter)
                                    # Add a penalty if letter not already guessed
                                    new_game.penalties += 1
                                    # And mark the turn as over, so the animation can play (eventually)
                                    new_game.turn_taken = True

                        # The letters of the alphabet. For each one, apply the function that checks to see
                        # if it is valid and acts accordingly.
                        if event.key is pygame.K_a:
                            letter_checker("A")
                        elif event.key is pygame.K_b:
                            letter_checker("B")
                        elif event.key is pygame.K_c:
                            letter_checker("C")
                        elif event.key is pygame.K_d:
                            letter_checker("D")
                        elif event.key is pygame.K_e:
                            letter_checker("E")
                        elif event.key is pygame.K_f:
                            letter_checker("F")
                        elif event.key is pygame.K_g:
                            letter_checker("G")
                        elif event.key is pygame.K_h:
                            letter_checker("H")
                        elif event.key is pygame.K_i:
                            letter_checker("I")
                        elif event.key is pygame.K_j:
                            letter_checker("J")
                        elif event.key is pygame.K_k:
                            letter_checker("K")
                        elif event.key is pygame.K_l:
                            letter_checker("L")
                        elif event.key is pygame.K_m:
                            letter_checker("M")
                        elif event.key is pygame.K_n:
                            letter_checker("N")
                        elif event.key is pygame.K_o:
                            letter_checker("O")
                        elif event.key is pygame.K_p:
                            letter_checker("P")
                        elif event.key is pygame.K_q:
                            letter_checker("Q")
                        elif event.key is pygame.K_r:
                            letter_checker("R")
                        elif event.key is pygame.K_s:
                            letter_checker("S")
                        elif event.key is pygame.K_t:
                            letter_checker("T")
                        elif event.key is pygame.K_u:
                            letter_checker("U")
                        elif event.key is pygame.K_v:
                            letter_checker("V")
                        elif event.key is pygame.K_w:
                            letter_checker("W")
                        elif event.key is pygame.K_x:
                            letter_checker("X")
                        elif event.key is pygame.K_y:
                            letter_checker("Y")
                        elif event.key is pygame.K_z:
                            letter_checker("Z")

        # TURN CYCLE

        if title_screen.game_over is False:  # If the game is running
            if new_game.points_so_far >= new_game.points_to_win:  # and if they have more points than they need to win
                # user presses space to reset the game
                title_screen.space_to_continue = True
                # A victory warble if it has not played yet:
                if new_game.has_warbled is False:
                    sound_victory_warble.play()
                    new_game.has_warbled = True
            # else if they have more penalties than the penalty limit
            elif new_game.penalties >= new_game.penalty_limit:
                # play the hangsprite defeat animation
                hangsprite.phase = 4
                # user can press space to reset game
                title_screen.space_to_continue = True
                # A loser womp-womp if it hasn't played yet:
                if new_game.has_warbled is False:
                    sound_defeat_womp.play()
                    new_game.has_warbled = True
            else:
                # Check to see if the hangman needs to go to the next phase
                # Phase 1 threshold 25%
                if new_game.penalties >= new_game.penalty_limit * .25 and new_game.penalties < new_game.penalty_limit * .5:
                    hangsprite.phase = 1
                # Phase 2 threshold 50%
                elif new_game.penalties >= new_game.penalty_limit * .50 and new_game.penalties < new_game.penalty_limit * .75:
                    hangsprite.phase = 2
                # phase 3 threshold 75%
                elif new_game.penalties >= new_game.penalty_limit * .75 and new_game.penalties < new_game.penalty_limit:
                    hangsprite.phase = 3

                # Restart the turn-cycle
                new_game.turn_taken = False

        # DRAW PORTION
        # If just booted up or after a session
        if title_screen.game_over is True:
            # Run the title screen
            title_screen.draw_title()
        # otherwise, if in the middle of a game, draw the game
        elif title_screen.game_over is False:
            new_game.draw_game()  # The main draw sequence
            # AND, draw the HangSprite! His animations will accompany everything else.
            hangsprite.update_hangsprite()
            # Draw space to continue vic/def popups
            if new_game.points_so_far >= new_game.points_to_win:
                # VICTORY POPUP
                def_pop = pygame.Surface((SCREEN_SIZE[0], 50))
                def_pop.fill(0)
                def_text = title_screen.font.render("YOU WIN! Space to continue...", False, TEXT_COLOR)
                MAIN_SURFACE.blit(def_pop, (0, SCREEN_SIZE[1] * .5))
                MAIN_SURFACE.blit(def_text, (0, SCREEN_SIZE[1] * .52))
                debug_word = title_screen.font.render("THE WORD WAS: " + str(new_game.word), False, TEXT_COLOR)
                def_pop.fill(0)
                MAIN_SURFACE.blit(def_pop, (0, SCREEN_SIZE[1] * .01))
                MAIN_SURFACE.blit(debug_word, (0, SCREEN_SIZE[1] * .03))
            elif new_game.penalties >= new_game.penalty_limit:
                # DEFEAT POPUP
                def_pop = pygame.Surface((SCREEN_SIZE[0], 50))
                def_pop.fill(0)
                def_text = title_screen.font.render("YOU LOSE! Space to continue...", False, TEXT_COLOR)
                MAIN_SURFACE.blit(def_pop, (0, SCREEN_SIZE[1] * .5))
                MAIN_SURFACE.blit(def_text, (0, SCREEN_SIZE[1] * .52))
                debug_word = title_screen.font.render("THE WORD WAS: " + str(new_game.word), False, TEXT_COLOR)
                def_pop.fill(0)
                MAIN_SURFACE.blit(def_pop, (0, SCREEN_SIZE[1] * .01))
                MAIN_SURFACE.blit(debug_word, (0, SCREEN_SIZE[1] * .03))

        # flip the display
        pygame.display.flip()

        # pump the queue
        pygame.event.pump()

        dt = GAME_CLOCK.tick(FPS)  # Keep it at 30 FPS
        hangsprite.dt += dt  # Whoah this actually works, way easier than my "gears."

    pygame.quit()  # Exit the app if the user leaves the game loop by clicking the X


if __name__ == "__main__":
    main()
