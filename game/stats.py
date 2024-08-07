import math
from proficiency import *

class Stats:
    
    def __init__(self, lvl:int, prof:Proficiency):
        self.lvl = lvl
        self.prof = prof
        self.exp = 0
        self.maxhp = 0
        self.hp = 0
        self.atk = 0
        self.dfc = 0
        self.mAtk = 0
        self.mDfc = 0
        self.spd = 0
        self.setStats()
    
    def calc_lvl(exp):
        return math.floor((exp/100)**(1/2))

    def calc_expTotal(self, lvl):
        return 100 * lvl**2

    def calc_expGoal(self, lvl):
        return (100 * lvl**2) - (100 * (lvl-1)**2)

    def calc_hp(self, lvl):
        pValue = (20+self.prof.hp)/20
        return round((75 + ((lvl**3 * 5)**0.5))**pValue)

    def calc_atk(self, lvl):
        pValue = (20+self.prof.atk)/20
        return round((20 + (4 * lvl))**pValue)

    def calc_dfc(self, lvl):
        pValue = (20+self.prof.dfc)/20
        return round((15 + (3 * lvl))**pValue)

    def calc_spd(self, lvl):
        pValue = (20+self.prof.spd)/20
        return round((10 + (2 * lvl))**pValue)

    def setStats(self):
        self.maxhp = self.calc_hp(self.lvl)
        self.hp = self.maxhp
        self.atk = self.calc_atk(self.lvl)
        self.dfc = self.calc_dfc(self.lvl)
        self.mAtk = self.calc_atk(self.lvl)
        self.mDfc = self.calc_dfc(self.lvl)
        self.spd = self.calc_spd(self.lvl)

    def addExp(self, exp):
        self.exp += exp
        while self.exp >= self.calc_expGoal(self.lvl): #maybe look into optimising from O(n) to O(1)
            self.exp -= self.calc_expGoal(self.lvl)
            self.lvl += 1
            print(f"You leveled up to Lvl. {self.lvl}!")
        self.setStats()

    def addLvl(self, lvl):
        exp = self.calc_expTotal(lvl + self.lvl) - self.calc_expTotal(self.lvl)
        self.addExp(exp)
    
    def remLvl(self, lvl):
        self.exp = 0
        self.lvl -= lvl
        self.setStats()
        
    def setLvl(self, lvl):
        self.lvl = lvl
        self.setStats()