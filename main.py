from character import *
from battle import *
from attack import *
from modifier import *

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
startLvl = 5000

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
# player.printStats()

field = [enemy]

def groupModifiers(modifierList):
    groupedModifiers = []
    for modifier in modifierList:
        if isinstance(modifier, Modifier_Standard):
            if modifier not in groupedModifiers:
                groupedModifiers.append(modifier)
            else:
                groupedModifierIndex = groupedModifiers.index(modifier)
                groupedModifiers[groupedModifierIndex].rank += 1
    return groupedModifiers

def decideModifiers(char:Character):
    rankReset()
    selecting = True
    while selecting:
        if char.stats.lvl < 10:
            chance = 0
        else:
            chance = (1-((10*(1+len(char.modifiers))**2)/char.stats.lvl))**2
        if random.random() <= chance:
            modifier = random.choices(availableModifiers, [modifier.rarity for modifier in availableModifiers])[0]
            char.modifiers.append(modifier)
            char.stats.remLvl(5)
        else:
            selecting = False
    groupedModifiers = groupModifiers(char.modifiers)
    for modifier in groupedModifiers:
        modifier.apply(char)
    print([modifier.name for modifier in char.modifiers])
    char.name = " ".join([*[f"<{modifier.name} {modifier.rank}>" for modifier in groupedModifiers],char.name])
    

def findEnemy():
    enemy = random.choice(field)
    decideModifiers(enemy)
    return enemy

while True:
    Battle(player, findEnemy())
    enemy.stats.hp = enemy.stats.maxhp
    player.stats.hp = player.stats.maxhp
    enemy.stats.lvl = determineEnemyLvl()
    enemy.modifiers.clear()
    enemy.name = "Enemy"
    enemy.stats.setStats()

# while True:
#     player.printStats()
#     exp = int(input("Exp to add: "))
#     player.stats.addExp(exp)