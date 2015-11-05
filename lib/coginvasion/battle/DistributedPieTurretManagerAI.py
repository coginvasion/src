# Embedded file name: lib.coginvasion.battle.DistributedPieTurretManagerAI
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from lib.coginvasion.globals import CIGlobals
from lib.coginvasion.battle.DistributedPieTurretAI import DistributedPieTurretAI

class DistributedPieTurretManagerAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedPieTurretManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.turretId2turret = {}

    def killTurret(self, turretId):
        turret = self.turretId2turret[turretId]
        turret.disable()
        turret.requestDelete()
        del self.turretId2turret[turretId]

    def requestPlace(self, posHpr):
        avId = self.air.getAvatarIdFromSender()
        turret = DistributedPieTurretAI(self.air)
        turret.setManager(self)
        turret.generateWithRequired(self.zoneId)
        turret.b_setMaxHealth(100)
        turret.b_setHealth(100)
        turret.b_setOwner(avId)
        x, y, z, h, p, r = posHpr
        turret.b_setPosHpr(x, y, z, h, p, r)
        turret.b_setParent(CIGlobals.SPRender)
        turret.startScanning()
        self.turretId2turret[turret.doId] = turret
        self.sendUpdateToAvatarId(avId, 'turretPlaced', [turret.doId])

    def disable(self):
        for turret in self.turretId2turret.values():
            turret.requestDelete()
            turret.disable()
            turret.delete()

        self.turretId2turret = None
        return