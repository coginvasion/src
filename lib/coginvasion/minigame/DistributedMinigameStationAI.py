# Embedded file name: lib.coginvasion.minigame.DistributedMinigameStationAI
"""

  Filename: DistributedMinigameStationAI.py
  Created by: blach (15Oct14)

"""
from panda3d.core import *
from lib.coginvasion.globals import CIGlobals
from pandac.PandaModules import *
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.interval.IntervalGlobal import *
import MinigameBase
from DistributedGroupStationAI import DistributedGroupStationAI

class DistributedMinigameStationAI(DistributedGroupStationAI):
    game2maxPlayers = {CIGlobals.UnoGame: 4,
     CIGlobals.RaceGame: 4,
     CIGlobals.GunGame: 8,
     CIGlobals.FactoryGame: 4,
     CIGlobals.CameraShyGame: 4,
     CIGlobals.EagleGame: 4,
     CIGlobals.DeliveryGame: 4}

    def __init__(self, air):
        try:
            self.DistributedMinigameStationAI_initialized
            return
        except:
            self.DistributedMinigameStationAI_initialized = 1

        DistributedGroupStationAI.__init__(self, air)
        self.game = ''

    def setStation(self, game):
        self.game = game
        self.maxAvatars = self.game2maxPlayers[self.game]
        self.availableSlots = self.maxAvatars
        self.maximumSlots = self.maxAvatars
        self.resetAvailableSlots()

    def b_setStation(self, game):
        self.d_setStation(game)
        self.setStation(game)

    def d_setStation(self, game):
        self.sendUpdate('setStation', [game])

    def getStation(self):
        return self.game

    def monitorTime(self, task):
        if self.time == 0:
            self.stopTimer()
            self.createMinigame()
            return task.done
        return task.cont

    def createMinigame(self):
        minigame = MinigameBase.MinigameBase(self.air)
        minigame.createMinigame(self.game, len(self.avatars), self.avatars)
        laffMeter = 1
        if self.game in [CIGlobals.UnoGame,
         CIGlobals.GunGame,
         CIGlobals.FactoryGame,
         CIGlobals.CameraShyGame]:
            laffMeter = 0
        for avatar in self.avatars:
            self.d_headOff(avatar.doId, minigame.zoneId, laffMeter)

        del minigame

    def d_headOff(self, doId, zone, laffMeter):
        self.sendUpdateToAvatarId(doId, 'headOff', [zone, laffMeter])

    def delete(self):
        DistributedGroupStationAI.delete(self)
        self.game = None
        return