from character import *
from battle import *

startLvl = int(input("Enter the level to start at: "))
startStats = stats(startLvl,0,0,0,0,0,0,0)
player = character("You", startStats)
enemy = character("Bad Guy", startStats)
player.stats.setStats()
<<<<<<< HEAD

enemy = character("Enemy", startStats)

while True:
    player.printStats()
    exp = int(input("Exp to add: "))
    player.stats.addExp(exp)
=======
battle(player)
# while True:
#     player.printStats()
#     exp = int(input("Exp to add: "))
#     player.stats.addExp(exp)
>>>>>>> 5eef6d4d1725264ca735e6a26e48cfead9be1324
