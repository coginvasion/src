# Embedded file name: lib.coginvasion.avatar.DistributedAvatarAI
"""

  Filename: DistributedAvatarAI.py
  Created by: blach (02Nov14)

"""
from panda3d.core import *
from direct.distributed import DistributedNodeAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedAvatarAI(DistributedNodeAI.DistributedNodeAI):
    notify = directNotify.newCategory('DistributedAvatarAI')

    def __init__(self, air):
        try:
            self.DistributedAvatarAI_initialized
            return
        except:
            self.DistributedAvatarAI_initialized = 1

        DistributedNodeAI.DistributedNodeAI.__init__(self, air)
        self.health = 0
        self.maxHealth = 0
        self.name = ''
        self.place = 0
        self.hood = ''

    def setHood(self, hood):
        self.hood = hood

    def d_setHood(self, hood):
        self.sendUpdate('setHood', [hood])

    def b_setHood(self, hood):
        self.d_setHood(hood)
        self.setHood(hood)

    def getHood(self):
        return self.hood

    def d_setChat(self, chat):
        self.sendUpdate('setChat', [chat])

    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.d_setName(name)
        self.setName(name)

    def getName(self):
        return self.name

    def setMaxHealth(self, health):
        self.maxHealth = health

    def d_setMaxHealth(self, health):
        self.sendUpdate('setMaxHealth', [health])

    def b_setMaxHealth(self, health):
        self.d_setMaxHealth(health)
        self.setMaxHealth(health)

    def getMaxHealth(self):
        return self.maxHealth

    def setPlace(self, place):
        self.place = place

    def b_setPlace(self, place):
        self.sendUpdate('setPlace', [place])
        self.setPlace(place)

    def getPlace(self):
        return self.place

    def isDead(self):
        return self.health <= 0

    def setHealth(self, health):
        self.health = health

    def d_setHealth(self, health):
        self.sendUpdate('setHealth', [health])

    def b_setHealth(self, health):
        self.d_setHealth(health)
        self.setHealth(health)

    def getHealth(self):
        return self.health

    def d_announceHealth(self, level, hp):
        self.sendUpdate('announceHealth', [level, hp])

    def disable(self):
        self.health = None
        self.maxHealth = None
        self.name = None
        return