# Embedded file name: lib.coginvasion.minigame.DistributedToonCannonAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedNodeAI import DistributedNodeAI

class DistributedToonCannonAI(DistributedNodeAI):
    notify = directNotify.newCategory('DistributedToonCannonAI')

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)
        self.avatar = None
        return

    def putAvatarInTurret(self, avId):
        self.avatar = avId

    def delete(self):
        del self.avatar
        DistributedNodeAI.delete(self)