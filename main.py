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
startLvl = 50

def determineEnemyLvl():
    pLvl = player.stats.lvl
    return random.randint(round(pLvl-(pLvl**0.5)), round(pLvl+(pLvl**0.5)))
    
    # if pLvl < 20:
    #     return random.randint(round(pLvl*0.8), round(pLvl*1.2))
    # elif (pLvl >= 20) and (pLvl < 40):
    #     return random.randint(pLvl - 4, pLvl + 4)
    # elif (pLvl >= 40) and (pLvl < 100):
    #     return random.randint(round(pLvl*0.9), round(pLvl*1.1))
    # else:
    #     return random.randint(pLvl - 10, pLvl + 10)

profStandard = Proficiency(0,0,0,0,0,0)
profOP = Proficiency(3,3,3,3,3,3)
profWK = Proficiency(-3,-3,-3,-3,-3,-3)

profTank = Proficiency(1,-1,3,-2,2,-3)
profJuggernaut = Proficiency(3,1,1,-2,1,-2)

player = Character(playerName, Stats(startLvl, profStandard), True)
enemy = Character("Enemy", Stats(determineEnemyLvl(), profStandard), False)
player.knownSkills.append(atkDefault)
player.knownSkills.append(atkPsnSlash)
player.knownSkills.append(atkToxSpore)
player.knownSkills.append(atkBurnBlade)
player.knownSkills.append(atkFlamethrower)
enemy.knownSkills.append(atkDefault)
player.printStats()

while True:
    Battle(player, enemy)
    enemy.stats.hp = enemy.stats.maxhp
    player.stats.hp = player.stats.maxhp
    enemy.stats.lvl = determineEnemyLvl()
    enemy.stats.setStats()

# while True:
#     player.printStats()
#     exp = int(input("Exp to add: "))
#     player.stats.addExp(exp)