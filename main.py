"""
Graphical Hangman v1:

A simple game of hangman, in a pygame instance. It has multiple difficulty levels, a small but easily expanded
vocabulary, improved animations and sound over v0, and a fully clickable menu interface (where v0 was key-strokes only).
"""

import pygame
import vocab

SIZE = (640, 360)  # resolution
FPS = 30

pygame.mixer.init()  # init mixer
pygame.init()        # init pygame

MAIN_SURFACE = pygame.display.set_mode(SIZE)           # main surface
FG_SURFACE = pygame.Surface((SIZE[0], SIZE[1] * .33))  # the bottom-third of the game screen
FG_LOC = (0, SIZE[1] * .69)                            # The positioning of the bottom third

VM = vocab.VocabManager()  # The word and category stuff, in an object

# Window Icon and Caption
pygame.display.set_caption("Graphical Hangman v1")
icon_graphic = pygame.image.load("res/G_Hangman_Icon.png").convert_alpha()
pygame.display.set_icon(icon_graphic)


GAME_CLOCK = pygame.time.Clock()  # game clock

# Some colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BG_COLOR = (118, 171, 145)  # A much lighter green
FG_COLOR = (26, 87, 57)  # a sort of dark green

# some fonts, all using the default pygame font
NORMAL_FONT = pygame.font.Font(None, 30)
SMALLER_FONT = pygame.font.Font(None, 24)
LARGER_FONT = pygame.font.Font(None, 40)

# Some permanent locations on the menu screen:
TEXT_POS_1 = (SIZE[0] * .66, SIZE[1] * .45)  # Top spot on the menu
TEXT_POS_2 = (SIZE[0] * .66, SIZE[1] * .55)  # 2nd down
TEXT_POS_3 = (SIZE[0] * .66, SIZE[1] * .65)  # 3rd down
TEXT_POS_4 = (SIZE[0] * .66, SIZE[1] * .75)  # 4th down

TEXT_POS_5 = (SIZE[0] * .25, SIZE[1] * .65)  # An extra spot for use in the options menu and maybe other things

# LOAD SOUNDS
# Some sounds to play during Hangsprite's animations
sound_rope_lower = pygame.mixer.Sound("res/rope_lower.wav")  # A "ropey" sound
sound_horn = pygame.mixer.Sound("res/hangsprite_trumpet.wav")  # a little trumpet blare
sound_drop = pygame.mixer.Sound("res/drop.wav")  # a "CLUNK" sound

# A short title tune
sound_title_tune = pygame.mixer.Sound("res/entry_warble.wav")  # A little entry tune with horn and drums

# LOAD ART
# The oversized sprite sheets for the title graphic and the background sprite.
game_over_sheet = pygame.image.load("res/graphical_hangman_menu_graphic_bigsheet.png").convert_alpha()
hangsprite_bigsheet = pygame.image.load("res/hangsprite_2.png").convert_alpha()


