class Status:
    def __init__(self, name:str, desc:str, duration:int):
        self.name = name
        self.desc = desc
        self.duration = duration
    
    def apply(self):
        pass
    
class Poison(Status):
    def __init__(self):
        super().__init__("Poison", "Take reccuring damage.", 3)
        
    def apply(self):