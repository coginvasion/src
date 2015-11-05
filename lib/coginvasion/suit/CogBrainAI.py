# Embedded file name: lib.coginvasion.suit.CogBrainAI
"""

  Filename: CogBrainAI.py
  Created by: blach (27Jan15)

  Description: This module represents the Cog's intelligence.

"""
from panda3d.core import *
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.showbase.DirectObject import DirectObject
from lib.coginvasion.globals import CIGlobals
import SuitPathFinder
import random

class CogBrain(DirectObject):
    PANIC_SPEED = 0.15
    PANIC_DELAY = 0.5
    RUNAWAY_SPEED = 0.1
    RUNAWAY_SAFE_DISTANCE = 50
    MAX_BOSS_HELPERS = 5
    PANIC_HP_FACTOR = 0.222
    ATTACK_DISTANCE = 40.0
    MAX_ATTACKERS = 3
    Difficulty2MaxAttackThrows = {}
    for level in range(1, 5):
        Difficulty2MaxAttackThrows[level] = 3

    for level in range(5, 10):
        Difficulty2MaxAttackThrows[level] = 4

    for level in range(9, 13):
        Difficulty2MaxAttackThrows[level] = 5

    def __init__(self, suit):
        self.suit = suit
        self.panicHP = self.suit.getMaxHealth() * self.PANIC_HP_FACTOR
        self.fsm = ClassicFSM('CogBrain', [State('off', self.enterOff, self.exitOff),
         State('neutral', self.enterNeutral, self.exitNeutral),
         State('followBoss', self.enterFollowBoss, self.exitFollowBoss),
         State('panic', self.enterPanic, self.exitPanic),
         State('runAway', self.enterRunAway, self.exitRunAway)], 'off', 'off')
        self.fsm.enterInitialState()

    def start(self):
        taskMgr.add(self.__think, self.suit.uniqueName('think'))

    def end(self, andGoOff = 1):
        taskMgr.remove(self.suit.uniqueName('think'))
        if andGoOff:
            self.fsm.request('off')

    def __think(self, task = None):
        if task:
            task.delayTime = 1
        if self.suit.getAttacking():
            if task:
                return task.again
            else:
                return
        _help_priority = 0
        _panic_priority = 0
        _run_priority = 0
        _helper_suits = 0
        boss = None
        for av in self.suit.getManager().suits.values():
            if av.doId != self.suit.doId:
                if av.head in ('vp',):
                    boss = av
                    for suit in self.suit.getManager().suits.values():
                        if suit.doId != self.suit.doId:
                            if suit.brain:
                                if suit.brain.fsm.getCurrentState().getName() == 'followBoss':
                                    _helper_suits += 1

        if _helper_suits == self.MAX_BOSS_HELPERS - 1:
            _help_priority = 2
        elif _helper_suits == self.MAX_BOSS_HELPERS - 2:
            _help_priority = 2.5
        elif _helper_suits == self.MAX_BOSS_HELPERS - 3:
            _help_priority = 3.5
        elif _helper_suits == self.MAX_BOSS_HELPERS - 4:
            _help_priority = 4
        elif _helper_suits == self.MAX_BOSS_HELPERS - 5:
            _help_priority = 4.5
        if boss == None or _helper_suits == self.MAX_BOSS_HELPERS:
            _help_priority = 0
        if self.fsm.getCurrentState().getName() == 'followBoss':
            if self.bossSpotKey != boss.boss.spot:
                self.fsm.request('followBoss', [boss])
                return task.again
        _toons_in_range = 0
        in_range = 15
        for av in self.suit.air.doId2do.values():
            if av.__class__.__name__ == 'DistributedToonAI':
                if av.zoneId == self.suit.zoneId:
                    if self.suit.getDistance(av) <= in_range:
                        _toons_in_range += 1

        if self.fsm.getCurrentState().getName() == 'followBoss':
            _panic_priority = _toons_in_range / 0.85
        else:
            _panic_priority = _toons_in_range / 0.75
        if self.fsm.getCurrentState().getName() == 'panic' and _toons_in_range > 0:
            _run_priority = 5
        if self.suit.getHealth() <= self.panicHP:
            if _panic_priority < 4:
                _panic_priority = 4
        if _run_priority == 5:
            self.fsm.request('runAway', [av])
            del _help_priority
            del _panic_priority
            del _run_priority
            del _helper_suits
            del boss
            del in_range
            del _toons_in_range
            try:
                del av
            except:
                pass

            if task:
                return task.done
            else:
                return
        elif _panic_priority <= 2 and _help_priority <= 2:
            state_num = random.randint(0, 2)
            if state_num == 0 or state_num == 1:
                new_state = 'neutral'
            else:
                new_state = 'followBoss'
            if boss == None or _help_priority == 0:
                if self.fsm.getCurrentState().getName() != 'neutral':
                    self.fsm.request('neutral')
            else:
                new_state = 'neutral'
                if self.fsm.getCurrentState().getName() != new_state:
                    if self.fsm.getCurrentState().getName() == 'followBoss':
                        del _help_priority
                        del _panic_priority
                        del _run_priority
                        del _helper_suits
                        del boss
                        del in_range
                        del _toons_in_range
                        try:
                            del args
                        except:
                            pass

                        try:
                            del new_state
                        except:
                            pass

                        try:
                            del state_num
                        except:
                            pass

                        try:
                            del av
                        except:
                            pass

                        if task:
                            return task.again
                        else:
                            return
                    args = []
                    if new_state == 'followBoss':
                        args = [boss]
                    self.fsm.request(new_state, args)
        elif _panic_priority > _help_priority:
            if self.fsm.getCurrentState().getName() != 'panic':
                self.fsm.request('panic')
                del _help_priority
                del _panic_priority
                del _run_priority
                del _helper_suits
                del boss
                del in_range
                del _toons_in_range
                try:
                    del args
                except:
                    pass

                try:
                    del new_state
                except:
                    pass

                try:
                    del state_num
                except:
                    pass

                try:
                    del av
                except:
                    pass

                if task:
                    return task.done
                else:
                    return
        elif _panic_priority < _help_priority:
            if self.fsm.getCurrentState().getName() != 'followBoss':
                self.fsm.request('followBoss', [boss])
        elif _panic_priority == _help_priority:
            new_state = random.choice(['panic', 'followBoss'])
            if self.fsm.getCurrentState().getName() != new_state:
                args = []
                if new_state == 'followBoss':
                    args = [boss]
                self.fsm.request(new_state, args)
        del _help_priority
        del _panic_priority
        del _run_priority
        del _helper_suits
        del boss
        del in_range
        del _toons_in_range
        try:
            del args
        except:
            pass

        try:
            del new_state
        except:
            pass

        try:
            del state_num
        except:
            pass

        try:
            del av
        except:
            pass

        if task:
            return task.again
        else:
            return

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterNeutral(self):
        self.suit.createPath(fromCurPos=True)
        self.numAttacksThrown = 0
        if not self.suit.isBackup():
            self.neutral_startLookingForToons()

    def neutral_startLookingForToons(self):
        taskMgr.add(self.__lookForToons, self.suit.uniqueName('lookForToon'))

    def neutral_stopLookingForToons(self):
        taskMgr.remove(self.suit.uniqueName('lookForToon'))

    def __lookForToons(self, task):
        if self.suit.isBackup() or not hasattr(self, 'numAttacksThrown'):
            return task.done
        elif self.suit.getAttacking():
            task.delayTime = 1.0
            return task.again
        elif self.numAttacksThrown >= self.Difficulty2MaxAttackThrows[self.suit.getLevel()]:
            self.numAttacksThrown = 0
            if not self.suit.isWalking():
                self.suit.createPath(path_key=self.suit.currentPath, fromCurPos=True)
            task.delayTime = 10
            return task.again
        else:
            closestToonOrTurret = None
            obj2range = {}
            for obj in base.air.doId2do.values():
                if obj.__class__.__name__ in ('DistributedToonAI', 'DistributedPieTurretAI'):
                    if obj.zoneId == self.suit.zoneId:
                        if not obj.isDead():
                            if obj.__class__.__name__ == 'DistributedToonAI':
                                if obj.getNumAttackers() < self.MAX_ATTACKERS:
                                    dist = obj.getDistance(self.suit)
                                    if dist <= self.ATTACK_DISTANCE:
                                        obj2range[obj] = dist
                            else:
                                dist = obj.getDistance(self.suit)
                                if dist <= self.ATTACK_DISTANCE:
                                    obj2range[obj] = dist

            ranges = []
            for distance in obj2range.values():
                ranges.append(distance)

            ranges.sort()
            for obj in obj2range.keys():
                distance = obj2range[obj]
                if distance == ranges[0]:
                    closestToonOrTurret = obj

            if closestToonOrTurret != None and not self.suit.getAttacking():
                if self.suit.head != 'vp':
                    if self.suit.walkTrack:
                        self.ignore(self.suit.walkTrack.getName())
                        self.suit.walkTrack.clearToInitial()
                        self.suit.walkTrack = None
                self.suit.b_setSuitState(3, -1, -1)
                self.suit.b_setAnimState('neutral')
                self.end(0)
                self.suit.headsUp(closestToonOrTurret)
                self.suit.attackToon(closestToonOrTurret)
                self.suit.setAttacking(True)
                if closestToonOrTurret.__class__.__name__ == 'DistributedToonAI':
                    closestToonOrTurret.addNewAttacker(self.suit.doId)
                self.numAttacksThrown += 1
                return task.done
            if self.numAttacksThrown > 0:
                if not self.suit.isWalking():
                    self.suit.createPath(path_key=self.suit.currentPath, fromCurPos=True)
            elif not self.suit.isWalking():
                self.suit.createPath(fromCurPos=True)
            self.numAttacksThrown = 0
            task.delayTime = 3.5
            return task.again

    def exitNeutral(self):
        self.neutral_stopLookingForToons()
        del self.numAttacksThrown

    def enterPanic(self):
        taskMgr.add(self.__panic, self.suit.uniqueName('panic'))

    def __panic(self, task):
        self.suit.createPath(durationFactor=self.PANIC_SPEED, fromCurPos=True)
        if task.time == 2.0:
            self.__think(None)
        task.delayTime = self.PANIC_DELAY
        return task.again

    def exitPanic(self):
        taskMgr.remove(self.suit.uniqueName('panic'))

    def enterFollowBoss(self, boss):
        self.boss = boss
        if boss.boss.spot == None:
            self.bossSpot = boss.getPos(render)
        else:
            self.bossSpot = CIGlobals.SuitSpawnPoints[self.suit.hood][boss.boss.spot]
        if self.suit.currentPath == boss.boss.spot:
            self.suit.createPath(path_key=boss.boss.spot, fromCurPos=True)
        else:
            self.suit.currentPathQueue = SuitPathFinder.find_path(self.suit.hood, self.suit.currentPath, boss.boss.spot)
            self.suit.currentPathQueue.remove(self.suit.currentPathQueue[0])
            self.suit.createPath(fromCurPos=True)
        taskMgr.add(self.__followBoss, self.suit.uniqueName('followBoss'))
        self.bossSpotKey = boss.boss.spot
        return

    def __followBoss(self, task):
        if self.boss not in self.suit.getManager().suits.values():
            self.fsm.request('neutral')
            return task.done
        elif self.suit.getDistance(self.boss) <= 4:
            self.suit.b_setSuitState(3, -1, -1)
            if self.suit.walkTrack:
                self.suit.ignore(self.suit.walkTrack.getDoneEvent())
                self.suit.walkTrack.pause()
                self.suit.walkTrack = None
                self.suit.b_setAnimState('neutral')
                self.suit.setH(self.suit.getH() - 180)
                self.suit.d_setH(self.suit.getH())
            return task.done
        else:
            return task.cont

    def exitFollowBoss(self):
        self.suit.resetPathQueue()
        taskMgr.remove(self.suit.uniqueName('followBoss'))
        del self.boss
        del self.bossSpot
        del self.bossSpotKey

    def enterRunAway(self, toon):
        self.toon = toon
        self.suit.createPath(durationFactor=self.RUNAWAY_SPEED, fromCurPos=True)
        taskMgr.add(self.__runAway, self.suit.uniqueName('runAway'))

    def __runAway(self, task):
        try:
            if self.suit.getDistance(self.toon) >= self.RUNAWAY_SAFE_DISTANCE:
                self.start()
                return task.done
            if self.suit.walkTrack == None or self.suit.walkTrack.isStopped():
                self.suit.createPath(durationFactor=self.RUNAWAY_SPEED, fromCurPos=True)
            return task.cont
        except:
            self.fsm.request('neutral')
            return task.done

        return

    def exitRunAway(self):
        taskMgr.remove(self.suit.uniqueName('runAway'))
        del self.toon