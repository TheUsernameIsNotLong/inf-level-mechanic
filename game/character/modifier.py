from game.character.character import Character
from math import ceil
import random

class Modifier_Standard:
    
    def __init__(self, name:str, rarity:float, rank:int=1, hp:int=1, atk:int=0, dfc:int=0, mAtk:int=0, mDfc:int=0, spd:int=0):
        
        self.name = name
        self.rarity = rarity # Weight for each modifier (Greater the number, more common the modifier is)
        self.rank = rank # Begins at rank 1, but increases when grouped with similar modifiers
        self.hp = hp
        self.atk = atk
        self.dfc = dfc
        self.mAtk = mAtk
        self.mDfc = mDfc
        self.spd = spd
    
    def apply(self, char:Character):
        
        # 10% hp increase is represented as 1.1, so if rank were 2, it multiplies by 0.1 to produce a 1.2x increase to hp
        char.stats.maxhp = ceil(char.stats.maxhp * (1+(self.rank*(self.hp-1))))
        char.stats.hp = char.stats.maxhp
        char.stats.atk += self.rank*self.atk
        char.stats.dfc += self.rank*self.dfc
        char.stats.mAtk += self.rank*self.mAtk
        char.stats.mDfc += self.rank*self.mDfc
        char.stats.spd += self.rank*self.spd

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

md_healthy = Modifier_Standard("Healthy", 20, hp=1.1)
md_speedy = Modifier_Standard("Speedy", 20, spd=25)
md_enduring = Modifier_Standard("Enduring", 20, dfc=40)
md_sharp = Modifier_Standard("Sharp", 20, atk=55)
md_magical = Modifier_Standard("Magical", 20, mAtk=55)
md_wise = Modifier_Standard("Magical", 20, mDfc=40)
md_mystical = Modifier_Standard("Mystical", 10, mAtk=45, mDfc=30)
md_murderous = Modifier_Standard("Murderous", 10, atk=85)
md_tanky = Modifier_Standard("Tanky", 10, dfc=70, mDfc=30, spd=-10)
md_dangerous = Modifier_Standard("Dangerous", 0, hp=1e-9, atk=9e9, dfc=9e9, mAtk=9e9, mDfc=9e9, spd=9e9)

availableModifiers = [md_healthy,
                      md_speedy,
                      md_enduring,
                      md_sharp,
                      md_magical,
                      md_wise,
                      md_mystical,
                      md_murderous,
                      md_tanky,
                      md_dangerous]

def rankReset():
    for modifier in availableModifiers:
        modifier.rank = 1
        
# Modifiers may soon use the copy module to prevent modifying the original instances' ranks, like the attacks in attack.py