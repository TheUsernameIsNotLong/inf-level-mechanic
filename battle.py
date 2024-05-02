from character import character

class battle:
    def __init__(self, char1:character, char2:character) -> None: #chars: list,
        self.char1 = char1
        self.char2 = char2
        #characters = {}
        #for idx, character in enumerate(...chars):
        #    characters[f"character{idx}"]
            
        print(f"~ {char1.name} VS. {char2.name} ~")
        turn = 0
        self.turn()
    
    def turn(self):
        turn += 1
        print(f"Turn {turn}:")