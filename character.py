import math
from status import *

class Proficiency:
    
    def __init__(self, hp:int=0, atk:int=0, dfc:int=0, mAtk:int=0, mDfc:int=0, spd:int=0):
        
        #  3 -> S Rank (best)
        #  2 -> A Rank
        #  1 -> B Rank
        #  0 -> C Rank (standard)
        # -1 -> D Rank
        # -2 -> E Rank
        # -3 -> F Rank (worst)
        
        self.hp = hp
        self.atk = atk
        self.dfc = dfc
        self.mAtk = mAtk
        self.mDfc = mDfc
        self.spd = spd

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

class Character:

    def __init__(self, name:str, stats:Stats, player:bool):
        self.name = name
        self.stats = stats
        self.player = player
        self.knownSkills = []
        self.activeStates = []
        self.modifiers = []
        # VVV Passive States VVV
        self.canHeal = True # Can recieve healing from any healing source
        # VVV Current Actions VVV
        self.battle = None # Is this character currently in a battle?
    
    def harm(self, hp):
        self.stats.hp -= hp
        if self.stats.hp <= 0:
            self.stats.hp = 0 # Do not allow negative health
            self.addStatus(KO())
    
    def heal(self, hp):
        self.stats.hp += hp
        if self.stats.hp > self.stats.maxhp:
            self.stats.hp = self.stats.maxhp
            
    def addStatus(self, status:Status):
        print(f"{self.name} is inflicted with {status.name}!")
        self.activeStates.append(status) # This may replace statuses with lower duration/lvl
        if isinstance(status, KO): # Run status effect immediately if defeated
            status.apply(self)
    
    def removeStatus(self, status:Status):
        try:
            self.activeStates.remove(status)
            print(f"{self.name} is no longer inflicted with {status.name}!")
        except:
            print(f"{self.name} is not inflicted with {status.name}!")

    
    def applyStatus(self):
        for s in self.activeStates:
            if isinstance(s, Status_Damage):
                s.apply()
    
    def printStats(self):
        print("~ CHARACTER SHEET ~")
        print(f"NAME:\t{self.name}")
        print(f"LVL:\t{self.stats.lvl}")
        print(f"EXP:\t{self.stats.exp}/{self.stats.calc_expGoal(self.stats.lvl)}")
        print(f"HP:\t{self.stats.hp}")
        print(f"ATK:\t{self.stats.atk}")
        print(f"DFC:\t{self.stats.dfc}")
        print(f"M.ATK:\t{self.stats.mAtk}")
        print(f"M.DFC:\t{self.stats.mDfc}")
        print(f"SPD:\t{self.stats.spd}")