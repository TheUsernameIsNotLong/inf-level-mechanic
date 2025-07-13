""" 
Modules imported:
- math: For mathematical operations.
- random: For random number generation (modifier selection).
- game.character.character: For character management.
"""

from math import ceil
import random
from game.character.character import Character

class ModifierStandard:
    """Class representing a standard modifier that can be applied to characters."""
    def __init__(self, name:str, rarity:float, rank:int=1, hp:int=1, atk:int=0, dfc:int=0, m_atk:int=0, m_dfc:int=0, spd:int=0):

        self.name = name
        self.rarity = rarity # Weight for each modifier (Greater the number, more common the modifier is)
        self.rank = rank # Begins at rank 1, but increases when grouped with similar modifiers
        self.hp = hp
        self.atk = atk
        self.dfc = dfc
        self.m_atk = m_atk
        self.m_dfc = m_dfc
        self.spd = spd

    def apply(self, char:Character):
        """Apply the modifier's effects to the character's stats."""
        # 10% hp increase is represented as 1.1, so if rank were 2, it multiplies by 0.1 to produce a 1.2x increase to hp
        char.stats.maxhp = ceil(char.stats.maxhp * (1+(self.rank*(self.hp-1))))
        char.stats.hp = char.stats.maxhp
        char.stats.atk += self.rank*self.atk
        char.stats.dfc += self.rank*self.dfc
        char.stats.mAtk += self.rank*self.m_atk
        char.stats.mDfc += self.rank*self.m_dfc
        char.stats.spd += self.rank*self.spd

def group_modifiers(modifier_list):
    """Group modifiers of the same type and increase their rank."""
    grouped_modifiers = []
    for modifier in modifier_list:
        if isinstance(modifier, ModifierStandard):
            if modifier not in grouped_modifiers:
                grouped_modifiers.append(modifier)
            else:
                grouped_modifier_index = grouped_modifiers.index(modifier)
                grouped_modifiers[grouped_modifier_index].rank += 1
    return grouped_modifiers

def decide_modifiers(char:Character):
    """Decide which modifiers to apply to the character based on their level and existing modifiers."""
    rank_reset()
    selecting = True
    while selecting:
        if char.stats.lvl < 10:
            chance = 0
        else:
            chance = (1-((10*(1+len(char.modifiers))**2)/char.stats.lvl))**2
        if random.random() <= chance:
            modifier = random.choices(available_modifiers, [modifier.rarity for modifier in available_modifiers])[0]
            char.modifiers.append(modifier)
            char.stats.remLvl(5)
        else:
            selecting = False
    grouped_modifiers = group_modifiers(char.modifiers)
    for modifier in grouped_modifiers:
        modifier.apply(char)
    print([modifier.name for modifier in char.modifiers])
    char.name = " ".join([*[f"<{modifier.name} {modifier.rank}>" for modifier in grouped_modifiers],char.name])

md_healthy = ModifierStandard("Healthy", 20, hp=1.1)
md_speedy = ModifierStandard("Speedy", 20, spd=25)
md_enduring = ModifierStandard("Enduring", 20, dfc=40)
md_sharp = ModifierStandard("Sharp", 20, atk=55)
md_magical = ModifierStandard("Magical", 20, m_atk=55)
md_wise = ModifierStandard("Magical", 20, m_dfc=40)
md_mystical = ModifierStandard("Mystical", 10, m_atk=45, m_dfc=30)
md_murderous = ModifierStandard("Murderous", 10, atk=85)
md_tanky = ModifierStandard("Tanky", 10, dfc=70, m_dfc=30, spd=-10)
md_dangerous = ModifierStandard("Dangerous", 0, hp=1e-9, atk=9e9, dfc=9e9, m_atk=9e9, m_dfc=9e9, spd=9e9)

available_modifiers = [md_healthy,
                      md_speedy,
                      md_enduring,
                      md_sharp,
                      md_magical,
                      md_wise,
                      md_mystical,
                      md_murderous,
                      md_tanky,
                      md_dangerous]

def rank_reset():
    """Reset the rank of all available modifiers to 1."""
    for modifier in available_modifiers:
        modifier.rank = 1

# Modifiers may soon use the copy module to prevent modifying the original instances' ranks, like the attacks in attack.py
