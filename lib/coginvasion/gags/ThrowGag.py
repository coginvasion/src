# Embedded file name: lib.coginvasion.gags.ThrowGag
"""

  Filename: ThrowGag.py
  Created by: DecodedLogic (07Jul15)

"""
from panda3d.core import CollisionSphere, BitMask32, CollisionNode, NodePath, CollisionHandlerEvent
from direct.interval.ProjectileInterval import ProjectileInterval
from lib.coginvasion.gags.Gag import Gag
from lib.coginvasion.gags.GagType import GagType
from lib.coginvasion.globals import CIGlobals
from direct.actor.Actor import Actor
import GagGlobals

class ThrowGag(Gag):

    def __init__(self, name, model, damage, hitSfx, splatColor, anim = None, scale = 1):
        Gag.__init__(self, name, model, damage, GagType.THROW, hitSfx, anim=anim, scale=scale)
        self.splatScale = GagGlobals.splatSizes[self.name]
        self.splatColor = splatColor
        self.entities = []

    def build(self):
        if not self.gag:
            Gag.build(self)
            self.equip()
            if self.anim and self.gag:
                self.gag.loop('chan')
        return self.gag

    def start(self):
        super(ThrowGag, self).start()
        self.build()
        self.avatar.setPlayRate(self.playRate, 'pie')
        self.avatar.play('pie', fromFrame=0, toFrame=45)

    def throw(self):
        self.avatar.play('pie', fromFrame=45, toFrame=90)
        if not self.gag:
            self.build()

    def release(self):
        Gag.release(self)
        base.audio3d.attachSoundToObject(self.woosh, self.gag)
        self.woosh.play()
        throwPath = NodePath('ThrowPath')
        throwPath.reparentTo(self.avatar)
        throwPath.setScale(render, 1)
        throwPath.setPos(0, 160, -90)
        throwPath.setHpr(90, -90, 90)
        entity = self.gag
        if not entity:
            entity = self.build()
        entity.wrtReparentTo(render)
        entity.setHpr(throwPath.getHpr(render))
        self.gag = None
        if not self.handJoint:
            self.handJoint = self.avatar.find('**/def_joint_right_hold')
        track = ProjectileInterval(entity, startPos=self.handJoint.getPos(render), endPos=throwPath.getPos(render), gravityMult=0.9, duration=3)
        track.start()
        self.entities.append([entity, track])
        if self.isLocal():
            self.buildCollisions(entity)
        self.reset()
        return

    def handleSplat(self):
        base.audio3d.detachSound(self.woosh)
        if self.woosh:
            self.woosh.stop()
        self.buildSplat(self.splatScale, self.splatColor)
        base.audio3d.attachSoundToObject(self.hitSfx, self.splat)
        self.splat.reparentTo(render)
        self.splat.setPos(self.splatPos)
        self.hitSfx.play()
        self.cleanupEntity(self.splatPos)
        self.splatPos = None
        taskMgr.doMethodLater(0.5, self.delSplat, 'Delete Splat')
        return

    def cleanupEntity(self, pos):
        for entity, track in self.entities:
            if entity.getPos() == pos:
                self.entities.remove([entity, track])
                if isinstance(entity, Actor):
                    entity.cleanup()
                entity.removeNode()

    def onCollision(self, entry):
        intoNP = entry.getIntoNodePath()
        avNP = intoNP.getParent()
        fromNP = entry.getFromNodePath().getParent()
        if fromNP.isEmpty():
            return
        for key in base.cr.doId2do.keys():
            obj = base.cr.doId2do[key]
            if obj.__class__.__name__ in ('DistributedSuit', 'DistributedTutorialSuit'):
                if obj.getKey() == avNP.getKey():
                    self.avatar.sendUpdate('suitHitByPie', [obj.doId, self.getID()])
            elif obj.__class__.__name__ == 'DistributedToon':
                if obj.getKey() == avNP.getKey():
                    if obj.getHealth() < obj.getMaxHealth() and not obj.isDead():
                        if obj != self.avatar:
                            self.avatar.sendUpdate('toonHitByPie', [obj.doId, self.getID()])
                        else:
                            self.avatar.acceptOnce('gagSensor-into', self.onCollision)
                            return

        self.splatPos = fromNP.getPos()
        self.avatar.sendUpdate('setSplatPos', [self.getID(),
         self.splatPos.getX(),
         self.splatPos.getY(),
         self.splatPos.getZ()])
        self.handleSplat()

    def buildCollisions(self, entity):
        pieSphere = CollisionSphere(0, 0, 0, 1)
        pieSensor = CollisionNode('gagSensor')
        pieSensor.addSolid(pieSphere)
        pieNP = entity.attachNewNode(pieSensor)
        pieNP.setCollideMask(BitMask32(0))
        pieNP.node().setFromCollideMask(CIGlobals.WallBitmask | CIGlobals.FloorBitmask)
        event = CollisionHandlerEvent()
        event.set_in_pattern('%fn-into')
        event.set_out_pattern('%fn-out')
        base.cTrav.add_collider(pieNP, event)
        self.avatar.acceptOnce('gagSensor-into', self.onCollision)