# All the stuff for the options menu, including surfaces and hitboxes
class Options:
    def __init__(self):
        self.music_enabled = True  # whether sound is on or off
        self.penalty_limit = 8  # Difficulty Level (4=HARD,6=MEDIUM,8=EASY,10=VERY EASY)

        # the menu options. For each option:
        # a Font.render() Surface
        # a location on the screen
        # a hitbox for using the Rect.collidepoint() function

        # increase difficulty
        self.increase_text = NORMAL_FONT.render("HARDER", False, WHITE)
        self.increase_loc = TEXT_POS_1
        self.increase_hitbox = pygame.Rect(self.increase_loc, (self.increase_text.get_width(), self.increase_text.get_height()))

        # decrease difficulty
        self.decrease_text = NORMAL_FONT.render("EASIER", False, WHITE)
        self.decrease_loc = TEXT_POS_2
        self.decrease_hitbox = pygame.Rect(self.decrease_loc, (self.decrease_text.get_width(), self.decrease_text.get_height()))

        # enable/disable sound
        self.sound_text = NORMAL_FONT.render("SOUND OFF/ON", False, WHITE)
        self.sound_loc = TEXT_POS_3
        self.sound_hitbox = pygame.Rect(self.sound_loc, (self.sound_text.get_width(), self.sound_text.get_height()))

        # back
        self.back_text = NORMAL_FONT.render("BACK", False, WHITE)
        self.back_loc = TEXT_POS_4
        self.back_hitbox = pygame.Rect(self.back_loc, (self.back_text.get_width(), self.back_text.get_height()))

        # update (displays whatever just happened)
        self.update_status = " "  # " ","SOUND OFF","SOUND ON","VERY EASY","EASY","MEDIUM","HARD"
        self.update_text = NORMAL_FONT.render(str(self.update_status), False, WHITE)
        self.update_loc = TEXT_POS_5
        # end of menu options

    # Turns the sound on and off by flipping the boolean
    def switch_music(self):
        if self.music_enabled is True:
            self.music_enabled = False
        elif self.music_enabled is False:
            self.music_enabled = True

    # Lowers the difficulty to the next level
    # takes the current penalty limit, lowers it,
    # and sets the new penalty limit
    def decrease_difficulty(self, current_limit):
        switches = {"4": 6, "6": 8, "8": 10}
        self.penalty_limit = switches.get(str(current_limit))

    # Does the same as the above, but increases the difficulty
    def increase_difficulty(self, current_limit):
        switches = {"10": 8, "8": 6, "6": 4}
        self.penalty_limit = switches.get(str(current_limit))

    # This shows the user a font surface with text
    # that tells them what they just did in the options menu
    def change_update_status_diff(self, diff):
        status_dict = {"4": "HARD", "6": "MEDIUM", "8": "EASY", "10": "VERY EASY"}
        self.update_status = status_dict.get(str(diff))
        self.update_text = NORMAL_FONT.render(str(self.update_status), False, WHITE)

    # Does the same as the above, but for the sound option
    def change_update_status_sound(self):
        if self.music_enabled is True:
            self.update_status = "SOUND ON"
        if self.music_enabled is False:
            self.update_status = "SOUND OFF"
        self.update_text = NORMAL_FONT.render(str(self.update_status), False, WHITE)

    # takes the mouse coordinates from the event handling part of the game loop
    # and uses them to check to the hitboxes for the clickable interface
    # applied the effects of each button in the process.
    def options_hitboxes(self, x, y):                                  # takes mouse coords
        if self.increase_hitbox.collidepoint(x, y):                    # checks the increase hitbox
            if self.penalty_limit > 4:                                 # checks current difficulty
                self.increase_difficulty(self.penalty_limit)           # raise the difficulty
                self.change_update_status_diff(self.penalty_limit)     # update the player of the change
        elif self.decrease_hitbox.collidepoint(x, y):                  # checks decrease hitbox
            if self.penalty_limit < 10:                                # checks the difficulty
                self.decrease_difficulty(self.penalty_limit)           # lowers the difficulty
                self.change_update_status_diff(self.penalty_limit)     # notify the player
        elif self.sound_hitbox.collidepoint(x, y):                     # check the sound hitbox
            self.switch_music()                                        # turn music on/off
            self.change_update_status_sound()                          # notify the player
        elif self.back_hitbox.collidepoint(x, y):                      # check the back button hitbox
            title_screen.menu_state = "MAIN"                           # sends player back to main menu


# The instance of the Options class that I will be using
options = Options()


