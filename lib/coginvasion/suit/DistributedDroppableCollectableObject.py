# Embedded file name: lib.coginvasion.suit.DistributedDroppableCollectableObject
"""

  Filename: DistributedDroppableCollectableObject.py
  Created by: blach (22Mar15)

"""
from panda3d.core import *
from direct.distributed.DistributedNode import DistributedNode
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.controls.ControlManager import CollisionHandlerRayStart
from lib.coginvasion.globals import CIGlobals

class DistributedDroppableCollectableObject(DistributedNode):
    notify = directNotify.newCategory('DistributedDroppableCollectableObject')

    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        NodePath.__init__(self, 'droppableCollectableObject')
        self.collSensorNodePath = None
        self.collRayNodePath = None
        return

    def loadObject(self):
        pass

    def removeObject(self):
        pass

    def loadCollisions(self):
        sphere = CollisionSphere(0, 0, 0, 1)
        sphere.setTangible(0)
        node = CollisionNode(self.uniqueName('collectableCollNode'))
        node.addSolid(sphere)
        node.setCollideMask(CIGlobals.WallBitmask)
        self.collSensorNodePath = self.attachNewNode(node)
        ray = CollisionRay(0.0, 0.0, CollisionHandlerRayStart, 0.0, 0.0, -1.0)
        rayNode = CollisionNode(self.uniqueName('collectableRayNode'))
        rayNode.addSolid(ray)
        rayNode.setFromCollideMask(CIGlobals.FloorBitmask)
        rayNode.setIntoCollideMask(BitMask32.allOff())
        self.collRayNodePath = self.attachNewNode(rayNode)
        lifter = CollisionHandlerFloor()
        lifter.addCollider(self.collRayNodePath, self)
        base.cTrav.addCollider(self.collRayNodePath, lifter)

    def removeCollisions(self):
        if self.collSensorNodePath:
            self.collSensorNodePath.removeNode()
            self.collSensorNodePath = None
        if self.collRayNodePath:
            self.collRayNodePath.removeNode()
            self.collRayNodePath = None
        return

    def load(self):
        self.loadObject()
        self.loadCollisions()
        self.acceptCollisions()

    def unload(self):
        self.ignoreCollisions()
        self.removeCollisions()
        self.removeObject()
        self.removeNode()
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()

    def handleCollisions(self, entry):
        self.sendUpdate('collectedObject', [])

    def acceptCollisions(self):
        self.acceptOnce('enter' + self.collSensorNodePath.node().getName(), self.handleCollisions)

    def ignoreCollisions(self):
        self.ignore('enter' + self.collSensorNodePath.node().getName())

    def generate(self):
        DistributedNode.generate(self)
        self.load()

    def disable(self):
        self.unload()
        DistributedNode.disable(self)