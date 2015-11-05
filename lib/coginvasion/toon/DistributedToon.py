# Embedded file name: lib.coginvasion.toon.DistributedToon
"""

  Filename: DistributedToon.py
  Created by: blach (17June14)
  
"""
from lib.coginvasion.globals import CIGlobals
from lib.coginvasion.online.OnlineGlobals import *
from direct.distributed.DistributedObject import DistributedObject
from lib.coginvasion.toon import Toon
from direct.distributed.DistributedSmoothNode import DistributedSmoothNode
from lib.coginvasion.avatar.DistributedAvatar import DistributedAvatar
from lib.coginvasion.toon.ChatBalloon import ChatBalloon
from lib.coginvasion.toon.LabelScaler import LabelScaler
from direct.gui.DirectGui import *
from direct.actor.Actor import Actor
from direct.interval.ProjectileInterval import ProjectileInterval
from direct.showbase.ShadowPlacer import ShadowPlacer
from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase import Audio3DManager
from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import *
from direct.distributed.DelayDeletable import DelayDeletable
from direct.distributed import DelayDelete
import random
notify = DirectNotify().newCategory('DistributedToon')

class DistributedToon(Toon.Toon, DistributedAvatar, DistributedSmoothNode, DelayDeletable):

    def __init__(self, cr):
        try:
            self.DistributedToon_initialized
            return
        except:
            self.DistributedToon_initialized = 1

        Toon.Toon.__init__(self, cr)
        DistributedAvatar.__init__(self, cr)
        DistributedSmoothNode.__init__(self, cr)
        self.token = -1
        self.ghost = 0

    def setGhost(self, value):
        self.ghost = value
        if value:
            self.ghostOn()
        else:
            self.ghostOff()

    def d_setGhost(self, value):
        self.sendUpdate('setGhost', [value])

    def b_setGhost(self, value):
        self.d_setGhost(value)
        self.setGhost(value)

    def getGhost(self):
        return self.ghost

    def setDNAStrand(self, dnaStrand):
        Toon.Toon.setDNAStrand(self, dnaStrand)

    def d_setDNAStrand(self, dnaStrand):
        self.sendUpdate('setDNAStrand', [dnaStrand])

    def b_setDNAStrand(self, dnaStrand):
        self.setDNAStrand(dnaStrand)
        self.d_setDNAStrand(dnaStrand)

    def lookAtObject(self, h, p, r, blink = 1):
        if self.getPart('head').getHpr() == (h, p, r):
            return
        Toon.Toon.lerpLookAt(self, self.getPart('head'), tuple((h, p, r)))
        if blink:
            maxBlinks = random.randint(1, 2)
            numBlinks = 0
            delay = 0
            for blink in range(maxBlinks):
                if numBlinks == 0:
                    taskMgr.add(self.doBlink, 'blinkOnTurn')
                else:
                    delay += 0.2
                    taskMgr.doMethodLater(delay, self.doBlink, 'doBlink')
                numBlinks += 1

    def b_lookAtObject(self, h, p, r, blink = 1):
        self.d_lookAtObject(h, p, r, blink)
        self.lookAtObject(h, p, r, blink)

    def d_lookAtObject(self, h, p, r, blink = 1):
        self.sendUpdate('lookAtObject', [h,
         p,
         r,
         blink])

    def setChat(self, chat):
        Toon.Toon.setChat(self, chat)

    def tntStart(self):
        self.pies.tntStart()

    def b_tntStart(self):
        self.sendUpdate('tntStart', [])
        self.tntStart()

    def tntRelease(self):
        self.pies.tntRelease()

    def b_tntRelease(self):
        self.sendUpdate('tntRelease', [])
        self.tntRelease()

    def tntHitGround(self):
        self.pies.handleTntHitGround()

    def b_tntHitGround(self):
        self.sendUpdate('tntHitGround', [])
        self.tntHitGround()

    def tntExplode(self):
        self.pies.tntExplode()

    def b_tntExplode(self):
        self.sendUpdate('tntExplode', [])
        self.tntExplode()

    def setTntPos(self, x, y, z):
        pos = Point3(x, y, z)
        self.pies.setTntPos(pos)

    def pieStart(self):
        self.pies.pieStart()

    def b_pieStart(self):
        self.sendUpdate('pieStart', [])
        self.pieStart()

    def pieThrow(self):
        self.pies.pieThrow()

    def b_pieThrow(self):
        self.sendUpdate('pieThrow', [])
        self.pieThrow()

    def pieRelease(self):
        self.pies.pieRelease()

    def b_pieRelease(self):
        self.sendUpdate('pieRelease', [])
        self.pieRelease()

    def pieSplat(self):
        self.pies.handlePieSplat()

    def b_pieSplat(self):
        self.sendUpdate('pieSplat', [])
        self.pieSplat()

    def setPieType(self, pietype):
        lastPieType = self.pies.getPieType()
        self.pies.setPieType(pietype)
        if self.pies.getPieType() == 3:
            self.attachTNT()
        elif lastPieType == 3:
            if self.pies.tnt_state != 'released':
                self.detachTNT()

    def b_setPieType(self, pietype):
        self.d_setPieType(pietype)
        self.setPieType(pietype)

    def d_setPieType(self, pietype):
        self.sendUpdate('setPieType', [pietype])

    def setGagAmmo(self, ammoList):
        bdayAmmo = ammoList[0]
        tartAmmo = ammoList[1]
        sliceAmmo = ammoList[2]
        if len(ammoList) > 3:
            tntAmmo = ammoList[3]
            self.pies.setAmmo(tntAmmo, 3)
        self.pies.setAmmo(tartAmmo, 1)
        self.pies.setAmmo(bdayAmmo, 0)
        self.pies.setAmmo(sliceAmmo, 2)

    def setMoney(self, money):
        self.money = money

    def getMoney(self):
        return self.money

    def setAdminToken(self, value):
        self.token = value
        if value > -1:
            Toon.Toon.setAdminToken(self, value)
        else:
            Toon.Toon.removeAdminToken(self)

    def getAdminToken(self):
        return self.token

    def setAnimState(self, anim, timestamp = None, callback = None, extraArgs = []):
        self.anim = anim
        if timestamp == None:
            ts = 0.0
        else:
            ts = globalClockDelta.localElapsedTime(timestamp)
        if self.animFSM.getStateNamed(anim):
            self.animFSM.request(anim, [ts, callback, extraArgs])
        return

    def b_setAnimState(self, anim):
        self.d_setAnimState(anim)
        self.setAnimState(anim, None)
        return

    def d_setAnimState(self, anim):
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.sendUpdate('setAnimState', [anim, timestamp])

    def getAnimState(self):
        return self.anim

    def setName(self, name):
        Toon.Toon.setName(self, name)
        if self.cr.isShowingPlayerIds:
            self.showAvId()

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.d_setName(name)
        self.setName(name)

    def showAvId(self):
        self.setDisplayName(self.getName() + '\n' + str(self.doId))

    def showName(self):
        self.setDisplayName(self.getName())

    def setDisplayName(self, name):
        self.setupNameTag(tempName=name)

    def wrtReparentTo(self, parent):
        DistributedSmoothNode.wrtReparentTo(self, parent)

    def announceHealthAndPlaySound(self, level, hp):
        DistributedAvatar.announceHealth(self, level, hp)
        hpSfx = self.audio3d.loadSfx('phase_11/audio/sfx/LB_toonup.mp3')
        self.audio3d.attachSoundToObject(hpSfx, self)
        SoundInterval(hpSfx).start()
        del hpSfx

    def announceGenerate(self):
        DistributedAvatar.announceGenerate(self)
        if self.animFSM.getCurrentState().getName() == 'off':
            self.setAnimState('neutral')
        self.startBlink()

    def generate(self):
        DistributedAvatar.generate(self)
        DistributedSmoothNode.generate(self)
        self.startSmooth()

    def disable(self):
        if self.track != None:
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        self.stopBlink()
        self.ignore('showAvId')
        self.ignore('showName')
        self.token = None
        Toon.Toon.disable(self)
        DistributedAvatar.disable(self)
        return

    def delete(self):
        try:
            self.DistributedToon_deleted
        except:
            self.DistributedToon_deleted = 1
            self.stopSmooth()
            Toon.Toon.delete(self)
            DistributedAvatar.delete(self)
            DistributedSmoothNode.delete(self)