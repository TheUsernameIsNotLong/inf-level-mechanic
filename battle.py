from character import Character

class battle:
    def __init__(self, char1:Character, char2:Character):
        self.char1 = char1
        self.char2 = char2
        print(f"~ {char1.name}  VS. {char2.name} ~")
        print(f"  LV. {char1.stats.lvl}    LV. {char2.stats.lvl}")
        self.turnNum = 0
        self.turn()
    
    def turn(self):
        self.turnNum += 1
        print(f"Turn {self.turnNum}:")
    
    def attack(self, attacker:Character, defender:Character):
        damage = (4*attacker.stats.atk) - (3*defender.stats.dfc)
        defender.harm(damage)
    
    def escape(self):
        print("Escape battle")