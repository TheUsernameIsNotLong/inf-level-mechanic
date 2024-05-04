from character import *
from battle import *

startLvl = int(input("Enter the level to start at: "))
startStats = Stats(startLvl,0,0,0,0,0,0,0,0)
player = Character("You", startStats)
enemy = Character("Enemy", startStats)

battleActions = ("Attack",
                 "Escape")

battle(player, enemy)

# while True:
#     player.printStats()
#     exp = int(input("Exp to add: "))
#     player.stats.addExp(exp)
