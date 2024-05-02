from character import *

startLvl = int(input("Enter the level to start at: "))
startStats = stats(startLvl,0,0,0,0,0,0,0)
defaultSkillPoints = 30
player = character("You", startStats)
player.stats.setStats()
<<<<<<< HEAD
<<<<<<< HEAD

enemy = character("Enemy", startStats)
=======
>>>>>>> parent of 5eef6d4 (updated stuff)

while True:
    player.printStats()
    exp = int(input("Exp to add: "))
<<<<<<< HEAD
    player.stats.addExp(exp)
=======
battle(player)
# while True:
#     player.printStats()
#     exp = int(input("Exp to add: "))
#     player.stats.addExp(exp)
>>>>>>> 5eef6d4d1725264ca735e6a26e48cfead9be1324
=======
    player.stats.addExp(exp)
>>>>>>> parent of 5eef6d4 (updated stuff)
