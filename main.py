""" 
Modules imported:
- configparser: For configuration file handling.
- game.core.data: For core game data management.
- game.battle.encounter: For enemy encounter logic.
- game.battle.battle: For battle flow and control.
- game.battle.attack: For managing attacks and abilities.
"""

import configparser
import game.core.data as data
from game.battle.encounter import *
from game.battle.battle import *
from game.battle.attack import *

# Prepare config file
config = configparser.ConfigParser()
config.read('config.ini')

# Setting player name
while True:
    playerName = input("Please enter your name: ")
    if (len(playerName) >= 1) and (len(playerName) <= 20):
        break
    else:
        print("Your name should be between 1 and 20 letters long!")

# Level the player starts at
START_LVL = 50 # This will change a lot through commits since I playtest with different levels

# Defining player & enemy characters
player = Character(playerName, Stats(START_LVL, profStandard), True)
enemy = Character("Enemy", Stats(1, profStandard), False)

data.party.append(player)
field.append(enemy)

# Looping battle (for testing)
while True:
    party = data.party
    enemies = [find_enemy()]
    Battle(party, enemies)
    for member in party+enemies:
        member.stats.hp = member.stats.maxhp
    if config['options_game']['modifiersEnabled'] == "true":
        enemy.modifiers.clear()
        enemy.name = "Enemy"
    enemy.stats.set_stats()
