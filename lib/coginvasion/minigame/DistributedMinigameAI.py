# Embedded file name: lib.coginvasion.minigame.DistributedMinigameAI
"""

  Filename: DistributedMinigameAI.py
  Created by: blach (06Oct14)

"""
from panda3d.core import *
from lib.coginvasion.globals import CIGlobals
from pandac.PandaModules import *
from direct.distributed import DistributedObjectAI
import TimerAI

class DistributedMinigameAI(DistributedObjectAI.DistributedObjectAI, TimerAI.TimerAI):

    def __init__(self, air):
        try:
            self.DistributedMinigameAI_initialized
            return
        except:
            self.DistributedMinigameAI_initialized = 1

        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        TimerAI.TimerAI.__init__(self)
        self.air = air
        self.readyAvatars = 0
        self.numPlayers = 0
        self.avatars = []
        self.zone = 0
        self.finalScores = []
        self.finalScoreAvIds = []

    def myFinalScore(self, score):
        avId = self.air.getAvatarIdFromSender()
        self.finalScoreAvIds.append(avId)
        self.finalScores.append(score)
        if len(self.finalScores) == self.numPlayers:
            self.sendUpdate('finalScores', [self.finalScoreAvIds, self.finalScores])

    def sendHeadPanels(self):
        gender = None
        head = None
        for avatar in self.avatars:
            gender = avatar.getGender()
            animal = avatar.getAnimal()
            head, color = avatar.getHeadStyle()
            r, g, b, _ = color
            self.d_generateHeadPanel(gender, animal, head, [r, g, b], avatar.doId, avatar.getName())

        return

    def d_generateHeadPanel(self, gender, head, headtype, color, doId, name):
        self.sendUpdate('generateHeadPanel', [gender,
         head,
         headtype,
         color,
         doId,
         name])

    def d_updateHeadPanelValue(self, doId, direction):
        self.sendUpdate('updateHeadPanelValue', [doId, direction])

    def appendAvatar(self, avatar):
        self.avatars.append(avatar)

    def clearAvatar(self, avatar = None, doId = None):
        if avatar != None and doId != None or avatar == None and doId == None:
            return
        else:
            if avatar != None:
                self.avatars.remove(avatar)
            elif doId != None:
                for avatar in self.avatars:
                    if avatar.doId == doId:
                        self.avatars.remove(avatar)

            return

    def isAvatarPresent(self, doId):
        for avatar in self.avatars:
            if avatar.doId == doId:
                return True

        return False

    def setNumPlayers(self, players):
        self.numPlayers = players

    def getNumPlayers(self):
        return self.numPlayers

    def getAvatarName(self, doId):
        for avatar in self.avatars:
            if avatar.doId == doId:
                return avatar.getName()

        return None

    def ready(self):
        if self.readyAvatars == None:
            return
        else:
            self.readyAvatars += 1
            if self.areAllAvatarsReady():
                self.allAvatarsReady()
            return

    def areAllAvatarsReady(self):
        return self.getNumPlayers() == self.readyAvatars

    def allAvatarsReady(self):
        self.d_startGame()

    def leaving(self):
        doId = self.air.getAvatarIdFromSender()
        if self.isAvatarPresent(doId):
            self.clearAvatar(doId=doId)

    def d_startGame(self):
        self.sendUpdate('allPlayersReady', [])

    def d_gameOver(self, winner = 0, winnerDoId = []):
        self.givePrizes(winnerDoId)
        self.sendUpdate('gameOver', [winner, winnerDoId, 0])

    def d_abort(self):
        self.sendUpdate('abort', [])

    def givePrizes(self, winnerAvId):
        for avatar in self.avatars:
            if avatar.doId in winnerAvId:
                avatar.b_setMoney(avatar.getMoney() + self.winnerPrize)
            else:
                avatar.b_setMoney(avatar.getMoney() + self.loserPrize)

    def d_setTimerTime(self, time):
        self.sendUpdate('setTimerTime', [time])

    def delete(self):
        DistributedObjectAI.DistributedObjectAI.delete(self)
        TimerAI.TimerAI.disable(self)
        self.readyAvatars = None
        self.numPlayers = None
        self.avatars = None
        self.zone = None
        return