# The animated title screen, surfaces, data, and the animated background
class TitleScreen:
    def __init__(self):
        self.sheet = game_over_sheet  # The sprite sheet for the title screen
        self.cell_w = 640  # the width of a cell on the sheet
        self.cell_h = 358  # the height
        self.sheet_frames_x = 4  # how many frames wide the sheet is
        self.sheet_frames_y = 6  # how many frames tall the sheet is

        # creates a tuple which represents the rect required to blit a portion of the
        # master sheet, for each frame of the animation, and stores them in an ordered list.
        self.frames = []
        for y in range(0, self.sheet_frames_y):
            for x in range(0, self.sheet_frames_x):
                # adds a rect tuple for each frame of the sheet
                self.frames.append((x * self.cell_w, y * self.cell_h, self.cell_w, self.cell_h))

        self.frame_counter = 0  # which frame the animation is currently "on"
        self.frame_max = 22     # the total frames in the animation
        self.dt = 0             # The delta time for this animation (ms since last frame-change)

        # The menu state determines what is drawn on the screen later in the update() function
        self.menu_state = "MAIN"  # "MAIN", "OPTIONS", "HIGH SCORE", "GAME", "QUIT"

        # For each button on the main menu:
        # a text surface
        # a location on the map
        # and a hitbox for using the mouse in the form of a Rect object.

        # The new game button
        self.new_game_text = NORMAL_FONT.render("NEW GAME", False, WHITE)
        self.new_game_loc = TEXT_POS_1
        self.new_game_text_hitbox = pygame.Rect(self.new_game_loc, (self.new_game_text.get_width(), self.new_game_text.get_height()))

        # the options button
        self.options_text = NORMAL_FONT.render("OPTIONS", False, WHITE)
        self.options_loc = TEXT_POS_2
        self.options_text_hitbox = pygame.Rect(self.options_loc, (self.options_text.get_width(), self.options_text.get_height()))

        # the high score button
        self.high_score_text = NORMAL_FONT.render("HIGH SCORES", False, WHITE)
        self.high_score_loc = TEXT_POS_3
        self.high_score_text_hitbox = pygame.Rect(self.high_score_loc, (self.high_score_text.get_width(), self.high_score_text.get_height()))

        # the quit button
        self.quit_text = NORMAL_FONT.render("QUIT", False, WHITE)
        self.quit_loc = TEXT_POS_4
        self.quit_text_hitbox = pygame.Rect(self.quit_loc, (self.quit_text.get_width(), self.quit_text.get_height()))

    # Checks to see if any of the hitboxes are being touched
    # using the Rect.collidepoint() function
    # and if so, applies their effects
    def main_hitboxes(self, x, y):                                    # takes the mouse coordinates
        if self.quit_text_hitbox.collidepoint(x, y):                  # checks the quit hitbox
            self.menu_state = "QUIT"                                  # changes the menu state to "QUIT"
        elif self.options_text_hitbox.collidepoint(x, y):             # checks the options hitbox
            self.menu_state = "OPTIONS"                               # changes the menu state to "OPTIONS"
        elif self.new_game_text_hitbox.collidepoint(x, y):            # checks the new game hitbox
            self.menu_state = "GAME"                                  # changes the state to "GAME"
            # and some other stuff probably
            reset()                                                   # resets the game
            if options.music_enabled is True:                         # checks to see if the music is enabled
                sound_title_tune.play()                               # plays the entry warble


# the instance of the TitleScreen class
title_screen = TitleScreen()


# the Hangsprite, or background sprite.
class HangSprite:
    def __init__(self):
        self.sheet = hangsprite_bigsheet  # the sprite sheet
        self.cell_w = 160                 # the width of a cell
        self.cell_h = 160                 # the height of a cell
        self.sheet_frames_x = 6           # frames across
        self.sheet_frames_y = 6           # frames tall

        # creates a tuple which represents the rect required to blit a portion of the
        # master sheet, for each frame of the animation, and stores them in an ordered list.
        self.frames = []
        for y in range(0, self.sheet_frames_y):
            for x in range(0, self.sheet_frames_x):
                # adds a rect tuple for each frame of the sheet
                self.frames.append((x * self.cell_w, y * self.cell_h, self.cell_w, self.cell_h))

        self.frame_counter = 0      # what frame the animation is currently "on"
        self.frame_max = 31         # max frame in the animation
        self.dt = 0                 # ms since last frame change

        # which phase the game is in. 0 = Fresh, 1 = 33% penalties, 2 = 66% penalties, 3 = game over
        self.animation_phase = 0


# the instance of the hangsprite class
bg_sprite = HangSprite()


