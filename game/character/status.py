""" 
Modules imported:
- random: For random number generation.
- math: For mathematical operations.
- game.core.display: For displaying battle information.
"""

import random
from math import floor
from game.core.display import scr_turn

class Status:
    """Base class for all status effects."""
    def __init__(self, tag:str, name:str, desc:str):
        self.tag = tag
        self.name = name
        self.desc = desc

    def apply(self):
        """Method to apply the status effect. Should be overridden in subclasses."""
        pass

class StatusSpecial(Status):
    """Base class for special status effects that do not require a level."""
    def __init__(self, tag:str, name:str, desc:str):
        super().__init__(tag, name, desc)

    def apply(self, char):
        """Method to apply the special status effect. Should be overridden in subclasses."""
        pass

class StatusDamage(Status):
    """Base class for status effects that deal damage over time."""
    def __init__(self, tag:str, name:str, desc:str, lvl:float, duration:int, stackable:bool):
        super().__init__(tag, name, desc)
        self.lvl = lvl
        self.duration = duration
        self.stackable = stackable

    def lvl_round(self):
        """Rounds the level to the nearest integer based on a random chance."""
        lvl_lower = int(self.lvl)
        lvl_part = self.lvl - lvl_lower
        if random.random() > lvl_part:
            self.lvl = lvl_lower
        else:
            self.lvl = lvl_lower + 1

    def print_damage(self, char, damage):
        """Prints the damage taken by the character."""
        battle = char.battle
        if battle is not None:
            scr_turn(battle.turn_num, battle.party, battle.enemies)
        print(f"{char.name} took {damage} {self.name} damage!")
        input()

    def apply(self, char):
        if not self.lvl.is_integer():
            self.lvl_round()

class StatusState(Status):
    """Base class for status effects that affect character states."""
    def __init__(self, tag:str, name:str, desc:str, duration:int):
        super().__init__(tag, name, desc)
        self.duration = duration

class KO(StatusSpecial):
    """Status effect for when a character is knocked out."""
    def __init__(self):
        super().__init__("KO", "Knocked Out", "No health remaining.")

    def apply(self, char):
        print(f"{char.name} has been knocked out!")
        char.canHeal = False

class Poison(StatusDamage):
    """Status effect for poison, dealing damage over time."""
    def __init__(self, lvl:float=1, duration:int=4):
        super().__init__("PSN", "Poison", "Take reccuring damage.", lvl, duration, True)

    def apply(self, char):
        super().apply(char)
        damage = floor(char.stats.hp*(1-(1-0.05)**self.lvl))
        char.harm(damage)
        self.print_damage(char, damage)

class Burn(StatusDamage):
    """Status effect for burn, dealing flat damage over time."""
    def __init__(self, lvl:float=1):
        super().__init__("BRN", "Burn", "Take reccuring flat damage.", lvl, 1, False)
        self.duration += self.lvl

    def apply(self, char):
        super().apply(char)
        damage = floor(char.stats.maxhp*0.08)
        char.harm(damage)
        self.print_damage(char, damage)

class Radiation(StatusDamage):
    """Status effect for radiation, dealing damage based on current health."""
    def __init__(self, lvl:float=1):
        super().__init__("RAD", "Radiation", "Take reccuring damage.", lvl, 5, True)

    def apply(self, char):
        super().apply(char)
        damage = floor(self.lvl * 0.125 * char.stats.hp)
        char.harm(damage)
        self.print_damage(char, damage)
        self.lvl /= 2

class Paralysis(StatusState):
    """Status effect for paralysis, preventing physical attacks."""
    def __init__(self, duration:int=3):
        super().__init__("PAR", "Paralysed", "Unable to use physical attacks.", duration)

    def apply(self):
        print("Paralysed!")

class Silence(StatusState):
    """Status effect for silence, preventing magic attacks."""
    def __init__(self, duration:int=2):
        super().__init__("SIL", "Silenced", "Unable to use magic attacks.", duration)

    def apply(self):
        print("Silenced!")

class Lock(StatusState):
    """Status effect for lock, preventing any movement."""
    def __init__(self, duration:int=2):
        super().__init__("LOK", "Locked", "Unable to move.", duration)

    def apply(self):
        print("Locked!")

availableStates = {
    "KO": KO,
    "PSN": Poison,
    "BRN": Burn,
    "RAD": Radiation,
    "PAR": Paralysis,
    "SIL": Silence,
    "LOK": Lock
}
