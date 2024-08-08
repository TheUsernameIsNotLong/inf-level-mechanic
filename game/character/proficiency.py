class Proficiency:
    
    def __init__(self, name:str, hp:int=0, mp:int=0, atk:int=0, dfc:int=0, mAtk:int=0, mDfc:int=0, spd:int=0):
        
        #  3 -> S Rank (best)
        #  2 -> A Rank
        #  1 -> B Rank
        #  0 -> C Rank (standard)
        # -1 -> D Rank
        # -2 -> E Rank
        # -3 -> F Rank (worst)
        
        self.name = name
        self.hp = hp
        self.mp = mp
        self.atk = atk
        self.dfc = dfc
        self.mAtk = mAtk
        self.mDfc = mDfc
        self.spd = spd

# Proficiency sets
profStandard = Proficiency("Standard",0,0,0,0,0,0,0)
profOP = Proficiency("Over-powered",3,3,3,3,3,3,3)
profWK = Proficiency("Weak",-3,-3,-3,-3,-3,-3,-3)

# Player proficiency sets
profTank = Proficiency("Tanky",1,0,-1,3,-2,2,-3)
profMage = Proficiency("Mage",-1,3,-3,-2,2,2,-1)
profSorcerer = Proficiency("Sorcerer",-1,1,-3,-2,3,3,-1)
profCannon = Proficiency("Glass Cannon",-1,0,1,-1,1,-1,1)
profTrueCannon = Proficiency("TRUE Glass Cannon",-3,0,3,-3,3,-3,3)

# Enemy proficiency sets
profJuggernaut = Proficiency("Juggernaut",3,0,1,1,-2,1,-2)
profWeak = Proficiency("Weak",-3,0,-1,-2,-1,-2,2)
profLethal = Proficiency("Lethal",-1,0,3,-1,3,-1,-1)

availableProficiencies = [profStandard,
                          profTank,
                          profMage,
                          profSorcerer,
                          profCannon,
                          profTrueCannon]