# Embedded file name: lib.coginvasion.cog.SuitHealBossBehavior
"""

  Filename: SuitHealBossBehavior.py
  Created by: DecodedLogic (20Sep15)

"""
from lib.coginvasion.cog.SuitHabitualBehavior import SuitHabitualBehavior
from lib.coginvasion.cog import SuitAttacks
from lib.coginvasion.globals import CIGlobals
from direct.interval.IntervalGlobal import Sequence, Wait, Func
from direct.distributed.ClockDelta import globalClockDelta
import random

class SuitHealBossBehavior(SuitHabitualBehavior):
    HEAL_SPEED = 50.0
    HEAL_DISTANCE = 20.0
    HEAL_COOLDOWN = 10.0

    def __init__(self, suit, boss):
        doneEvent = 'suit%s-healBoss' % suit.doId
        SuitHabitualBehavior.__init__(self, suit, doneEvent)
        self.boss = boss
        self.maxHeal = int(self.suit.getLevel() * 7)
        self.minHeal = int(self.suit.getLevel() * 2.5)
        self.suitHealTrack = None
        self.cooldownTrack = None
        self.canHeal = True
        return

    def __attemptToHealBoss(self, hp):
        if self.isBossAvailable():
            self.boss.b_setHealth(self.boss.getHealth() + hp)
            self.boss.d_announceHealth(1, hp)
            self.suit.d_handleWeaponTouch()

    def isBossAvailable(self):
        if not self.boss.isEmpty() and not hasattr(self.boss, 'DELETED') and not self.boss.isDead():
            return True
        return False

    def __disableBoss(self):
        if self.isBossAvailable():
            self.boss.getBrain().stopThinking()
            self.boss.b_setAnimState('neutral')

    def __enableBoss(self):
        if self.isBossAvailable():
            self.boss.getBrain().startThinking()

    def __toggleCanHeal(self):
        if self.canHeal:
            self.canHeal = False
        else:
            self.canHeal = True

    def enter(self):
        SuitHabitualBehavior.enter(self)
        self.__toggleCanHeal()
        attack = random.randint(0, 6)
        attackName = SuitAttacks.SuitAttackLengths.keys()[attack]
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.suit.sendUpdate('doAttack', [attack, self.boss.doId, timestamp])
        distance = self.suit.getDistance(self.boss)
        timeUntilHeal = distance / self.HEAL_SPEED
        timeUntilRelease = 1.0
        self.suit.d_setChat(CIGlobals.SuitHealTaunt)
        hp = random.randint(self.minHeal, self.maxHeal)
        if self.boss.getHealth() + hp > self.boss.getMaxHealth():
            hp = self.boss.getMaxHealth() - self.boss.getHealth()
        if attackName != 'glowerpower':
            if self.suit.suitPlan.getSuitType() == 'C':
                timeUntilRelease = 2.2
            else:
                timeUntilRelease = 3.0
        self.suitHealTrack = Sequence(Func(self.__disableBoss), Wait(timeUntilRelease + timeUntilHeal), Func(self.__attemptToHealBoss, hp), Func(self.__enableBoss), Func(self.exit))
        self.suitHealTrack.start()

    def exit(self):
        SuitHabitualBehavior.exit(self)
        if self.suitHealTrack:
            self.suitHealTrack.pause()
            self.suitHealTrack = None
        self.cooldownTrack = Sequence(Wait(self.HEAL_COOLDOWN), Func(self.__toggleCanHeal))
        self.cooldownTrack.start()
        return

    def shouldStart(self):
        SuitHabitualBehavior.shouldStart(self)
        if self.suit.getDistance(self.boss) <= self.HEAL_DISTANCE:
            if not hasattr(self.suit, 'DELETED') and not hasattr(self.boss, 'DELETED'):
                return self.canHeal
        return False

    def unload(self):
        SuitHabitualBehavior.unload(self)
        if self.suitHealTrack:
            self.suitHealTrack.pause()
            self.suitHealTrack = None
        if self.cooldownTrack:
            self.cooldownTrack.pause()
            self.cooldownTrack = None
        del self.suitHealTrack
        del self.cooldownTrack
        del self.maxHeal
        del self.minHeal
        del self.boss
        return