# All the stuff for the hangman game, including surfaces and text
class Hangman:
    def __init__(self):
        self.word = None            # the currently active word
        self.display_word = ""      # the word which is displayed to the player
        self.word_dict = {}         # a dictionary of letters in the word, with asterisk values
        self.tried = []             # letters that have already been tried this turn
        self.revealed_dict = {}     # dict gets each letter in word and has boolean value "HIDE" which hides the letter
        self.category = None        # the current category
        self.penalties = 0          # current number of penalties
        self.streaking = False      # whether the player is currently on a streak
        self.total_streak = 0       # total number of words in streak so far
        self.score = 0              # score so far for this word (letters guessed correctly)
        self.req_score = 0          # score required to win
        self.over = False           # If there is a game over state

        # Several surfaces for the main game display and their locations:
        # penalty surface
        self.pen_surf = NORMAL_FONT.render("PENALTIES: " + str(self.penalties) + "/" + str(options.penalty_limit), False, WHITE)
        self.pen_loc = (SIZE[0] * .6, SIZE[1] * .85)

        # display word surface
        self.display_surf = SMALLER_FONT.render(self.display_word, False, WHITE)
        self.display_loc = (SIZE[0] * .1, SIZE[1] * .7)

        # prompt surface
        self.prompt_surf = NORMAL_FONT.render("Hit a letter key!", False, WHITE)
        self.prompt_loc = (SIZE[0] * .6, SIZE[1] * .55)

        # streak surface
        self.streak_surf = SMALLER_FONT.render("WORD STREAK: " + str(self.total_streak), False, WHITE)
        self.streak_loc = (SIZE[0] * .6, SIZE[1] * .62)

        # category surface
        self.cat_surf = SMALLER_FONT.render("FROM CATEGORY: " + str(self.category), False, WHITE)
        self.cat_loc = (SIZE[0] * .1, SIZE[1] * .85)

    # creates the dictionaries for managing the word and hiding it
    def create_display_word(self):
        self.word_dict = {str(k): "*" for k in self.word}
        self.revealed_dict = {str(k): "HIDE" for k in self.word_dict}

    # After every player input the display word has to be re-drawn
    def handle_display_word(self):
        a_word = [letter for letter in self.word]        # create an ordered list out of the word
        display_word = ""                                # create an empty string
        for char in a_word:                              # for each char in the list
            if self.revealed_dict[char] is "HIDE":       # if their value is "HIDE" in the revealed_dict
                display_word += "*"                      # add an asterisk to the display_word
            else:                                        # else
                display_word += str(char)                # add the letter itself to the display_word
        self.display_word = display_word                 # update the display_word

    # checks the corresponding key press
    def check_letter(self, letter):                      # takes a character
        if letter not in self.tried:                     # if not yet tried
            if letter in self.word_dict:                 # and if not in the word_dict
                self.revealed_dict[letter] = "FOUND"     # change its value in the revealed_dict to "FOUND"
                self.score += 1                          # add one to the score
                self.tried.append(letter)                # append the letter to the list of tried letters
            else:                                        # else
                self.penalties += 1                      # add one penalty
                self.tried.append(letter)                # add the letter to the list of tried letters


# the instance of the Hangman object
hangman = Hangman()


# FUNCTIONS

