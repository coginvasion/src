# Embedded file name: lib.coginvasion.minigame.DistributedEagleGameAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.task import Task
from lib.coginvasion.globals import CIGlobals
from lib.coginvasion.cog import SuitBank
from DistributedEagleSuitAI import DistributedEagleSuitAI
from DistributedToonCannonAI import DistributedToonCannonAI
from DistributedMinigameAI import DistributedMinigameAI

class DistributedEagleGameAI(DistributedMinigameAI):
    notify = directNotify.newCategory('DistributedEagleGameAI')
    MaxEagles = 5
    NumRounds = 3
    RoundTime = 65

    def __init__(self, air):
        DistributedMinigameAI.__init__(self, air)
        self.setZeroCommand(self.b_roundOver)
        self.setInitialTime(self.RoundTime)
        self.cannonPositions = {0: (-5, 0, 0),
         1: (-15, 0, 0),
         2: (5, 0, 0),
         3: (15, 0, 0)}
        self.cannonId2cannon = {}
        self.eagleId2eagle = {}
        self.avId2score = {}
        self.round = 1
        self.winnerPrize = 60
        self.loserPrize = 20

    def d_gameOver(self):
        winners = []
        for avId in self.avId2score.keys():
            score = self.avId2score[avId]
            if score == max(self.avId2score.values()):
                winners.append(avId)

        DistributedMinigameAI.d_gameOver(self, 1, winners)

    def gameOverTask(self, task):
        self.d_gameOver()
        return Task.done

    def allRoundsEndedTask(self, task):
        self.sendUpdate('allRoundsEnded', [])
        avIdArray = self.avId2score.keys()
        scoreArray = self.avId2score.values()
        self.sendUpdate('finalScores', [avIdArray, scoreArray])
        taskMgr.doMethodLater(7.0, self.gameOverTask, self.uniqueName('DEagleGameAI-gameOver'))
        return Task.done

    def roundOver(self):
        taskMgr.remove(self.uniqueName('DEagleGameAI-eagleSpawner'))
        if self.getRound() < self.NumRounds:
            taskMgr.doMethodLater(3.3, self.__swapEagles, self.uniqueName('DEagleGameAI-swapEagles'))
            taskMgr.doMethodLater(5.55, self.startNewRoundTask, self.uniqueName('DEagleGameAI-startNewRound'))
        else:
            taskMgr.doMethodLater(3.3, self.removeAllEaglesTask, self.uniqueName('DEagleGameAI-removeAllEagles'))
            taskMgr.doMethodLater(5.1499999999999995, self.allRoundsEndedTask, self.uniqueName('DEagleGameAI-allRoundsEnded'))

    def d_roundOver(self):
        self.sendUpdate('roundOver', [])

    def b_roundOver(self):
        self.d_roundOver()
        self.roundOver()

    def startNewRoundTask(self, task):
        self.d_startRound(self.getRound())
        return Task.done

    def removeAllEaglesTask(self, task):
        self.__removeAllEagles()
        return Task.done

    def __removeAllEagles(self):
        for eagle in self.eagleId2eagle.values():
            del self.eagleId2eagle[eagle.doId]
            eagle.disable()
            eagle.requestDelete()

    def __swapEagles(self, task):
        self.startRound(self.getRound() + 1)
        self.__removeAllEagles()
        taskMgr.add(self.__eagleSpawner, self.uniqueName('DEagleGameAI-eagleSpawner'))

    def __makeEagle(self):
        if not self.air:
            return
        eagle = DistributedEagleSuitAI(self.air)
        eagle.setMinigame(self)
        eagle.generateWithRequired(self.zoneId)
        eagle.b_setLevel(0)
        eagle.b_setSuit(SuitBank.getIdFromSuit(SuitBank.LegalEagle), 3)
        eagle.b_setName(SuitBank.LegalEagle.getName())
        eagle.b_setPlace(self.zoneId)
        self.eagleId2eagle[eagle.doId] = eagle

    def __eagleSpawner(self, task):
        if len(self.eagleId2eagle.keys()) == 0:
            for _ in range(self.MaxEagles):
                self.__makeEagle()

        elif len(self.eagleId2eagle.keys()) < self.MaxEagles:
            self.__makeEagle()
        task.delayTime = 2.0
        return Task.again

    def startRound(self, num):
        self.round = num

    def d_startRound(self, num):
        self.startTiming()
        self.sendUpdate('startRound', [num])

    def b_startRound(self, num):
        self.d_startRound(num)
        self.startRound(num)

    def getRound(self):
        return self.round

    def needACannon(self):
        self.missedEagle()

    def hitEagle(self, eagleId):
        avId = self.air.getAvatarIdFromSender()
        if not self.avId2score.get(avId):
            self.avId2score[avId] = 1
        else:
            self.avId2score[avId] += 1
        self.sendUpdate('updateHeadPanelValue', [avId, 1])
        eagle = self.eagleId2eagle.get(eagleId)
        if eagle:
            eagle.handleGotHit()
            del self.eagleId2eagle[eagleId]
        cannonId = self.getCannonOfAvatar(avId)
        self.sendUpdateToAvatarId(avId, 'enterCannon', [cannonId])

    def missedEagle(self):
        avId = self.air.getAvatarIdFromSender()
        cannonId = self.getCannonOfAvatar(avId)
        self.sendUpdateToAvatarId(avId, 'enterCannon', [cannonId])

    def getCannonOfAvatar(self, avId):
        for avatar in self.avatars:
            if avatar.doId == avId:
                return self.cannonId2cannon.keys()[self.avatars.index(avatar)]

    def allAvatarsReady(self):
        for avatar in self.avatars:
            self.sendUpdateToAvatarId(avatar.doId, 'enterCannon', [self.getCannonOfAvatar(avatar.doId)])

        DistributedMinigameAI.allAvatarsReady(self)
        self.sendHeadPanels()
        self.b_startRound(1)

    def announceGenerate(self):
        DistributedMinigameAI.announceGenerate(self)
        for i in range(4):
            cannon = DistributedToonCannonAI(self.air)
            cannon.generateWithRequired(self.zoneId)
            cannon.d_setPos(*self.cannonPositions[i])
            cannon.b_setParent(CIGlobals.SPRender)
            self.cannonId2cannon[cannon.doId] = cannon

        taskMgr.add(self.__eagleSpawner, self.uniqueName('DEagleGameAI-eagleSpawner'))

    def delete(self):
        self.stopTiming()
        taskMgr.remove(self.uniqueName('DEagleGameAI-removeAllEagles'))
        taskMgr.remove(self.uniqueName('DEagleGameAI-gameOver'))
        taskMgr.remove(self.uniqueName('DEagleGameAI-swapEagles'))
        taskMgr.remove(self.uniqueName('DEagleGameAI-startNewRound'))
        taskMgr.remove(self.uniqueName('DEagleGameAI-eagleSpawner'))
        for cannon in self.cannonId2cannon.values():
            cannon.disable()
            cannon.requestDelete()

        del self.cannonId2cannon
        for eagle in self.eagleId2eagle.values():
            eagle.disable()
            eagle.requestDelete()

        del self.eagleId2eagle
        del self.cannonPositions
        del self.eagleFlyPoints
        del self.round
        DistributedMinigameAI.delete(self)