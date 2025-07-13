""" 
Modules imported:
- math: For advanced mathematical calculations.
- game.character.proficiency: For character proficiency management.
"""

import math
from game.character.proficiency import *

class Stats:
    """Class representing character stats, including level, proficiency, and various attributes."""

    def __init__(self, lvl:int, prof, char=None):
        self.lvl = lvl
        self.prof = prof
        self.char = char # Changes if connected to a character class instance
        self.exp = 0
        self.maxhp = 0
        self.hp = 0
        self.maxmp = 0
        self.mp = 0
        self.atk = 0
        self.dfc = 0
        self.m_atk = 0
        self.m_dfc = 0
        self.spd = 0
        self.set_stats()

    def calc_lvl(self, exp):
        """Calculate the level based on experience points."""
        return math.floor((exp/100)**(1/2))

    def calc_exp_total(self, lvl):
        """Calculate the total experience points required to reach a certain level."""
        return 100 * lvl**2

    def calc_exp_goal(self, lvl):
        """Calculate the experience points required to reach the next level."""
        return (100 * lvl**2) - (100 * (lvl-1)**2)

    def calc_hp(self, lvl):
        """Calculate the maximum health points based on level and proficiency."""
        p_value = (20+self.prof.hp)/20
        return round((75 + ((lvl**3 * 5)**0.5))**p_value)

    def calc_mp(self, lvl):
        """Calculate the maximum magic points based on level and proficiency."""
        p_value = (20+self.prof.mp)/20
        return round((2*lvl)**p_value)

    def calc_atk(self, lvl):
        """Calculate the attack power based on level and proficiency."""
        p_value = (20+self.prof.atk)/20
        return round((20 + (4 * lvl))**p_value)

    def calc_dfc(self, lvl):
        """Calculate the defense power based on level and proficiency."""
        p_value = (20+self.prof.dfc)/20
        return round((15 + (3 * lvl))**p_value)

    def calc_spd(self, lvl):
        """Calculate the speed based on level and proficiency."""
        p_value = (20+self.prof.spd)/20
        return round((10 + (2 * lvl))**p_value)

    def set_stats(self):
        """Set the stats based on the current level and proficiency."""
        self.maxhp = self.calc_hp(self.lvl)
        self.hp = self.maxhp
        self.maxmp = self.calc_mp(self.lvl)
        self.mp = self.maxmp
        self.atk = self.calc_atk(self.lvl)
        self.dfc = self.calc_dfc(self.lvl)
        self.m_atk = self.calc_atk(self.lvl)
        self.m_dfc = self.calc_dfc(self.lvl)
        self.spd = self.calc_spd(self.lvl)

    def add_exp(self, exp):
        """Add experience points and handle level-ups."""
        self.exp += exp
        while self.exp >= self.calc_exp_goal(self.lvl):
            self.exp -= self.calc_exp_goal(self.lvl)
            self.lvl += 1
            print(f"You leveled up to Lvl. {self.lvl}!")
            self.learn_lvl_skills()
        self.set_stats()

    def learn_lvl_skills(self):
        """Check if the character learns any skills at the current level."""
        skill = self.char.lvl_skills.get(self.lvl)
        if skill is not None:
            self.char.add_skill(skill)

    def add_lvl(self, lvl):
        """Add levels and adjust experience points accordingly."""
        exp = self.calc_exp_total(lvl + self.lvl) - self.calc_exp_total(self.lvl)
        self.add_exp(exp)

    def rem_lvl(self, lvl):
        """Remove levels and adjust stats accordingly."""
        self.exp = 0
        self.lvl -= lvl
        self.set_stats()

    def set_lvl(self, lvl):
        """Set the level directly and adjust stats accordingly."""
        self.lvl = lvl
        self.set_stats()
