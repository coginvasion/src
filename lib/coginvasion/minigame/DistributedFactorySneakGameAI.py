# Embedded file name: lib.coginvasion.minigame.DistributedFactorySneakGameAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from DistributedToonFPSGameAI import DistributedToonFPSGameAI

class DistributedFactorySneakGameAI(DistributedToonFPSGameAI):
    notify = directNotify.newCategory('DistributedFactorySneakGameAI')