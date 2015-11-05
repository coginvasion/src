# Embedded file name: lib.coginvasion.cog.DistributedSuit
"""

  Filename: DistributedSuit.py
  Created by: DecodedLogic (01Sep15)

"""
from direct.distributed.DistributedSmoothNode import DistributedSmoothNode
from direct.distributed.DelayDeletable import DelayDeletable
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.interval.IntervalGlobal import SoundInterval, LerpPosInterval, ProjectileInterval
from direct.interval.IntervalGlobal import Sequence, LerpColorScaleInterval, Func
from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from lib.coginvasion.avatar.DistributedAvatar import DistributedAvatar
from lib.coginvasion.cog.SuitState import SuitState
from lib.coginvasion.cog import SuitBank
from lib.coginvasion.cog.SuitBank import SuitPlan
from lib.coginvasion.cog import SuitGlobals
from lib.coginvasion.cog import Voice
from lib.coginvasion.cog import Variant
from lib.coginvasion.cog.Suit import Suit
from lib.coginvasion.cog.SpawnMode import SpawnMode
from lib.coginvasion.globals import CIGlobals
from lib.coginvasion.npc.NPCWalker import NPCWalkInterval
from lib.coginvasion.suit import SuitAttacks
from panda3d.core import Point3, VBase4
import types, random

