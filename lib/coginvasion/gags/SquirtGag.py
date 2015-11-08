# Embedded file name: lib.coginvasion.gags.SquirtGag
"""

  Filename: SquirtGag.py
  Created by: DecodedLogic (10Jul15)

"""
from lib.coginvasion.gags import GagGlobals
from lib.coginvasion.gags.Gag import Gag
from lib.coginvasion.gags.GagType import GagType
from lib.coginvasion.globals import CIGlobals
from direct.interval.IntervalGlobal import Sequence, Func, Wait, LerpScaleInterval, Parallel
from direct.interval.ActorInterval import ActorInterval
from panda3d.core import Point3, Vec3, NodePath, CollisionSphere, CollisionHandlerEvent, CollisionNode
import abc

class SquirtGag(Gag):

    def __init__(self, name, model, damage, hitSfx, spraySfx, missSfx, toonAnim, enableReleaseFrame, completeSquirtFrame, startAnimFrame = 0, scale = 1, playRate = 1):
        Gag.__init__(self, name, model, damage, GagType.SQUIRT, hitSfx, scale=scale, autoRelease=True, playRate=playRate)
        self.sprayScale = GagGlobals.splatSizes.get(self.name)
        self.spraySfx = None
        self.missSfx = None
        self.origin = None
        self.sprayRange = None
        self.spray = None
        self.sprayJoint = None
        self.canSquirt = False
        self.hitSomething = False
        self.toonAnim = toonAnim
        self.startAnimFrame = 0
        self.enableReleaseFrame = enableReleaseFrame
        self.completeSquirtFrame = completeSquirtFrame
        self.lastFrame = 0
        if game.process == 'client':
            if spraySfx:
                self.spraySfx = base.audio3d.loadSfx(spraySfx)
            if missSfx:
                self.missSfx = base.audio3d.loadSfx(missSfx)
        return

    def start(self):
        Gag.start(self)
        if self.anim:
            self.build()
            self.equip()
            duration = base.localAvatar.getDuration(self.anim, toFrame=self.enableReleaseFrame)
            Parallel(ActorInterval(self.avatar, self.anim, startFrame=self.startAnimFrame, endFrame=self.enableReleaseFrame, playRate=self.playRate), Wait(duration - 0.15), Func(self.setSquirtEnabled, True)).start()

    def startSquirt(self, sprayScale, containerHold):

        def startSpray():
            self.doSpray(sprayScale, containerHold, sprayScale)

        Sequence(ActorInterval(self.avatar, self.toonAnim, startFrame=self.enableReleaseFrame, endFrame=self.completeSquirtFrame), Func(startSpray)).start()

    def setSquirtEnabled(self, flag):
        self.canSquirt = flag

    def doSpray(self, scaleUp, scaleDown, hold):
        base.audio3d.attachSoundToObject(self.spraySfx, self.gag)
        self.spraySfx.play()
        spraySequence = Sequence(Func(self.getSprayTrack(self.origin, self.sprayRange, scaleUp, hold, scaleDown).start))
        sprayParallel = Parallel()
        sprayParallel.append(Func(spraySequence.start))
        sprayParallel.start()

    def completeSquirt(self):
        numFrames = base.localAvatar.getNumFrames(self.toonAnim)
        finishSeq = Sequence()
        finishSeq.append(Wait(0.5))
        finishSeq.append(Func(self.avatar.play, self.toonAnim, fromFrame=self.completeSquirtFrame, toFrame=numFrames))
        finishSeq.append(Func(self.reset))
        finishSeq.append(Func(self.avatar.play, 'neutral'))
        finishSeq.append(Func(self.cleanupSpray))
        finishSeq.start()
        if self.avatar == base.localAvatar:
            base.localAvatar.enablePieKeys()
            if base.localAvatar.getBackpack().getSupply() == 0:
                self.cleanupGag()

    def onCollision(self, entry):
        self.hitSomething = True
        base.audio3d.attachSoundToObject(self.hitSfx, self.sprayNP)
        self.hitSfx.play()
        intoNP = entry.getIntoNodePath()
        avNP = intoNP.getParent()
        if self.avatar.doId == base.localAvatar.doId:
            for key in base.cr.doId2do.keys():
                obj = base.cr.doId2do[key]
                if obj.__class__.__name__ == 'DistributedSuit':
                    if obj.getKey() == avNP.getKey():
                        self.avatar.sendUpdate('suitHitByPie', [obj.doId, self.getID()])
                elif obj.__class__.__name__ == 'DistributedToon':
                    if obj.getKey() == avNP.getKey():
                        if obj.getHealth() < obj.getMaxHealth():
                            self.avatar.sendUpdate('toonHitByPie', [obj.doId, self.getID()])

        if base.localAvatar == self.avatar:
            self.splatPos = self.sprayNP.getPos(render)
            gagPos = self.sprayNP.getPos(render)
            self.handleSplat()
            self.avatar.sendUpdate('setSplatPos', [self.getID(),
             gagPos.getX(),
             gagPos.getY(),
             gagPos.getZ()])

    def handleMiss(self):
        if self.spray and self.hitSomething == False:
            base.audio3d.attachSoundToObject(self.missSfx, self.spray)
            self.missSfx.play()
            self.cleanupSpray()

    def handleSplat(self):
        self.cleanupSplat()
        self.buildSplat(GagGlobals.splatSizes.get(self.getName()), GagGlobals.WATER_SPRAY_COLOR)
        self.splat.setPos(self.splatPos)
        self.splat.reparentTo(render)
        self.splatPos = None
        taskMgr.doMethodLater(0.5, self.delSplat, 'Delete Splat')
        return

    def getSprayTrack(self, origin, target, scaleUp, hold, scaleDown, horizScale = 1.0, vertScale = 1.0):
        base.localAvatar.stop(self.toonAnim)
        self.lastFrame = self.avatar.getCurrentFrame(self.toonAnim)
        track = Sequence()
        sprayProp = loader.loadModel(GagGlobals.SPRAY_MDL)
        sprayProp.setTwoSided(1)
        sprayScale = hidden.attachNewNode('spray-parent')
        sprayRot = hidden.attachNewNode('spray-rotate')
        sprayRot.setColor(GagGlobals.WATER_SPRAY_COLOR)
        sprayRot.setTransparency(1)
        collNode = CollisionNode('Collision')
        spraySphere = CollisionSphere(0, 0, 0, 1)
        spraySphere.setTangible(0)
        collNode.addSolid(spraySphere)
        collNode.setCollideMask(CIGlobals.WallBitmask)
        sprayNP = sprayRot.attachNewNode(collNode)
        sprayNP.setY(1)
        self.sprayNP = sprayNP
        event = CollisionHandlerEvent()
        event.set_in_pattern('%fn-into')
        event.set_out_pattern('%fn-out')
        base.cTrav.add_collider(sprayNP, event)
        self.avatar.acceptOnce(sprayNP.node().getName() + '-into', self.onCollision)

        def showSpray(sprayScale, sprayProp, origin, target):
            objects = [sprayRot, sprayScale, sprayProp]
            for item in objects:
                index = objects.index(item)
                if index == 0:
                    item.reparentTo(self.sprayJoint)
                    item.setPos(self.sprayJoint.getPos(render))
                    item.setHpr(self.sprayJoint.getHpr(render))
                    item.setP(0)
                else:
                    item.reparentTo(objects[index - 1])
                item.clearMat()

        track.append(Func(showSpray, sprayScale, sprayProp, origin, target))
        self.spray = sprayRot

        def calcTargetScale():
            distance = Vec3(target - origin).length()
            yScale = distance / GagGlobals.SPRAY_LEN
            targetScale = Point3(yScale * horizScale, yScale, yScale * vertScale)
            return targetScale

        track.append(Parallel(LerpScaleInterval(sprayScale, scaleUp, calcTargetScale, startScale=GagGlobals.PNT3NEAR0), sprayNP.posInterval(0.25, self.spray.getPos(render) + Point3(0, 50, 0), startPos=self.spray.getPos(render) + Point3(0, 5, 0))))
        track.append(Wait(hold))
        track.append(Func(self.handleMiss))
        track.append(LerpScaleInterval(sprayScale, 0.75, GagGlobals.PNT3NEAR0))

        def hideSpray():
            (lambda prop: prop.removeNode(), [sprayProp, sprayRot, sprayScale])

        track.append(Func(hideSpray))
        track.append(Func(self.completeSquirt))
        return track

    def getSprayRange(self):
        sprayRange = NodePath('Squirt Range')
        sprayRange.reparentTo(self.avatar)
        sprayRange.setScale(render, 1)
        sprayRange.setPos(0, 160, -90)
        sprayRange.setHpr(90, -90, 90)
        return sprayRange

    @abc.abstractmethod
    def getSprayStartPos(self):
        return Point3(0, 0, 0)

    def cleanupSpray(self):
        if self.spray:
            self.spray.removeNode()
            self.spray = None
        self.hitSomething = False
        self.canSquirt = False
        return