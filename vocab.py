"""
Sam Gibson
23 AUG

The vocab manager for the main.py file for Graphical Hangman v1

"""
import random


# THE RAW CATEGORIES
cat_animals = ["cat", "bat", "dog", "bear", "whale", "lion", "pig", "goat", "cow", "snake"]
cat_food = ["apple", "banana", "pear", "pizza", "pie", "beef", "taco", "cheese", "carrot", "peanut"]
cat_geography = ["mountain", "lake", "ocean", "hill", "valley", "cliff", "bay", "peninsula", "range", "plains"]
cat_military = ["tank", "jet", "nuke", "rank", "war", "sergeant", "trench", "rifle", "uniform", "orders"]
cat_space = ["star", "planet", "moon", "vacuum", "meteor", "comet", "asteroid", "gravity", "mars", "jupiter"]
cat_nature = ["tree", "breeze", "desert", "plains", "bugs", "sky", "clouds", "river", "forest", "beach"]
cat_vehicles = ["car", "bus", "truck", "plane", "train", "boat", "blimp", "bike", "wagon", "horse"]
cat_music = ["rock", "country", "rap", "fuzz", "metal", "folk", "riff", "chord", "scale", "octave"]
cat_instruments = ["tuba", "guitar", "bass", "harmonica", "violin", "cello", "piano", "drums", "trombone", "saxophone"]
cat_household = ["phone", "kitchen", "closet", "room", "curtains", "carpet", "attic", "basement", "garage", "driveway"]
cat_history = ["medieval", "renaissance", "ancient", "prehistoric", "archaeology", "ruins"]
cat_technology = ["phone", "circuit", "wire", "transistor", "gate", "miniaturization", "electromagnetic", "signal",
                  "antenna", "display"]
cat_politics = ["democrat", "republican", "libertarian", "communism", "capitalism", "socialism", "fascism", "vote",
                "coup", "election"]
cat_fantasy = ["dragon", "princess", "sword", "magic", "dungeon", "goblin", "elf", "orc", "hobbit", "unicorn"]
cat_gaming = ["role", "shooter", "strategy", "simulation", "sandbox", "jrpg", "tactical", "steam", "twitch", "indie"]
cat_school = ["pencil", "paper", "textbook", "teacher", "lunch", "locker", "backpack", "grades", "finals", "graduation"]
cat_internet = ["wifi", "broadband", "network", "gateway", "router", "provider", "neutrality", "piracy", "facebook",
                "reddit"]
cat_parties = ["drunk", "wasted", "dancing", "barfing", "social", "music", "guests", "surprise", "frat", "sorority"]
cat_math = ["division", "subtraction", "addition", "multiplication", "fraction", "decimal", "algebra", "calculus",
            "equation", "proof"]
cat_challenge = ["discomforting", "stargazing", "revolutionary", "discombobulated", "superconducting",
                 "superconductor", "microprocessor", "parliamentarian"]
cat_colors = ["YELLOW", "RED", "BLUE", "GREEN", "WHITE", "BLACK", "BROWN", "GRAY", "GREY", "PURPLE"]
cat_noises = ["CRY", "LAUGH", "COUGH", "BANG", "CRASH", "CRACK", "SHOUT", "WHISPER", "GIGGLE", "GROAN"]
cat_cities = ["PORTLAND", "SEATTLE", "CHICAGO", "LONDON", "LOUISVILLE", "CANBERRA", "PRAGUE", "SANTIAGO", "MOGADISHU",
              "CAIRO", "PARIS", "MOSCOW", "CALCUTTA", "SHANGHAI", "SEOUL"]
cat_shapes = ["SQUARE", "RECTANGLE", "RHOMBOID", "TRIANGLE", "PYRAMID", "PARALLELOGRAM", "SPHERE", "CYLINDER", "CONE",
              "CONVEX"]
cat_numbers = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "ELEVEN", "TWELVE",
               "THIRTEEN"]
cat_drinks = ["WATER", "BEER", "SODA", "POP", "ALE", "JUICE", "ENERGY", "COFFEE", "WINE", "MILK"]
cat_languages = ["SIGN", "ENGLISH", "SPANISH", "ARABIC", "MANDARIN", "JAPANESE", "HINDI", "RUSSIAN", "FRENCH", "DUTCH",
                 "SWAHILI", "GERMAN", "SWEDISH", "ITALIAN", "DANISH", "LITHUANIAN", "CANTONESE", "PORTUGUESE"]
cat_entertainment = ["television", "radio", "streaming", "netflix", "hulu", "comedy", "play", "theater", "sports",
                     "music", "poetry", "park"]
cat_art = ["painting", "singing", "sculpture", "sketch", "draw", "paint", "palette", "photography", "design",
           "portrait"]

# cat_authors = ["DICKENS", "HERBERT", "HEINLEIN", "TWAIN", "DELANEY"]  # I'll save this for two word functionality


# CATEGORY MASTER LIST
category_list = []


class Category:
    def __init__(self, cat_list, name):
        self.word_list = cat_list
        self.name = name
        category_list.append(self)


art = Category(cat_art, "ART")

entertainment = Category(cat_entertainment, "ENTERTAINMENT")

colors = Category(cat_colors, "COLORS")

languages = Category(cat_languages, "LANGUAGES")

drinks = Category(cat_drinks, "DRINKS")

numbers = Category(cat_numbers, "NUMBERS")

shapes = Category(cat_shapes, "SHAPES")

cities = Category(cat_cities, "CITIES")

noises = Category(cat_noises, "NOISES")

animals = Category(cat_animals, "ANIMALS")

food = Category(cat_food, "FOOD")

geography = Category(cat_geography, "GEOGRAPHY")

military = Category(cat_military, "MILITARY")

space = Category(cat_space, "SPACE")

nature = Category(cat_nature, "NATURE")

vehicles = Category(cat_vehicles, "VEHICLES")

music = Category(cat_music, "MUSIC")

instruments = Category(cat_instruments, "INSTRUMENTS")

household = Category(cat_household, "HOUSEHOLD")

history = Category(cat_history, "HISTORY")

technology = Category(cat_technology, "TECHNOLOGY")

politics = Category(cat_politics, "POLITICS")

fantasy = Category(cat_fantasy, "FANTASY")

gaming = Category(cat_gaming, "GAMING")

school = Category(cat_school, "SCHOOL")

internet = Category(cat_internet, "INTERNET")

parties = Category(cat_parties, "PARTIES")

math = Category(cat_math, "MATH")

challenge = Category(cat_challenge, "CHALLENGE")


class VocabManager:
    def __init__(self):
        self.categories = category_list
        self.chosen_cat = None
        self.chosen_cat_name = None
        self.chosen_word = None

    def choose_word(self):
        self.chosen_cat = random.choice(self.categories)
        self.chosen_cat_name = self.chosen_cat.name
        self.chosen_word = random.choice(self.chosen_cat.word_list).upper()

    def calculate_score(self):

        points = 0

        a_dict = {str(k): "Nada" for k in self.chosen_word}

        for keys in a_dict:
            points += 1

        return points




