# Embedded file name: lib.coginvasion.toon.LocalToon
"""
  
  Filename: LocalToon.py
  Created by: blach (30Nov14)
  
"""
from panda3d.core import *
from lib.coginvasion.globals import CIGlobals
from direct.controls import ControlManager
from direct.controls.GhostWalker import GhostWalker
from direct.controls.GravityWalker import GravityWalker
from direct.controls.ObserverWalker import ObserverWalker
from direct.controls.PhysicsWalker import PhysicsWalker
from direct.controls.SwimWalker import SwimWalker
from direct.controls.TwoDWalker import TwoDWalker
from DistributedToon import DistributedToon
from SmartCamera import SmartCamera
from lib.coginvasion.gui.ChatInput import ChatInput
from lib.coginvasion.gui.LaffOMeter import LaffOMeter
from lib.coginvasion.gui.MoneyGui import MoneyGui
from lib.coginvasion.gui.PieGui import PieGui
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from lib.coginvasion.hood import ZoneUtil

class LocalToon(DistributedToon):
    tntMaxDistance = 20.0
    neverDisable = 1

    def __init__(self, cr):
        try:
            self.LocalToon_initialized
            return
        except:
            self.LocalToon_initialized = 1

        DistributedToon.__init__(self, cr)
        self.avatarChoice = cr.localAvChoice
        self.smartCamera = SmartCamera()
        self.chatInput = ChatInput()
        self.moneyGui = MoneyGui()
        self.pieGui = PieGui(self.pies)
        self.laffMeter = LaffOMeter()
        self.runSfx = base.loadSfx('phase_3.5/audio/sfx/AV_footstep_runloop.wav')
        self.runSfx.setLoop(True)
        self.walkSfx = base.loadSfx('phase_3.5/audio/sfx/AV_footstep_walkloop.wav')
        self.walkSfx.setLoop(True)
        self.controlManager = ControlManager.ControlManager(True, False)
        self.offset = 3.2375
        self.movementKeymap = {'forward': 0,
         'backward': 0,
         'left': 0,
         'right': 0,
         'jump': 0}
        self.avatarMovementEnabled = False
        self.isMoving_forward = False
        self.isMoving_side = False
        self.isMoving_back = False
        self.isMoving_jump = False
        self.weaponType = None
        self.pieType = None
        self.pieThrowBtn = None
        base.cTrav = CollisionTraverser()
        return

    def ghostOn(self):
        self.getGeomNode().setTransparency(1)
        self.getGeomNode().setColorScale(1, 1, 1, 0.25)

    def ghostOff(self):
        self.getGeomNode().setColorScale(1, 1, 1, 1)
        self.getGeomNode().setTransparency(0)

    def enterReadBook(self, ts = 0, callback = None, extraArgs = []):
        self.stopLookAround()
        self.b_lookAtObject(0, -45, 0)
        DistributedToon.enterReadBook(self, ts, callback, extraArgs)

    def exitReadBook(self):
        DistributedToon.exitReadBook(self)
        self.startLookAround()

    def getAirborneHeight(self):
        return self.offset + 0.025

    def setupControls(self):
        self.walkControls = GravityWalker(legacyLifter=False)
        self.walkControls.setWallBitMask(CIGlobals.WallBitmask)
        self.walkControls.setFloorBitMask(CIGlobals.FloorBitmask)
        self.walkControls.setWalkSpeed(CIGlobals.ToonForwardSpeed, CIGlobals.ToonJumpForce, CIGlobals.ToonReverseSpeed, CIGlobals.ToonRotateSpeed)
        self.walkControls.initializeCollisions(base.cTrav, self, floorOffset=0.025, reach=4.0)
        self.walkControls.setAirborneHeightFunc(self.getAirborneHeight)

    def setWalkSpeedNormal(self):
        self.walkControls.setWalkSpeed(CIGlobals.ToonForwardSpeed, CIGlobals.ToonJumpForce, CIGlobals.ToonReverseSpeed, CIGlobals.ToonRotateSpeed)

    def setWalkSpeedSlow(self):
        self.walkControls.setWalkSpeed(CIGlobals.ToonForwardSlowSpeed, CIGlobals.ToonJumpSlowForce, CIGlobals.ToonReverseSlowSpeed, CIGlobals.ToonRotateSlowSpeed)

    def setupCamera(self):
        base.camLens.setMinFov(CIGlobals.DefaultCameraFov / (4.0 / 3.0))
        base.camLens.setNearFar(CIGlobals.DefaultCameraNear, CIGlobals.DefaultCameraFar)
        camHeight = max(self.getHeight(), 3.0)
        heightScaleFactor = camHeight * 0.3333333333
        defLookAt = Point3(0.0, 1.5, camHeight)
        camPos = (Point3(0.0, -9.0 * heightScaleFactor, camHeight),
         defLookAt,
         Point3(0.0, camHeight, camHeight * 4.0),
         Point3(0.0, camHeight, camHeight * -1.0),
         0)
        self.smartCamera.set_default_pos(camPos)
        self.smartCamera.set_parent(self)

    def setDNAStrand(self, dnaStrand):
        DistributedToon.setDNAStrand(self, dnaStrand)
        self.initCollisions()
        self.setupCamera()

    def setMoney(self, money):
        DistributedToon.setMoney(self, money)
        self.moneyGui.update()

    def setGagAmmo(self, ammoList):
        DistributedToon.setGagAmmo(self, ammoList)
        self.pieGui.update()

    def setupNameTag(self, tempName = None):
        DistributedToon.setupNameTag(self, tempName)
        if self.tag:
            self.tag['text_fg'] = CIGlobals.LocalNameTagColor

    def d_broadcastPositionNow(self):
        self.d_clearSmoothing()
        self.d_broadcastPosHpr()

    def b_setAnimState(self, anim, callback = None, extraArgs = []):
        if self.anim != anim:
            self.d_setAnimState(anim)
            DistributedToon.setAnimState(self, anim, callback=callback, extraArgs=extraArgs)

    def attachCamera(self):
        self.smartCamera.initialize_smartcamera()

    def startSmartCamera(self):
        self.smartCamera.initialize_smartcamera_collisions()
        self.smartCamera.start_smartcamera()

    def resetSmartCamera(self):
        self.stopSmartCamera()
        self.startSmartCamera()

    def stopSmartCamera(self):
        self.smartCamera.stop_smartcamera()

    def detachCamera(self):
        camera.reparentTo(render)
        camera.setPos(0, 0, 0)
        camera.setHpr(0, 0, 0)

    def enableAvatarControls(self):
        self.walkControls.enableAvatarControls()
        self.accept('arrow_up', self.updateMovementKeymap, ['forward', 1])
        self.accept('arrow_up-up', self.updateMovementKeymap, ['forward', 0])
        self.accept('arrow_down', self.updateMovementKeymap, ['backward', 1])
        self.accept('arrow_down-up', self.updateMovementKeymap, ['backward', 0])
        self.accept('arrow_left', self.updateMovementKeymap, ['left', 1])
        self.accept('arrow_left-up', self.updateMovementKeymap, ['left', 0])
        self.accept('arrow_right', self.updateMovementKeymap, ['right', 1])
        self.accept('arrow_right-up', self.updateMovementKeymap, ['right', 0])
        self.accept('control', self.updateMovementKeymap, ['jump', 1])
        self.accept('control-up', self.updateMovementKeymap, ['jump', 0])
        taskMgr.add(self.movementTask, 'avatarMovementTask')
        self.avatarMovementEnabled = True
        self.playMovementSfx(None)
        return

    def disableAvatarControls(self):
        self.walkControls.disableAvatarControls()
        self.ignore('arrow_up')
        self.ignore('arrow_up-up')
        self.ignore('arrow_down')
        self.ignore('arrow_down-up')
        self.ignore('arrow_left')
        self.ignore('arrow_left-up')
        self.ignore('arrow_right')
        self.ignore('arrow_right-up')
        self.ignore('control')
        self.ignore('control-up')
        taskMgr.remove('avatarMovementTask')
        self.isMoving_forward = False
        self.isMoving_side = False
        self.isMoving_back = False
        self.isMoving_jump = False
        self.avatarMovementEnabled = False
        self.playMovementSfx(None)
        for k, v in self.movementKeymap.items():
            self.updateMovementKeymap(k, 0)

        return

    def updateMovementKeymap(self, key, value):
        self.movementKeymap[key] = value

    def getMovementKeyValue(self, key):
        return self.movementKeymap[key]

    def playMovementSfx(self, movement):
        if movement == 'run':
            self.walkSfx.stop()
            self.runSfx.play()
        elif movement == 'walk':
            self.runSfx.stop()
            self.walkSfx.play()
        else:
            self.runSfx.stop()
            self.walkSfx.stop()

    def __forward(self):
        self.resetHeadHpr()
        self.stopLookAround()
        self.playMovementSfx('run')
        self.b_setAnimState('run')
        self.isMoving_side = False
        self.isMoving_back = False
        self.isMoving_forward = True
        self.isMoving_jump = False

    def __turn(self):
        self.resetHeadHpr()
        self.stopLookAround()
        self.playMovementSfx('walk')
        self.setPlayRate(1.0, 'walk')
        self.b_setAnimState('walk')
        self.isMoving_forward = False
        self.isMoving_back = False
        self.isMoving_side = True
        self.isMoving_jump = False

    def __reverse(self):
        self.resetHeadHpr()
        self.stopLookAround()
        self.playMovementSfx('walk')
        self.setPlayRate(-1.0, 'walk')
        self.b_setAnimState('walk')
        self.isMoving_side = False
        self.isMoving_forward = False
        self.isMoving_back = True
        self.isMoving_jump = False

    def __jump(self):
        self.playMovementSfx(None)
        if self.isMoving_forward or self.isMoving_side or self.isMoving_back:
            self.b_setAnimState('leap')
        else:
            self.b_setAnimState('jump')
        self.isMoving_side = False
        self.isMoving_forward = False
        self.isMoving_back = False
        self.isMoving_jump = True
        return

    def __neutral(self):
        self.resetHeadHpr()
        self.startLookAround()
        self.playMovementSfx(None)
        self.b_setAnimState('neutral')
        self.isMoving_side = False
        self.isMoving_forward = False
        self.isMoving_back = False
        self.isMoving_jump = False
        return

    def movementTask(self, task):
        if self.getMovementKeyValue('jump') == 1:
            if not self.isMoving_jump:
                if not self.walkControls.isAirborne:
                    if self.walkControls.mayJump:
                        self.__jump()
                    elif self.getMovementKeyValue('forward') == 1:
                        if not self.isMoving_forward:
                            self.__forward()
                    elif self.getMovementKeyValue('backward') == 1:
                        if not self.isMoving_back:
                            self.__reverse()
                    elif self.getMovementKeyValue('left') == 1 or self.getMovementKeyValue('right') == 1:
                        if not self.isMoving_side:
                            self.__turn()
                    elif self.isMoving_side or self.isMoving_forward or self.isMoving_back:
                        self.__neutral()
        elif self.getMovementKeyValue('forward') == 1:
            if not self.isMoving_forward:
                if not self.walkControls.isAirborne:
                    self.__forward()
        elif self.getMovementKeyValue('backward') == 1:
            if not self.isMoving_back:
                if not self.walkControls.isAirborne:
                    self.__reverse()
        elif self.getMovementKeyValue('left') == 1 or self.getMovementKeyValue('right') == 1:
            if not self.isMoving_side:
                if not self.walkControls.isAirborne:
                    self.__turn()
        elif self.isMoving_side or self.isMoving_forward or self.isMoving_back or self.isMoving_jump:
            if not self.walkControls.isAirborne:
                self.__neutral()
        return task.cont

    def createLaffMeter(self):
        r, g, b, a = self.getHeadColor()
        animal = self.getAnimal()
        maxHp = self.getMaxHealth()
        hp = self.getHealth()
        self.laffMeter.generate(r, g, b, animal, maxHP=maxHp, initialHP=hp)
        self.laffMeter.start()

    def disableLaffMeter(self):
        self.laffMeter.stop()
        self.laffMeter.disable()

    def deleteLaffMeter(self):
        self.laffMeter.delete()

    def enablePies(self, andKeys = 0):
        if self.avatarMovementEnabled and andKeys:
            self.enablePieKeys()
        self.pieGui.createGui()
        self.pieGui.setWeapon(self.pies.getPieTypeName(), playSound=False)

    def enablePieKeys(self):
        if self.weaponType == 'pie':
            if self.pieThrowBtn:
                self.pieThrowBtn.bind(DGG.B1PRESS, self.startPie)
                self.pieThrowBtn.bind(DGG.B1RELEASE, self.throwPie)
            self.accept('delete', self.startPie)
            self.accept('delete-up', self.throwPie)
        elif self.weaponType == 'tnt':
            if self.pies.tnt_state == 'ready':
                if self.pieThrowBtn:
                    self.pieThrowBtn.bind(DGG.B1RELEASE, self.startTNT)
                self.acceptOnce('delete', self.startTNT)

    def disablePieKeys(self):
        if self.pieThrowBtn:
            self.pieThrowBtn.unbind(DGG.B1PRESS)
            self.pieThrowBtn.unbind(DGG.B1RELEASE)
        self.ignore('delete')
        self.ignore('delete-up')

    def disablePies(self):
        self.disablePieKeys()
        self.pieGui.deleteGui()

    def setWeaponType(self, weaponType):
        enableKeysAgain = 0
        if weaponType != self.weaponType:
            enableKeysAgain = 1
        self.weaponType = weaponType
        if enableKeysAgain:
            self.disablePieKeys()
            self.enablePieKeys()

    def startTNT(self, foo = None):
        if self.pies.getAmmo() > 0:
            if self.pieThrowBtn:
                self.pieThrowBtn.unbind(DGG.B1RELEASE)
            self.resetHeadHpr()
            self.b_tntStart()
            Sequence(Wait(1.5), Func(self.releaseTNT)).start()

    def releaseTNT(self):
        if self.pies.getAmmo() > 0:
            self.b_tntRelease()
            self.pies.tntCollisions()
            self.acceptOnce('tntSensor-into', self.handleTntCollisions)

    def handleTntCollisions(self, entry):
        if not self.pies.tnt:
            return
        self.b_tntHitGround()
        x, y, z = self.pies.tnt.getPos(render)
        self.sendUpdate('setTntPos', [x, y, z])
        Sequence(Wait(2), Func(self.explodeTNT)).start()

    def explodeTNT(self):
        if not self.pies.tnt:
            return
        for obj in self.cr.doId2do.values():
            if obj.__class__.__name__ == 'DistributedSuit':
                if obj.getPlace() == self.zoneId:
                    if obj.getDistance(self.pies.tnt) <= self.tntMaxDistance:
                        self.sendUpdate('suitHitByPie', [obj.doId, 3])
                        Sequence(Wait(0.1), Func(self.checkSuitHealth, obj)).start()

        self.b_tntExplode()

    def createMoney(self):
        self.moneyGui.createGui()
        self.moneyGui.update()

    def handleMoneyChanged(self):
        self.moneyGui.update()

    def disableMoney(self):
        self.moneyGui.deleteGui()

    def resetHeadHpr(self):
        self.b_lookAtObject(0, 0, 0, blink=0)

    def startPie(self, foo = None):
        if self.pies.getAmmo() > 0:
            if self.pieThrowBtn:
                self.pieThrowBtn.unbind(DGG.B1PRESS)
            self.ignore('delete')
            self.pieType = self.pies.getPieType()
            self.resetHeadHpr()
            self.b_pieStart()
            self.pies.pieCollisions()

    def throwPie(self, foo = None):
        if self.pies.getAmmo() > 0:
            if self.pieThrowBtn:
                self.pieThrowBtn.unbind(DGG.B1RELEASE)
            self.ignore('delete-up')
            self.b_pieThrow()
            Sequence(Wait(0.75), Func(self.releasePie), Wait(0.3), Func(self.enablePieKeys)).start()

    def releasePie(self):
        if self.pies.getAmmo() > 0:
            self.acceptOnce('pieSensor-into', self.handlePieCollisions)
            self.b_pieRelease()

    def handlePieCollisions(self, entry):
        if self.pies.pie_state == 'start':
            return
        else:
            intoNP = entry.getIntoNodePath()
            avNP = intoNP.getParent()
            for key in self.cr.doId2do.keys():
                obj = self.cr.doId2do[key]
                if obj.__class__.__name__ == 'DistributedSuit':
                    if obj.getKey() == avNP.getKey():
                        if obj.getHealth() > 0:
                            self.sendUpdate('suitHitByPie', [obj.doId, self.pieType])
                elif obj.__class__.__name__ == 'DistributedToon':
                    if obj.getKey() == avNP.getKey():
                        if obj.getHealth() < obj.getMaxHealth() and not obj.isDead():
                            self.sendUpdate('toonHitByPie', [obj.doId, self.pieType])

            self.pieType = None
            self.b_pieSplat()
            return

    def checkSuitHealth(self, suit):
        if suit.getHealth() <= 0:
            self.sendUpdate('suitKilled', [suit.doId])

    def handleLookSpot(self, hpr):
        h, p, r = hpr
        self.d_lookAtObject(h, p, r, blink=1)

    def showPieButton(self):
        geom = CIGlobals.getDefaultBtnGeom()
        self.pieThrowBtn = DirectButton(geom=geom, geom_scale=(0.75, 1, 1), text='Throw Gag', text_scale=0.05, text_pos=(0, -0.01), relief=None, parent=base.a2dTopCenter, pos=(0, 0, -0.1))
        self.pieThrowBtn.setBin('gui-popup', 60)
        return

    def hidePieButton(self):
        self.pieThrowBtn.removeNode()
        self.pieThrowBtn = None
        return

    def showBookButton(self, inBook = 0):
        self.book_gui = loader.loadModel('phase_3.5/models/gui/sticker_open_close_gui.bam')
        self.book_btn = DirectButton(geom=(self.book_gui.find('**/BookIcon_CLSD'), self.book_gui.find('**/BookIcon_OPEN'), self.book_gui.find('**/BookIcon_RLVR')), relief=None, pos=(-0.175, 0, 0.163), command=self.bookButtonClicked, scale=(0.7, 0.8, 0.8), parent=base.a2dBottomRight)
        self.book_btn.setBin('gui-popup', 60)
        if inBook:
            self.book_btn['geom'] = (self.book_gui.find('**/BookIcon_OPEN'), self.book_gui.find('**/BookIcon_CLSD'), self.book_gui.find('**/BookIcon_RLVR2'))
            self.book_btn['command'] = self.bookButtonClicked
            self.book_btn['extraArgs'] = [0]
        return

    def hideBookButton(self):
        if hasattr(self, 'book_gui'):
            self.book_gui.removeNode()
            del self.book_gui
        if hasattr(self, 'book_btn'):
            self.book_btn.destroy()
            del self.book_btn

    def bookButtonClicked(self, openIt = 1):
        if openIt:
            base.cr.playGame.getPlace().fsm.request('shtickerBook')
        else:
            base.cr.playGame.getPlace().shtickerBookStateData.finished('resume')

    def handleHitByWeapon(self, attack, suit):
        taskMgr.remove('fallDone')
        if attack == 'canned':
            sfx = base.loadSfx('phase_5/audio/sfx/SA_canned_impact_only.mp3')
            SoundInterval(sfx).start()
        elif attack == 'playhardball':
            sfx = base.loadSfx('phase_5/audio/sfx/SA_hardball_impact_only_alt.mp3')
            SoundInterval(sfx).start()
        elif attack == 'clipontie':
            sfx = base.loadSfx('phase_5/audio/sfx/SA_powertie_impact.mp3')
            SoundInterval(sfx).start()
        self.b_lookAtObject(0, 0, 0, blink=1)
        self.cr.playGame.getPlace().fsm.request('stop')
        if not self.isDead():
            animToPlay = None
            timeToWait = 3.0
            if attack not in ('pickpocket', 'fountainpen'):
                suitH = suit.getH(render) % 360
                myH = self.getH(render) % 360
                if -90.0 <= suitH - myH <= 90.0:
                    animToPlay = 'fallFWD'
                else:
                    animToPlay = 'fallBCK'
            elif attack in ('pickpocket',):
                animToPlay = 'cringe'
            elif attack in ('fountainpen',):
                animToPlay = 'conked'
                timeToWait = 5.0
                self.getPart('head').setColorScale(0, 0, 0, 1)
                taskMgr.doMethodLater(3.0, self.resetHeadColor, 'resetHeadColorAfterFountainPen')
            self.b_setAnimState(animToPlay)
            taskMgr.doMethodLater(timeToWait, self.fallDone, 'fallDone')
        return

    def resetHeadColor(self, task):
        self.getPart('head').setColorScale(1, 1, 1, 1)
        return task.done

    def startMonitoringHP(self):
        taskMgr.add(self.monitorHealth, 'localToon-monitorHealth')

    def monitorHealth(self, task):
        if self.isDead():
            taskMgr.remove('fallDone')
            self.cr.playGame.getPlace().fsm.request('died', [{}, self.diedStateDone])
            return task.done
        return task.cont

    def stopMonitoringHP(self):
        taskMgr.remove('localToon-monitorHealth')

    def diedStateDone(self, requestStatus):
        zone = CIGlobals.RecoverAreaId
        doneStatus = {}
        doneStatus['mode'] = 'teleport'
        doneStatus['zoneId'] = zone
        doneStatus['hoodId'] = ZoneUtil.getHoodId(zone)
        doneStatus['where'] = ZoneUtil.getWhereName(zone)
        doneStatus['how'] = 'teleportIn'
        doneStatus['avId'] = base.localAvatar.doId
        doneStatus['shardId'] = None
        doneStatus['loader'] = ZoneUtil.getLoaderName(zone)
        self.cr.playGame.getPlace().doneStatus = doneStatus
        messenger.send(self.cr.playGame.getPlace().doneEvent)
        return

    def fallDone(self, task):
        self.cr.playGame.hood.loader.place.fsm.request('walk')
        self.b_setAnimState('neutral')
        return task.done

    def createChatInput(self):
        self.chatInput.load()
        self.chatInput.enter()

    def disableChatInput(self):
        self.chatInput.exit()
        self.chatInput.unload()

    def collisionsOn(self):
        self.controlManager.collisionsOn()

    def collisionsOff(self):
        self.controlManager.collisionsOff()

    def generate(self):
        DistributedToon.generate(self)

    def delete(self):
        DistributedToon.delete(self)
        self.deleteLaffMeter()

    def disable(self):
        self.stopMonitoringHP()
        taskMgr.remove('resetHeadColorAfterFountainPen')
        taskMgr.remove('fallDone')
        DistributedToon.disable(self)
        self.disableAvatarControls()
        self.disableLaffMeter()
        self.disablePies()
        self.disableChatInput()
        self.stopLookAround()
        self.weaponType = None
        self.pieType = None
        self.ignore('gotLookSpot')
        return

    def announceGenerate(self):
        DistributedToon.announceGenerate(self)
        self.setupControls()
        self.createChatInput()
        self.startLookAround()
        self.accept('gotLookSpot', self.handleLookSpot)

    def printAvPos(self):
        print self.getPos(render)