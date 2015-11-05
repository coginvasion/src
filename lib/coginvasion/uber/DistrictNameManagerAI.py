# Embedded file name: lib.coginvasion.uber.DistrictNameManagerAI
from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistrictNameManagerAI(DistributedObjectGlobalAI):
    notify = directNotify.newCategory('DistrictNameManagerAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

    def d_requestDistrictName(self):
        self.sendUpdate('requestDistrictName', [])

    def claimDistrictName(self, name):
        self.air.gotDistrictName(name)

    def noAvailableNames(self):
        self.air.noDistrictNames()

    def d_toonJoined(self, avatarId):
        self.sendUpdate('toonJoined', [avatarId])

    def d_toonLeft(self, avatarId):
        self.sendUpdate('toonLeft', [avatarId])