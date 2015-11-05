# Embedded file name: lib.coginvasion.minigame.Bullet
"""

  Filename: Bullet.py
  Created by: blach (19Jan15)

"""
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from lib.coginvasion.globals import CIGlobals
from direct.showbase.DirectObject import DirectObject
import random

class Bullet(DirectObject):
    damageFactor = 15.0
    max_dmg = 36
    ShotgunBulletSpeed = 300.0

    def __init__(self, mg, gunNozzle, local, gunName):
        self.mg = mg
        self.local = local
        self.gunName = gunName
        self.bullet = loader.loadModel('phase_4/models/minigames/bullet.egg')
        self.bullet.reparentTo(render)
        self.bullet.setTwoSided(1)
        self.bullet.setPos(gunNozzle.getPos(render))
        self.removeTrack = None
        self.timeSinceShoot = 0.1
        self.gunNozzle = gunNozzle
        if self.local:
            self.setupCollisions()
        self.shoot()
        return

    def setupCollisions(self):
        sphere = CollisionSphere(0, 0, 0, 0.1)
        collnode = CollisionNode('bulletCollNode-' + str(id(self)))
        collnode.addSolid(sphere)
        self.collnp = self.bullet.attachNewNode(collnode)
        self.collnp.setCollideMask(BitMask32(0))
        self.collnp.node().setFromCollideMask(CIGlobals.WallBitmask | CIGlobals.FloorBitmask | CIGlobals.EventBitmask)
        event = CollisionHandlerEvent()
        event.setInPattern('%fn-into')
        event.setOutPattern('%fn-out')
        base.cTrav.addCollider(self.collnp, event)

    def shoot(self):
        pathNode = NodePath('pathForBullet')
        pathNode.reparentTo(self.gunNozzle)
        pathNode.setPos(0, 10000, 0)
        if self.local:
            pathNode.setPos(self.mg.toonFps.gui.crosshair.getX(render), 10000, 0)
        if self.gunName == 'pistol':
            self.bullet.lookAt(pathNode)
            LerpPosInterval(self.bullet, fluid=1, pos=pathNode.getPos(render), duration=15.0, startPos=self.gunNozzle.getPos(render)).start()
        elif self.gunName == 'shotgun':
            self.bullet.setHpr(self.gunNozzle, random.uniform(89, 91), random.uniform(-1.0, 1.0), 0)
            self.bullet.setPos(self.gunNozzle.getPos(render))
            taskMgr.add(self.fireShotgunBulletTask, 'shotgunBulletTask' + str(id(self)))
        if self.local:
            self.acceptOnce('bulletCollNode-' + str(id(self)) + '-into', self.handleCollision)
        self.removeTrack = Sequence()
        self.removeTrack.append(Wait(10.0))
        self.removeTrack.append(Func(self.deleteBullet))
        self.removeTrack.start()
        taskMgr.add(self.calculateDamage, 'calculateBulletDamage' + str(id(self)))

    def fireShotgunBulletTask(self, task):
        self.bullet.setY(self.bullet, self.ShotgunBulletSpeed * globalClock.getDt())
        return task.cont

    def calculateDamage(self, task):
        self.timeSinceShoot += 0.01
        task.delayTime = 0.01
        return task.again

    def deleteBullet(self):
        self.ignore('bulletCollNode-' + str(id(self)) + '-into')
        taskMgr.remove('shotgunBulletTask' + str(id(self)))
        taskMgr.remove('calculateBulletDamage' + str(id(self)))
        if hasattr(self, 'timeSinceShoot'):
            del self.timeSinceShoot
        if hasattr(self, 'mg'):
            del self.mg
        if self.local:
            if hasattr(self, 'collnp'):
                self.collnp.removeNode()
                del self.collnp
        if hasattr(self, 'bullet'):
            self.bullet.removeNode()
            del self.bullet
        if hasattr(self, 'gunNozzle'):
            del self.gunNozzle
        if hasattr(self, 'removeTrack'):
            del self.removeTrack
        if hasattr(self, 'gunName'):
            del self.gunName

    def handleCollision(self, entry):
        taskMgr.remove('calculateBulletDamage' + str(id(self)))
        taskMgr.remove('shotgunBulletTask' + str(id(self)))