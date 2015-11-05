# Embedded file name: lib.coginvasion.gags.TrapGag
"""

  Filename: TrapGag.py
  Created by: DecodedLogic (08Jul15)

"""
from lib.coginvasion.gags.Gag import Gag
from lib.coginvasion.gags.GagType import GagType
import abc

class TrapGag(Gag):

    def __init__(self, name, model, damage, hitSfx, anim = None, doesAutoRelease = True):
        Gag.__init__(self, name, model, damage, GagType.TRAP, hitSfx, anim=anim, autoRelease=doesAutoRelease)
        self.hitSfx = None
        self.entity = None
        if game.process == 'client':
            self.hitSfx = base.audio3d.loadSfx(hitSfx)
        return

    def build(self):
        super(TrapGag, self).build()

    @abc.abstractmethod
    def buildCollisions(self):
        if not self.gag:
            return

    @abc.abstractmethod
    def activate(self):
        pass

    @abc.abstractmethod
    def onCollision(self, entry):
        pass

    @abc.abstractmethod
    def d_doCollision(self):
        pass

    def delete(self):
        super(TrapGag, self).delete()

    def unEquip(self):
        super(TrapGag, self).unEquip()
        if self.gag:
            self.cleanupGag()

    @abc.abstractmethod
    def startTrap(self):
        super(TrapGag, self).start()

    def throw(self):
        pass

    def release(self):
        super(TrapGag, self).release()
        if not self.gag:
            return

    def getHandle(self):
        return self