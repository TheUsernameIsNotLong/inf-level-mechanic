from character import *

startLvl = int(input("Enter the level to start at: "))
playerStats = stats(startLvl,0,0,0,0,0,0,0)
player = character("You", playerStats)
player.stats.set()

while True:
    player.printStats()
    exp = int(input("Exp to add: "))
    player.stats.addExp(exp)