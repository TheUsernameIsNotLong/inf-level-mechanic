from character import *
from battle import *

startLvl = int(input("Enter the level to start at: "))
startStats = stats(startLvl,0,0,0,0,0,0,0)
player = character("You", startStats)
player.stats.setStats()

enemy = character("Enemy", startStats)

while True:
    player.printStats()
    exp = int(input("Exp to add: "))
    player.stats.addExp(exp)