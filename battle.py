import random
from character import Character

class battle:
    def __init__(self, char1:Character, char2:Character):
        self.char1 = char1
        self.char2 = char2
        self.battleActions = ["Attack",
                              "Escape"]
        print(f"~ {char1.name}  VS. {char2.name} ~")
        print(f"  LV. {char1.stats.lvl}    LV. {char2.stats.lvl}")
        self.turnNum = 0
        self.turn(char1, char2)
    
    def turn(self, char1:Character, char2:Character):
        self.turnNum += 1
        print(f"Turn {self.turnNum}:")
        print()
        print(f"{char2.name}")
        print(f"HP: {char2.stats.hp}/{char2.stats.maxhp}")
        print()
        print(f"{char1.name}")
        print(f"HP: {char1.stats.hp}/{char1.stats.maxhp}")
        print()
        for i in range(len(self.battleActions)):
            print(f"{i+1}. {self.battleActions[i]}")
        while True:
            try:
                choice = int(input("Your turn: "))
                if (choice >= 1) and (choice <= len(self.battleActions)):
                    match choice:
                        case 1:
                            self.attack(char1, char2)
                            break
                        case 2:
                            self.escape()
                            break
                        case _:
                            print("You can't do that!")
            except Exception as e:
                print("You can't do that!")
                print(e)
        self.turn(char1, char2)
    
    def attack(self, attacker:Character, defender:Character):
        randModifier = 0.75 + (random.random()/2)
        damage = round(randModifier*((2*attacker.stats.atk) - (defender.stats.dfc)))
        defender.harm(damage)
    
    def escape(self):
        print("Escape battle")