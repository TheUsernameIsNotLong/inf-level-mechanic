import math
from status import *
class Stats:
    
    def __init__(self, lvl:int, exp:int, maxhp:int, hp:int, atk:int, dfc:int, mAtk:int, mDfc:int, spd:int):
        self.lvl = lvl
        self.exp = exp
        self.maxhp = maxhp
        self.hp = hp
        self.atk = atk
        self.dfc = dfc
        self.mAtk = mAtk
        self.mDfc = mDfc
        self.spd = spd
        self.setStats()

    def setStats(self):
        self.maxhp = calc_hp(self.lvl)
        self.hp = self.maxhp
        self.atk = calc_atk(self.lvl)
        self.dfc = calc_dfc(self.lvl)
        self.mAtk = calc_atk(self.lvl)
        self.mDfc = calc_dfc(self.lvl)
        self.spd = calc_spd(self.lvl)

    def addExp(self, exp):
        self.exp += exp
        while self.exp >= calc_expGoal(self.lvl): #maybe look into optimising from O(n) to O(1)
            self.exp -= calc_expGoal(self.lvl)
            self.lvl += 1
            print(f"You leveled up to Lvl. {self.lvl}!")
        self.setStats()

    def addLvl(self, lvl):
        exp = calc_expTotal(lvl + self.lvl) - calc_expTotal(self.lvl)
        self.addExp(exp)

class Character:

    def __init__(self, name:str, stats:Stats, player:bool):
        self.name = name
        self.stats = stats
        self.player = player
        self.knownSkills = []
        self.activeStates = []
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
        print(f"EXP:\t{self.stats.exp}/{calc_expGoal(self.stats.lvl)}")
        print(f"HP:\t{self.stats.hp}")
        print(f"ATK:\t{self.stats.atk}")
        print(f"DFC:\t{self.stats.dfc}")
        print(f"M.ATK:\t{self.stats.mAtk}")
        print(f"M.DFC:\t{self.stats.mDfc}")
        print(f"SPD:\t{self.stats.spd}")

def calc_lvl(exp):
    return math.floor((exp/100)**(1/2))

def calc_expTotal(lvl):
    return 100 * lvl**2

def calc_expGoal(lvl):
    return (100 * lvl**2) - (100 * (lvl-1)**2)

def calc_hp(lvl):
    return round(75 + ((lvl**3 * 5)**0.5))

def calc_atk(lvl):
    return round(20 + (4 * lvl))

def calc_dfc(lvl):
    return round(15 + (3 * lvl))

def calc_spd(lvl):
    return round(10 + (2 * lvl))