# The update function, which is a little bloated.
def update():
    # fill the surface
    MAIN_SURFACE.fill(BLACK)
    # if the menu state is "MAIN"
    if title_screen.menu_state is "MAIN":
        # blit the title animation
        MAIN_SURFACE.blit(title_screen.sheet, (0, 0), title_screen.frames[title_screen.frame_counter])
        # blit the menu buttons
        MAIN_SURFACE.blit(title_screen.new_game_text, title_screen.new_game_loc)
        MAIN_SURFACE.blit(title_screen.options_text, title_screen.options_loc)
        MAIN_SURFACE.blit(title_screen.quit_text, title_screen.quit_loc)
        # update animation timer
        if title_screen.frame_counter < title_screen.frame_max:   # if the current frame is less than the max frame
            if title_screen.dt > 250:                             # if it's been more than 250ms since the last change
                title_screen.frame_counter += 1                   # increase the frame counter to the next one
                title_screen.dt = 0                               # reset the title animation's delta time variable
    # else if the menu state is "OPTIONS"
    elif title_screen.menu_state is "OPTIONS":
        # blit the title animation
        MAIN_SURFACE.blit(title_screen.sheet, (0, 0), title_screen.frames[title_screen.frame_counter])
        # blit the menu buttons
        MAIN_SURFACE.blit(options.increase_text, options.increase_loc)
        MAIN_SURFACE.blit(options.decrease_text, options.decrease_loc)
        MAIN_SURFACE.blit(options.sound_text, options.sound_loc)
        MAIN_SURFACE.blit(options.back_text, options.back_loc)
        MAIN_SURFACE.blit(options.update_text, options.update_loc)
        # update animation timer
        if title_screen.frame_counter < title_screen.frame_max:   # if the current frame is less than the max frame
            if title_screen.dt > 250:                             # if it's been more than 250ms since the last chance
                title_screen.frame_counter += 1                   # increase the frame to the next one
                title_screen.dt = 0                               # reset the delta time variable
    # else if the menu state is "GAME"
    elif title_screen.menu_state is "GAME":
        # fill the background with the background color
        MAIN_SURFACE.fill(BG_COLOR)
        # fill the lower third
        FG_SURFACE.fill(FG_COLOR)
        # blit the lower third
        MAIN_SURFACE.blit(FG_SURFACE, FG_LOC)
        # blit the background sprite
        MAIN_SURFACE.blit(bg_sprite.sheet, (10, 10), bg_sprite.frames[bg_sprite.frame_counter])

        # control the animation speed of the background sprite through
        # the phases of the game
        if bg_sprite.dt > 500:                                              # if it's been more than 500ms
            if bg_sprite.animation_phase is 0:                              # if the animation phase is 0
                if bg_sprite.frame_counter < 16:                            # and the frame is less than 16
                    bg_sprite.frame_counter += 1                            # move to the next frame
                    bg_sprite.dt = 0                                        # reset the delta time variable
            elif bg_sprite.animation_phase is 1:                            # else if the animation is in phase 1
                if bg_sprite.frame_counter < 23:                            # and the frame is less than 23
                    bg_sprite.frame_counter += 1                            # move to the next frame
                    bg_sprite.dt = 0                                        # reset the delta time variable
                    if options.music_enabled is True:                       # if music is enabled
                        sound_rope_lower.play()                             # play the ropey sound effect
            elif bg_sprite.animation_phase is 2:                            # else if in phase 2
                if bg_sprite.frame_counter < 29:                            # if the frame is less than 29
                    bg_sprite.frame_counter += 1                            # move the frame to the next one
                    bg_sprite.dt = 0                                        # and reset the delta time variable
                    if options.music_enabled is True:                       # if music is enabled
                        sound_rope_lower.play()                             # play the ropey sound effect
            elif bg_sprite.animation_phase is 3:                            # else if in animation phase 3
                if bg_sprite.frame_counter < bg_sprite.frame_max:           # if frame count is less than max
                    bg_sprite.frame_counter += 1                            # move to the next frame
                    bg_sprite.dt = 0                                        # and reset the delta time variable
                    if bg_sprite.frame_counter == bg_sprite.frame_max - 1:  # if the frame counter is the 2nd to last
                        if options.music_enabled is True:                   # and if music is enabled
                            sound_horn.play()                               # play the trumpet effect
                    elif bg_sprite.frame_counter == bg_sprite.frame_max:    # else if it's the last frame
                        if options.music_enabled is True:                   # and music is enabled
                            sound_drop.play()                               # play the "CLUNK" sound effect

        # redraw the display word
        hangman.handle_display_word()

        # create the various surfaces
        hangman.pen_surf = NORMAL_FONT.render("PENALTIES: " + str(hangman.penalties) + "/" + str(options.penalty_limit), False, WHITE)
        hangman.display_surf = LARGER_FONT.render(hangman.display_word, False, WHITE)
        hangman.prompt_surf = NORMAL_FONT.render("Hit a letter key!", False, WHITE)
        hangman.streak_surf = SMALLER_FONT.render("WORD STREAK: " + str(hangman.total_streak), False, WHITE)
        hangman.cat_surf = SMALLER_FONT.render("FROM CATEGORY: " + str(hangman.category), False, WHITE)

        # and then blit those surfaces
        MAIN_SURFACE.blit(hangman.pen_surf, hangman.pen_loc)
        MAIN_SURFACE.blit(hangman.display_surf, hangman.display_loc)
        MAIN_SURFACE.blit(hangman.cat_surf, hangman.cat_loc)
        MAIN_SURFACE.blit(hangman.prompt_surf, hangman.prompt_loc)
        MAIN_SURFACE.blit(hangman.streak_surf, hangman.streak_loc)

        # if the game over state is true then
        # create a game over blurb and blit it
        # and let the player know what the word was
        if hangman.over is True:
            FG_SURFACE.fill(BLACK)
            MAIN_SURFACE.blit(FG_SURFACE, FG_LOC)
            blurb_text = None
            # apply the right value to the label depending
            # on whether it was a win or loss
            if hangman.penalties >= options.penalty_limit:
                blurb_text = "YOU LOSE, CLICK TO CONTINUE"
            elif hangman.score >= hangman.req_score:
                blurb_text = "YOU WIN, CLICK TO CONTINUE"
            # create the surfaces
            blurb_surf = LARGER_FONT.render(blurb_text, False, WHITE)
            word_hint = NORMAL_FONT.render("Word was: " + hangman.word, False, WHITE)
            # blit the surfaces
            MAIN_SURFACE.blit(blurb_surf, (0, SIZE[1] * .75))
            MAIN_SURFACE.blit(word_hint, (0, SIZE[1] * .85))


