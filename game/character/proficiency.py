""" 
Modules imported:
- dataclasses: For defining data classes.
"""

from dataclasses import dataclass

@dataclass
class Proficiency:
    """Class representing character proficiency, affecting various stats."""

    name: str
    hp: int
    mp: int
    atk: int
    dfc: int
    m_atk: int
    m_dfc: int
    spd: int

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
