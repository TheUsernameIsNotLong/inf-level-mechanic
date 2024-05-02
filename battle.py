class battle:
    def __init__(self, char1, char2):
        self.char1 = char1
        self.char2 = char2
        print(f"~ {char1.name} VS. {char2.name} ~")
    
    def turn(self):
        print("Turn X:")