# A reset function
def reset():
    hangman.penalties = 0                           # resets the penalties
    hangman.score = 0                               # resets the score
    hangman.req_score = 0                           # resets the required score to win
    hangman.word = None                             # resets the word
    hangman.tried = []                              # resets the list of attempted letters
    hangman.word_dict = {}                          # reset the word_dict that holds the letters
    hangman.revealed_dict = {}                      # reset the revealed_dict that hides the letters
    VM.choose_word()                                # VocabManager picks a new word
    hangman.word = VM.chosen_word                   # word is applied to the hangman game
    hangman.category = VM.chosen_cat_name           # category is applied to the hangman game
    hangman.req_score = VM.calculate_score()        # calculate the required score for the next word
    hangman.create_display_word()                   # create dicts out of the new word
    bg_sprite.animation_phase = 0                   # reset the background sprite animation phase to 0
    bg_sprite.frame_counter = 0                     # reset the background sprite frame counter to 0


# a smaller reset function
def smaller_reset():
    hangman.penalties = 0
    hangman.score = 0
    hangman.req_score = 0
    hangman.word = None
    hangman.tried = []
    hangman.word_dict = {}
    hangman.revealed_dict = {}
    bg_sprite.animation_phase = 0
    bg_sprite.frame_counter = 0


# the main function
def main():

    # main loop
    stopped = False
    while not stopped:

        # check the event queue
        for event in pygame.event.get():

            # Quit checker
            if event.type is pygame.QUIT:
                stopped = True

            # If the event is a mouse button up
            if event.type is pygame.MOUSEBUTTONUP:

                # get the mouse position and check the hitboxes for the main menu
                if title_screen.menu_state is "MAIN":
                    mouse_pos = pygame.mouse.get_pos()
                    title_screen.main_hitboxes(mouse_pos[0], mouse_pos[1])

                # get the mouse position and check the hitboxes for the options menu
                elif title_screen.menu_state is "OPTIONS":
                    mouse_pos = pygame.mouse.get_pos()
                    options.options_hitboxes(mouse_pos[0], mouse_pos[1])

                # during game over state, reset the game on a click
                elif title_screen.menu_state is "GAME":
                    if hangman.over is True:                   # check for game over state
                        if hangman.streaking is True:          # if the player won
                            hangman.total_streak += 1          # add to the streak
                        elif hangman.streaking is False:       # if they lost
                            hangman.total_streak *= 0          # erase it
                        smaller_reset()                        # apply the small reset function
                        title_screen.menu_state = "MAIN"       # change the menu state to "MAIN"
                        hangman.over = False                   # remove the game over state

            # Check for key presses:
            if event.type is pygame.KEYUP:

                # if a game is currently active
                if title_screen.menu_state is "GAME":

                    # check each key with the check_letter() function
                    if title_screen.menu_state is "GAME":
                        if event.key is pygame.K_a:
                            hangman.check_letter("A")
                        elif event.key is pygame.K_b:
                            hangman.check_letter("B")
                        elif event.key is pygame.K_c:
                            hangman.check_letter("C")
                        elif event.key is pygame.K_d:
                            hangman.check_letter("D")
                        elif event.key is pygame.K_e:
                            hangman.check_letter("E")
                        elif event.key is pygame.K_f:
                            hangman.check_letter("F")
                        elif event.key is pygame.K_g:
                            hangman.check_letter("G")
                        elif event.key is pygame.K_h:
                            hangman.check_letter("H")
                        elif event.key is pygame.K_i:
                            hangman.check_letter("I")
                        elif event.key is pygame.K_j:
                            hangman.check_letter("J")
                        elif event.key is pygame.K_k:
                            hangman.check_letter("K")
                        elif event.key is pygame.K_l:
                            hangman.check_letter("L")
                        elif event.key is pygame.K_m:
                            hangman.check_letter("M")
                        elif event.key is pygame.K_n:
                            hangman.check_letter("N")
                        elif event.key is pygame.K_o:
                            hangman.check_letter("O")
                        elif event.key is pygame.K_p:
                            hangman.check_letter("P")
                        elif event.key is pygame.K_q:
                            hangman.check_letter("Q")
                        elif event.key is pygame.K_r:
                            hangman.check_letter("R")
                        elif event.key is pygame.K_s:
                            hangman.check_letter("S")
                        elif event.key is pygame.K_t:
                            hangman.check_letter("T")
                        elif event.key is pygame.K_u:
                            hangman.check_letter("U")
                        elif event.key is pygame.K_v:
                            hangman.check_letter("V")
                        elif event.key is pygame.K_w:
                            hangman.check_letter("W")
                        elif event.key is pygame.K_x:
                            hangman.check_letter("X")
                        elif event.key is pygame.K_y:
                            hangman.check_letter("Y")
                        elif event.key is pygame.K_z:
                            hangman.check_letter("Z")

        # Quit if the player hits the quit option in the menu
        if title_screen.menu_state is "QUIT":
            stopped = True

        # if the player is in game and has won
        # then flag as streaking and enable the game over state
        if title_screen.menu_state is "GAME":
            if hangman.score >= hangman.req_score:
                hangman.streaking = True
                hangman.over = True

        # During the game, checks every frame to see if the penalty limit has
        # gone beyond the threshold for the next animation phase
        if title_screen.menu_state is "GAME":
            if hangman.penalties >= options.penalty_limit * .33 and hangman.penalties < options.penalty_limit * .66:
                bg_sprite.animation_phase = 1
            elif hangman.penalties >= options.penalty_limit * .66 and hangman.penalties < options.penalty_limit:
                bg_sprite.animation_phase = 2

            # if penalty limit reached then end the player's streak, finish the
            # animation, and enable game over state
            elif hangman.penalties >= options.penalty_limit:
                bg_sprite.animation_phase = 3
                # erase streak
                hangman.streaking = False
                # end game state
                hangman.over = True

        # draw the background with the update() function
        update()

        # Update the display
        pygame.display.flip()

        # pump the queue
        pygame.event.pump()

        # Framerate stuff
        dt = GAME_CLOCK.tick(FPS)  # set the delta time variable and the framerate
        title_screen.dt += dt  # add the delta time to the title animation's delta time
        bg_sprite.dt += dt  # add the delta time to the background sprite's delta time

    # Quit the program if the user exits
    pygame.quit()


# start point
if __name__ == "__main__":
    main()



