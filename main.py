from character import *

startLvl = int(input("Enter the level to start at: "))
startStats = stats(startLvl,0,0,0,0,0,0,0)
defaultSkillPoints = 30
player = character("You", startStats)
player.stats.setStats()

while True:
    player.printStats()
    exp = int(input("Exp to add: "))
    player.stats.addExp(exp)