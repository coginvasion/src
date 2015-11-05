# Embedded file name: lib.coginvasion.toon.SmartCamera
"""

  Filename: SmartCamera.py
  Created by: blach (27July14)
  
"""
from panda3d.core import *
from pandac.PandaModules import *
from direct.directnotify.DirectNotify import *
from direct.task import Task
from lib.coginvasion.globals import CIGlobals
import math

class SmartCamera:
    UPDATE_TASK_NAME = 'update_smartcamera'
    notify = DirectNotify().newCategory('SmartCamera')

    def __init__(self):
        self.default_pos = None
        self.parent = None
        self.cTrav = CollisionTraverser('camera_traverser')
        self.cTrav.set_respect_prev_transform(True)
        self.initialized = False
        self.started = False
        self.notify.debug('SmartCamera initialized!')
        return

    def set_default_pos(self, pos):
        self.default_pos = pos

    def get_default_pos(self):
        return self.default_pos

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def initialize_smartcamera(self):
        if not self.parent:
            self.notify.error('SmartCamera cannot initialize without a parent set!')
        if not self.default_pos:
            self.notify.error('SmartCamera cannot initialize without a default pos!')
        camera.reparent_to(self.get_parent())
        camera.set_pos(self.get_default_pos()[0])
        camera.set_hpr(0, 0, 0)

    def enterFirstPerson(self):
        self.stop_smartcamera()
        if hasattr(self.get_parent(), 'toon_head'):
            head = self.get_parent().toon_head
            camera.reparentTo(head)
        camera.setPos(0, -0.35, 0)
        camera.setHpr(0, 0, 0)

    def exitFirstPerson(self):
        self.initialize_smartcamera()
        self.initialize_smartcamera_collisions()
        self.start_smartcamera()

    def initialize_smartcamera_collisions(self):
        if self.initialized:
            return
        cam_sphere = CollisionSphere(0, 0, 0, 1.5)
        cam_collnode = CollisionNode('cam_node')
        cam_collnode.add_solid(cam_sphere)
        self.cam_coll_np = camera.attach_new_node(cam_collnode)
        self.cam_coll_np.set_collide_mask(BitMask32(0))
        self.cam_coll_np.node().set_from_collide_mask(CIGlobals.WallBitmask | CIGlobals.FloorBitmask)
        pusher = CollisionHandlerPusher()
        pusher.set_in_pattern('%in')
        pusher.add_collider(self.cam_coll_np, camera)
        self.cTrav.add_collider(self.cam_coll_np, pusher)
        self.initialized = True

    def delete_smartcamera_collisions(self):
        if hasattr(self, 'cam_coll_np'):
            self.cam_coll_np.remove_node()
            del self.cam_coll_np
        self.initialized = False

    def start_smartcamera(self):
        if not self.default_pos:
            self.notify.error('SmartCamera cannot start without a default camera position!')
        if self.started:
            return
        taskMgr.add(self.update_smartcamera, self.UPDATE_TASK_NAME)
        self.started = True

    def stop_smartcamera(self):
        self.delete_smartcamera_collisions()
        taskMgr.remove(self.UPDATE_TASK_NAME)
        self.started = False

    def update_smartcamera(self, task):
        camera.look_at(self.default_pos[1])
        camera.set_fluid_pos(self.default_pos[0])
        self.cTrav.traverse(render)
        return Task.again