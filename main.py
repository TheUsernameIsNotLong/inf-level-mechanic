from character import *
from battle import *
from attack import *

while True:
    playerName = input("Please enter your name: ")
    if (len(playerName) >= 1) and (len(playerName) <= 20): #20 characters may seem specific but its to allow awesome names such as "TheUsernameIsNotLong"
        break
    else:
        print("Your name should be between 1 and 20 letters long!") 

# while True:
#     try:
#         startLvl = int(input("Please enter the level to start at: "))
#         if startLvl >= 1:
#             break
#         else:
#             print("Please enter a positive number!")
#     except:
#         print("Please enter a positive number!")
startLvl = 10000

player = Character(playerName, Stats(startLvl,0,0,0,0,0,0,0,0), True)
enemy = Character("Enemy", Stats(startLvl,0,0,0,0,0,0,0,0), False)
player.knownSkills.append(atkDefault)
player.knownSkills.append(atkPsnSlash)
player.knownSkills.append(atkToxSpore)
enemy.knownSkills.append(atkDefault)
player.printStats()
# player.removeStatus(Poison(1))

while True:
    Battle(player, enemy)
    enemy.stats.hp = enemy.stats.maxhp
    player.stats.hp = player.stats.maxhp
    enemy.stats.lvl = player.stats.lvl
    enemy.stats.setStats()

# while True:
#     player.printStats()
#     exp = int(input("Exp to add: "))
#     player.stats.addExp(exp)