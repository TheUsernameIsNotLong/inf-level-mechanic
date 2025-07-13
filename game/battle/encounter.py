""" 
Modules imported:
- configparser: For reading configuration files.
- copy: For creating deep copies of objects.
- random: For generating random numbers.
- game.character.character: Contains definitions for character attributes and methods.
- game.character.modifier: Contains definitions for character modifiers.
- game.core.mechanics: Contains functions for game mechanics.
- game.core.data: Contains game data such as party members and enemy definitions.
"""

import configparser
import copy
import random
from game.character.character import *
from game.character.modifier import *
from game.core.mechanics import * 
import game.core.data as data


# Prepare config file
config = configparser.ConfigParser()
config.read('config.ini')

# Deciding enemy level based on player's current level - this will eventually be changed to a "team rating" system to work with multiple enemies and party members
def determine_enemy_lvl():
    """Determines the level of the enemy based on the player's level."""
    player = data.party[0]
    p_lvl = player.stats.lvl
    return random.randint(round(p_lvl-(p_lvl**0.5)), round(p_lvl+(p_lvl**0.5)))

# List of all possible encounters, this would be dependent on the player's level and area on the map, should there eventually be one
field = []

# Function for determining which enemy to encounter
def find_enemy():
    """Selects a random enemy from the field."""
    enemy = copy.deepcopy(random.choice(field))
    enemy.stats.lvl = determine_enemy_lvl()
    if config['options_game']['modifiersEnabled'] == "true":
        decide_modifiers(enemy)
    enemy.stats.set_stats()
    return enemy
