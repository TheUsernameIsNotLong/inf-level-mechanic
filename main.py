from character import *
from battle import *

startLvl = int(input("Enter the level to start at: "))
player = Character("You", Stats(startLvl,0,0,0,0,0,0,0,0))
enemy = Character("Enemy", Stats(startLvl,0,0,0,0,0,0,0,0))

# player.removeStatus(Poison(1))

battle(player, enemy)

# while True:
#     player.printStats()
#     exp = int(input("Exp to add: "))
#     player.stats.addExp(exp)