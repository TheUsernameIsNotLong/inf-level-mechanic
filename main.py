import configparser
import copy
import game.core.data as data
from game.character.character import *
from game.battle.battle import *
from game.battle.attack import *
from game.character.modifier import *

# Prepare config file
config = configparser.ConfigParser()
config.read('config.ini')

# Setting player name
while True:
    playerName = input("Please enter your name: ")
    if (len(playerName) >= 1) and (len(playerName) <= 20): #20 characters may seem specific but its to allow awesome names such as "TheUsernameIsNotLong"
        break
    else:
        print("Your name should be between 1 and 20 letters long!") 

# Level the player starts at
startLvl = 50 # This will change a lot through commits since I playtest with different levels

# Deciding enemy level based on player's current level
def determineEnemyLvl():
    pLvl = player.stats.lvl
    return random.randint(round(pLvl-(pLvl**0.5)), round(pLvl+(pLvl**0.5)))

# Defining player & enemy characters
player = Character(playerName, Stats(startLvl, profStandard), True)
enemy = Character("Enemy", Stats(1, profStandard), False)

data.party.append(player)

# List of all possible encounters, this would be dependent on the player's level and area on the map, should there eventually be one
field = [enemy]

# Function for determining which enemy to encounter
def findEnemy():
    enemy = copy.deepcopy(random.choice(field))
    enemy.stats.lvl = determineEnemyLvl()
    if config['options_game']['modifiersEnabled'] == "true":
        decideModifiers(enemy)
    enemy.stats.setStats()
    return enemy

# Looping battle (for testing)
while True:
    party = data.party
    enemies = [findEnemy()]
    Battle(party, enemies)
    for member in party+enemies:
        member.stats.hp = member.stats.maxhp
    if config['options_game']['modifiersEnabled'] == "true":
        enemy.modifiers.clear()
        enemy.name = "Enemy"
    enemy.stats.setStats()