class DistributedSuit(Suit, DistributedAvatar, DistributedSmoothNode, DelayDeletable):
    notify = directNotify.newCategory('DistributedSuit')

    def __init__(self, cr):
        Suit.__init__(self)
        DistributedAvatar.__init__(self, cr)
        DistributedSmoothNode.__init__(self, cr)
        self.anim = None
        self.state = SuitState.ALIVE
        self.dept = None
        self.variant = None
        self.suitPlan = None
        self.level = None
        self.moveIval = None
        self.suitFSM = ClassicFSM('DistributedSuit', [State('off', self.enterSuitOff, self.exitSuitOff),
         State('walking', self.enterWalking, self.exitWalking),
         State('flyingDown', self.enterFlyingDown, self.exitFlyingDown),
         State('flyingUp', self.enterFlyingUp, self.exitFlyingUp),
         State('lured', self.enterLured, self.exitLured)], 'off', 'off')
        self.stateIndex2suitState = {}
        self.suitFSM.enterInitialState()
        self.makeStateDict()
        return

    def enterWalking(self, startIndex, endIndex, ts = 0.0):
        durationFactor = 0.2
        if startIndex > -1:
            startPoint = CIGlobals.SuitSpawnPoints[self.getHood()].keys()[startIndex]
            startPos = CIGlobals.SuitSpawnPoints[self.getHood()][startPoint]
        else:
            startPos = self.getPos(render)
        endPoint = CIGlobals.SuitSpawnPoints[self.getHood()].keys()[endIndex]
        endPos = CIGlobals.SuitSpawnPoints[self.getHood()][endPoint]
        self.stopMoving()
        self.moveIval = NPCWalkInterval(self, endPos, durationFactor, startPos, fluid=1)
        self.moveIval.start(ts)
        self.animFSM.request('walk')

    def exitWalking(self):
        if self.moveIval:
            self.moveIval.pause()
            self.moveIval = None
        if not self.isDead():
            self.animFSM.request('off')
        return

    def enterFlyingDown(self, startIndex, endIndex, ts = 0.0):
        if self.getHood() != '' and startIndex != -1 and endIndex != -1:
            duration = 3
            startPoint = CIGlobals.SuitSpawnPoints[self.getHood()].keys()[startIndex]
            startPos = CIGlobals.SuitSpawnPoints[self.getHood()][startPoint] + (0, 0, 50)
            endPoint = CIGlobals.SuitSpawnPoints[self.getHood()].keys()[endIndex]
            endPos = CIGlobals.SuitSpawnPoints[self.getHood()][endPoint]
            self.stopMoving(finish=1)
            self.moveIval = LerpPosInterval(self, duration=duration, pos=endPos, startPos=startPos, fluid=1)
            self.moveIval.start(ts)
        self.animFSM.request('flyDown', [ts])
        yaw = random.uniform(0.0, 360.0)
        self.setH(yaw)

    def exitFlyingDown(self):
        self.stopMoving(finish=1)
        self.animFSM.request('off')

    def enterFlyingUp(self, startIndex, endIndex, ts = 0.0):
        if self.getHood() != '' and startIndex != -1 and endIndex != -1:
            duration = 3
            startPoint = CIGlobals.SuitSpawnPoints[self.getHood()].keys()[startIndex]
            endPoint = CIGlobals.SuitSpawnPoints[self.getHood()].keys()[endIndex]
            startPos = CIGlobals.SuitSpawnPoints[self.getHood()][startPoint]
            endPos = CIGlobals.SuitSpawnPoints[self.getHood()][endPoint] + (0, 0, 50)
            self.stopMoving(finish=1)
            self.moveIval = LerpPosInterval(self, duration=duration, pos=endPos, startPos=startPos, fluid=1)
            self.moveIval.start(ts)
        self.animFSM.request('flyAway', [ts])

    def exitFlyingUp(self):
        if self.moveIval:
            self.moveIval.finish()
            self.moveIval = None
        self.animFSM.request('off')
        return

    def enterLured(self, _, __, ___):
        self.loop('lured')

    def exitLured(self):
        self.stop()

    def enterSuitOff(self, foo1 = None, foo2 = None, foo3 = None):
        pass

    def exitSuitOff(self):
        pass

    def setName(self, name):
        Suit.setName(self, name, self.suitPlan.getName())

    def setLevel(self, level):
        self.level = level
        if self.level == 12:
            self.maxHealth = 200
        elif self.level > 0:
            self.maxHealth = (self.level + 1) * (self.level + 2)
        else:
            self.maxHealth = 1
        self.health = self.maxHealth
        self.updateHealthBar(self.health)

    def getLevel(self):
        return self.level

    def startMoveInterval(self, startX, startY, startZ, endX, endY, endZ, duration):
        self.stopMoving()
        endPos = Point3(endX, endY, endZ)
        self.moveIval = NPCWalkInterval(self, endPos, durationFactor=duration, fluid=1)
        self.moveIval.start()

    def stopMoveInterval(self):
        if self.moveIval:
            self.moveIval.clearToInitial()
            self.moveIval = None
        return

    def toggleRay(self, ray = 1):
        if ray:
            Suit.initializeRay(self, self.avatarType, 2)
        else:
            Suit.disableRay(self)

    def startProjInterval(self, startX, startY, startZ, endX, endY, endZ, duration, gravityMult, ts = 0.0):
        if ts != 0.0:
            ts = globalClockDelta.localElapsedTime(ts)
        self.stopMoveInterval()
        startPos = Point3(startX, startY, startZ)
        endPos = Point3(endX, endY, endZ)
        self.headsUp(endPos)
        self.moveIval = ProjectileInterval(self, startPos=startPos, endPos=endPos, gravityMult=gravityMult, duration=duration)
        self.moveIval.start(ts)

    def startPosInterval(self, startX, startY, startZ, endX, endY, endZ, duration, blendType, ts = 0.0):
        if ts != 0.0:
            ts = globalClockDelta.localElapsedTime(ts)
        self.stopMoveInterval()
        startPos = Point3(startX, startY, startZ)
        endPos = Point3(endX, endY, endZ)
        self.moveIval = LerpPosInterval(self, duration=duration, pos=endPos, startPos=startPos, blendType=blendType)
        self.moveIval.start(ts)

    def stopMoving(self, finish = 0):
        if self.moveIval:
            if finish:
                self.moveIval.finish()
            else:
                self.moveIval.pause()
            self.moveIval = None
        return

    def d_disableMovement(self, wantRay = False):
        self.sendUpdate('disableMovement', [])
        self.interruptAttack()
        self.stopMoving()
        if not wantRay:
            Suit.disableRay(self)

    def d_enableMovement(self):
        self.sendUpdate('enableMovement', [])
        Suit.initializeRay(self, self.avatarType, 2)

    def startRay(self):
        Suit.initializeRay(self, self.avatarType, 2)

    def setHealth(self, health):
        DistributedAvatar.setHealth(self, health)
        if self.isDead():
            self.interruptAttack()
        if self.getLevel() > 12:
            Sequence(LerpColorScaleInterval(self, 0.2, VBase4(1, 0, 0, 1)), Func(self.clearColorScale)).start()
        self.updateHealthBar(health)

    def announceHealth(self, level, hp):
        DistributedAvatar.announceHealth(self, level, hp)
        if level == 1:
            healthSfx = base.loadSfx(SuitGlobals.healedSfx)
            SoundInterval(healthSfx, node=self).start()
            del healthSfx

    def setSuit(self, arg, variant = 0):
        if isinstance(arg, SuitPlan):
            plan = arg
        else:
            plan = SuitBank.getSuitById(arg)
        voice = Voice.NORMAL
        if variant:
            if isinstance(variant, (int,
             long,
             float,
             complex)):
                variant = Variant.getVariantById(variant)
        if plan.getForcedVoice():
            voice = plan.getForcedVoice()
        Suit.generate(self, plan, variant, voice=voice)
        self.suitPlan = plan
        self.variant = Variant.getVariantById(variant)

    def getSuit(self):
        return tuple((self.suitPlan, self.variant))

    def spawn(self, startIndex, endIndex, spawnMode = SpawnMode.FLYDOWN):
        if spawnMode == SpawnMode.FLYDOWN:
            startPoint = CIGlobals.SuitSpawnPoints[self.getHood()].keys()[startIndex]
            startPos = CIGlobals.SuitSpawnPoints[self.getHood()][startPoint] + (0, 0, 50)
            endPoint = CIGlobals.SuitSpawnPoints[self.getHood()].keys()[endIndex]
            endPos = CIGlobals.SuitSpawnPoints[self.getHood()][endPoint]
            if self.moveIval:
                self.moveIval.finish()
                self.moveIval = None
            self.moveIval = LerpPosInterval(self, duration=3, pos=endPos, startPos=startPos, fluid=1)
        return

    def makeStateDict(self):
        self.stateIndex2suitState = {0: self.suitFSM.getStateNamed('off'),
         1: self.suitFSM.getStateNamed('walking'),
         2: self.suitFSM.getStateNamed('flyingDown'),
         3: self.suitFSM.getStateNamed('flyingUp'),
         4: self.suitFSM.getStateNamed('lured')}
        self.suitState2stateIndex = {}
        for stateId, state in self.stateIndex2suitState.items():
            self.suitState2stateIndex[state.getName()] = stateId

    def setSuitState(self, index, startPoint, endPoint, timestamp = None):
        if timestamp != None:
            ts = globalClockDelta.localElapsedTime(timestamp)
        else:
            ts = 0.0
        self.suitState = self.stateIndex2suitState[index]
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.suitFSM.request(self.suitState, [startPoint, endPoint, ts])
        return

    def getSuitState(self):
        return self.suitState

    def setAnimState(self, anim, timestamp = None):
        prevAnim = self.anim
        self.anim = anim
        if timestamp == None:
            ts = 0.0
        else:
            ts = globalClockDelta.localElapsedTime(timestamp)
        if type(anim) == types.IntType:
            if anim != 44 and anim != 45:
                anim = SuitGlobals.getAnimById(anim)
                animName = anim.getName()
            elif anim == 44:
                animName = 'die'
            elif anim == 45:
                animName = 'flyNeutral'
        elif type(anim) == types.StringType:
            animName = anim
        if self.animFSM.hasStateNamed(animName):
            self.animFSM.request(animName, [ts])
        else:
            self.loop(animName)
        messenger.send(SuitGlobals.animStateChangeEvent % self.uniqueName, [anim, prevAnim])
        return

    def doAttack(self, attackId, avId, timestamp = None):
        if timestamp == None:
            ts = 0.0
        else:
            ts = globalClockDelta.localElapsedTime(timestamp)
        attackName = SuitAttacks.SuitAttackLengths.keys()[attackId]
        attackTaunt = CIGlobals.SuitAttackTaunts[attackName][random.randint(0, len(CIGlobals.SuitAttackTaunts[attackName]) - 1)]
        avatar = self.cr.doId2do.get(avId)
        self.setChat(attackTaunt)
        self.animFSM.request('attack', [attackName, avatar, ts])
        return

    def throwObject(self):
        self.acceptOnce('enter' + self.wsnp.node().getName(), self.__handleWeaponCollision)
        Suit.throwObject(self)

    def __handleWeaponCollision(self, entry):
        self.sendUpdate('toonHitByWeapon', [self.attack, base.localAvatar.doId])
        base.localAvatar.handleHitByWeapon(self.attack, self)
        self.b_handleWeaponTouch()

    def b_handleWeaponTouch(self):
        self.sendUpdate('handleWeaponTouch', [])
        self.handleWeaponTouch()

    def announceGenerate(self):
        DistributedAvatar.announceGenerate(self)
        self.setAnimState('neutral')

    def generate(self):
        DistributedAvatar.generate(self)
        DistributedSmoothNode.generate(self)
        self.startSmooth()

    def disable(self):
        self.stopSmooth()
        self.anim = None
        self.state = None
        self.dept = None
        self.variant = None
        self.suitPlan = None
        if self.moveIval:
            self.moveIval.pause()
            self.moveIval = None
        Suit.disable(self)
        DistributedAvatar.disable(self)
        return

    def delete(self):
        Suit.delete(self)
        del self.anim
        del self.state
        del self.dept
        del self.variant
        del self.suitPlan
        del self.moveIval
        DistributedAvatar.delete(self)
        DistributedSmoothNode.delete(self)