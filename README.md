# graphical_hangman_pygame

GRAPHICAL HANGMAN v1

23 AUG 2018

Finished v1, which means it is no longer tantalizing the player with menu options that don't work. The options menu is fully functional
and all of the menus are now clickable. 

I chose not to do a high score system this time, but there is a win streak counter. It will keep track of your win streak
until you lose, at which point it is reset.

Graphics and Sound are still very basic and there's definitely a better way to do the background sprite but I went
with what I was comfortable with for this version. Sprites were made with GIMP and Piskel, sound was made with bfxr and Bosca Ceoil.

I re-wrote the game loop and organized the classes differently than in v0, and while they are still probably not
ideal they are a lot better than before. I'm still working on modular organization but this one doesn't have as much
spaghetti as I feared it would. Still has a lot though. The update function is monstrous.

An area in need of improvement is the way I handled the background sprite. I could not get pygame.transform() to do
what I wanted with scaling, so I had to re-size the spritesheet manually and just use it that way. The animation is definitely a work
in progress. They definitely need work, and should probably be moved to the built in sprite classes.

This project needs to be refactored very badly, and it couldn't hurt to improve the art and sound, but other than that the
little game is "feature complete"
