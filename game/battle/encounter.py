import configparser
import copy
import random
from ..character.character import *
from ..character.modifier import *
from ..core.mechanics import * 
import game.core.data as data


# Prepare config file
config = configparser.ConfigParser()
config.read('config.ini')

# Deciding enemy level based on player's current level - this will eventually be changed to a "team rating" system to work with multiple enemies and party members
def determineEnemyLvl():
    player = data.party[0]
    pLvl = player.stats.lvl
    return random.randint(round(pLvl-(pLvl**0.5)), round(pLvl+(pLvl**0.5)))

# List of all possible encounters, this would be dependent on the player's level and area on the map, should there eventually be one
field = []

# Function for determining which enemy to encounter
def findEnemy():
    enemy = copy.deepcopy(random.choice(field))
    enemy.stats.lvl = determineEnemyLvl()
    if config['options_game']['modifiersEnabled'] == "true":
        decideModifiers(enemy)
    enemy.stats.setStats()
    return enemy