# Embedded file name: lib.coginvasion.tutorial.DistributedTutorialSuitAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import Sequence, Wait, Func
from direct.task import Task
from lib.coginvasion.cog.DistributedSuitAI import DistributedSuitAI
from lib.coginvasion.cog import SuitGlobals, SuitAttacks
from lib.coginvasion.npc.NPCWalker import NPCWalkInterval
from lib.coginvasion.globals import CIGlobals
import TutorialGlobals
import random

class DistributedTutorialSuitAI(DistributedSuitAI):
    notify = directNotify.newCategory('DistributedTutorialSuitAI')
    ATTACK_IVAL_RANGE = [3, 15]

    def __init__(self, air, index, tut, avatarId):
        DistributedSuitAI.__init__(self, air)
        self.tutPartIndex = index
        self.tutorial = tut
        self.avatarId = avatarId
        self.currentPath = None
        self.walkTrack = None
        return

    def delete(self):
        base.taskMgr.remove(self.uniqueName('monitorHealth'))
        base.taskMgr.remove(self.uniqueName('doAttack'))
        base.taskMgr.remove(self.uniqueName('scwaa'))
        self.stopAttacks()
        if self.track:
            self.track.pause()
            self.track = None
        if self.walkTrack:
            self.walkTrack.pause()
            self.walkTrack = None
        if self.currentPath:
            self.currentPath = None
        self.tutorial = None
        self.tutPartIndex = None
        self.avatarId = None
        DistributedSuitAI.delete(self)
        return

    def spawn(self):
        pos = TutorialGlobals.SUIT_POINTS[TutorialGlobals.SUIT_SPAWN_POINT]
        index = TutorialGlobals.SUIT_POINTS.index(pos)
        self.spawnPoint = index
        self.b_setSuitState(2, index, index)
        flyTrack = self.posInterval(3, pos, startPos=pos + (0, 0, 50))
        flyTrack.start()
        self.track = Sequence()
        self.track.append(Wait(5.4))
        self.track.append(Func(self.b_setAnimState, 'neutral'))
        self.track.append(Wait(1.0))
        self.track.append(Func(self.startAI))
        self.track.start()
        self.b_setParent(CIGlobals.SPRender)
        taskMgr.add(self.monitorHealth, self.uniqueName('monitorHealth'))

    def createPath(self, fromCurPos = False):
        durationFactor = 0.2
        if not hasattr(self, 'currentPath'):
            self.currentPath = None
        if self.currentPath == None:
            path = random.choice(TutorialGlobals.SUIT_POINTS)
            self.currentPath = TutorialGlobals.SUIT_POINTS.index(path)
            startIndex = -1
        else:
            if fromCurPos == False:
                startIndex = int(self.currentPath)
            else:
                startIndex = -1
            self.currentPath += 1
            if self.currentPath >= len(TutorialGlobals.SUIT_POINTS):
                self.currentPath = 0
            path = TutorialGlobals.SUIT_POINTS[self.currentPath]
        endIndex = self.currentPath
        startPos = self.getPos(render)
        pathName = self.uniqueName('suitPath')
        self.walkTrack = NPCWalkInterval(self, path, startPos=startPos, name=pathName, durationFactor=durationFactor, fluid=1)
        self.walkTrack.setDoneEvent(self.walkTrack.getName())
        self.acceptOnce(self.walkTrack.getDoneEvent(), self.createPath)
        self.walkTrack.start()
        self.b_setAnimState('walk')
        self.b_setSuitState(1, startIndex, endIndex)
        return

    def monitorHealth(self, task):
        if self.health <= 0:
            self.tutorial.sendUpdateToAvatarId(self.avatarId, 'suitNoHealth', [self.tutPartIndex])
            if self.walkTrack:
                self.ignore(self.walkTrack.getDoneEvent())
                self.walkTrack.pause()
                self.walkTrack = None
            self.b_setSuitState(0, -1, -1)
            currentAnim = SuitGlobals.getAnimByName(self.anim)
            self.clearTrack()
            base.taskMgr.remove(self.uniqueName('scwaa'))
            self.stopAttacks()
            if currentAnim:
                self.track = Sequence(Wait(currentAnim.getDeathHoldTime()), Func(self.killSuit))
                self.track.start()
            else:
                self.killSuit()
            return Task.done
        else:
            return Task.cont

    def setSuit(self, plan, variant = 0):
        DistributedSuitAI.setSuit(self, plan, variant, self.tutorial)

    def closeSuit(self):
        DistributedSuitAI.closeSuit(self)
        self.tutorial.sendUpdateToAvatarId(self.avatarId, 'suitExploded', [self.tutPartIndex])

    def startAttacks(self):
        base.taskMgr.doMethodLater(random.randint(*self.ATTACK_IVAL_RANGE), self.__doAttack, self.uniqueName('doAttack'))

    def __doAttack(self, task):
        base.taskMgr.remove(self.uniqueName('scwaa'))
        target = self.air.doId2do.get(self.avatarId)
        if not target:
            return task.done
        self.clearTrack()
        self.b_setSuitState(0, -1, -1)
        self.b_setAnimState('neutral')
        self.headsUp(target)
        attack = random.choice(self.suitPlan.getAttacks())
        attackIndex = SuitAttacks.SuitAttackLengths.keys().index(attack)
        attackTaunt = random.randint(0, len(CIGlobals.SuitAttackTaunts[attack]) - 1)
        timestamp = globalClockDelta.getFrameNetworkTime()
        if self.isDead():
            self.stopAttacks()
            return task.done
        self.sendUpdate('doAttack', [attackIndex, target.doId, timestamp])
        self.d_setChat(CIGlobals.SuitAttackTaunts[attack][attackTaunt])
        attackLength = SuitAttacks.SuitAttackLengths[attack]
        base.taskMgr.doMethodLater(attackLength, self.__suitContinueWalkAfterAttack, self.uniqueName('scwaa'))
        task.delayTime = random.randint(*self.ATTACK_IVAL_RANGE)
        return task.again

    def __suitContinueWalkAfterAttack(self, task):
        self.createPath(fromCurPos=True)
        return task.done

    def stopAttacks(self):
        base.taskMgr.remove(self.uniqueName('doAttack'))

    def startAI(self):
        if self.tutPartIndex == 0:
            self.b_setAnimState('neutral')
        elif self.tutPartIndex == 1:
            self.createPath()
        elif self.tutPartIndex == 2:
            self.createPath()
            self.startAttacks()