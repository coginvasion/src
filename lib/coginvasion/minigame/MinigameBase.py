# Embedded file name: lib.coginvasion.minigame.MinigameBase
from direct.showbase.DirectObject import DirectObject
from lib.coginvasion.globals import CIGlobals
from DistributedRaceGameAI import DistributedRaceGameAI
from DistributedUnoGameAI import DistributedUnoGameAI
from DistributedGunGameAI import DistributedGunGameAI
from DistributedMinigameAI import DistributedMinigameAI
from DistributedFactorySneakGameAI import DistributedFactorySneakGameAI
from DistributedCameraShyGameAI import DistributedCameraShyGameAI
from DistributedEagleGameAI import DistributedEagleGameAI
from DistributedDeliveryGameAI import DistributedDeliveryGameAI

class MinigameBase(DirectObject):

    def __init__(self, cr):
        DirectObject.__init__(self)
        self.minigame = None
        self.zoneId = None
        self.cr = cr
        return

    def createMinigame(self, game, numPlayers, avatars):
        self.zoneId = base.air.allocateZone()
        gameClass = DistributedMinigameAI
        if game == CIGlobals.RaceGame:
            gameClass = DistributedRaceGameAI
        elif game == CIGlobals.UnoGame:
            gameClass = DistributedUnoGameAI
        elif game == CIGlobals.GunGame:
            gameClass = DistributedGunGameAI
        elif game == CIGlobals.FactoryGame:
            gameClass = DistributedFactorySneakGameAI
        elif game == CIGlobals.CameraShyGame:
            gameClass = DistributedCameraShyGameAI
        elif game == CIGlobals.EagleGame:
            gameClass = DistributedEagleGameAI
        elif game == CIGlobals.DeliveryGame:
            gameClass = DistributedDeliveryGameAI
        self.minigame = gameClass(self.cr)
        self.minigame.generateWithRequired(self.zoneId)
        self.minigame.setNumPlayers(numPlayers)
        for avatar in avatars:
            self.minigame.appendAvatar(avatar)

        taskMgr.add(self.monitorAvatars, self.cr.uniqueName('monitorAvatars'))

    def monitorAvatars(self, task):
        for avatar in self.minigame.avatars:
            if avatar not in self.cr.doId2do.values():
                self.minigame.d_abort()
                self.handleEmptyMinigame()
                return task.done

        return task.cont

    def handleEmptyMinigame(self):
        taskMgr.remove(self.cr.uniqueName('monitorAvatars'))
        base.air.deallocateZone(self.zoneId)
        self.minigame.requestDelete()
        self.delete()

    def delete(self):
        del self.minigame
        del self.zoneId
        del self.cr