# Embedded file name: lib.coginvasion.suit.DistributedCogBattleAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from lib.coginvasion.distributed.HoodMgr import HoodMgr
from lib.coginvasion.suit.DistributedSuitManagerAI import DistributedSuitManagerAI
from lib.coginvasion.shop.DistributedGagShopAI import DistributedGagShopAI
from lib.coginvasion.shop.DistributedBattleShopAI import DistributedBattleShopAI
from lib.coginvasion.battle.DistributedPieTurretManagerAI import DistributedPieTurretManagerAI
import CogBattleGlobals

class DistributedCogBattleAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedCogBattleAI')

    def __init__(self, air):
        try:
            self.DistributedCogBattle_initialized
            return
        except:
            self.DistributedCogBattle_initialized = 1

        DistributedObjectAI.__init__(self, air)
        self.avIds = None
        self.hoodIndex = -1
        self.numPlayers = None
        self.totalCogs = 0
        self.cogsRemaining = 0
        self.suitManager = None
        self.gagShop = None
        self.hoodMgr = HoodMgr()
        self.battleShop = None
        self.turretMgr = None
        self.arrivedAvatars = []
        return

    def setAvIdArray(self, array):
        self.avIds = array

    def getAvIdArray(self):
        return self.avIds

    def setTotalCogs(self, num):
        self.totalCogs = num

    def d_setTotalCogs(self, num):
        self.sendUpdate('setTotalCogs', [num])

    def b_setTotalCogs(self, num):
        self.d_setTotalCogs(num)
        self.setTotalCogs(num)

    def getTotalCogs(self):
        return self.totalCogs

    def setCogsRemaining(self, num):
        self.cogsRemaining = num
        if self.cogsRemaining <= 0:
            if self.suitManager:
                if self.suitManager.numSuits == 0 and not self.suitManager.tournament.inTournament:
                    self.suitManager.stopSpawner()
                    self.sendUpdate('victory', [])

    def d_setCogsRemaining(self, num):
        self.sendUpdate('setCogsRemaining', [num])

    def b_setCogsRemaining(self, num):
        if num > -1:
            self.d_setCogsRemaining(num)
        self.setCogsRemaining(num)

    def getCogsRemaining(self):
        return self.cogsRemaining

    def setHoodIndex(self, index):
        self.hoodIndex = index
        if not self.gagShop:
            self.gagShop = DistributedGagShopAI(self.air)
            self.gagShop.generateWithRequired(self.zoneId)
            x, y, z, h, p, r = self.hoodMgr.GagShopClerkPoints[CogBattleGlobals.HoodIndex2HoodName[self.getHoodIndex()]]
            self.gagShop.b_setPosHpr(x, y, z, h, p, r)
        if not self.battleShop:
            self.battleShop = DistributedBattleShopAI(self.air)
            self.battleShop.generateWithRequired(self.zoneId)
            x, y, z, h, p, r = self.hoodMgr.BattleShopClerkPoints[CogBattleGlobals.HoodIndex2HoodName[self.getHoodIndex()]]
            self.battleShop.b_setPosHpr(x, y, z, h, p, r)

    def d_setHoodIndex(self, index):
        self.sendUpdate('setHoodIndex', [index])

    def b_setHoodIndex(self, index):
        self.d_setHoodIndex(index)
        self.setHoodIndex(index)

    def getHoodIndex(self):
        return self.hoodIndex

    def setNumPlayers(self, players):
        self.numPlayers = players

    def getNumPlayers(self):
        return self.numPlayers

    def arrived(self):
        avId = self.air.getAvatarIdFromSender()
        self.arrivedAvatars.append(avId)

    def startWatchingAvatars(self):
        taskMgr.add(self.__monitorAvatars, 'DistributedCogBattleAI-monitorAvatars-' + str(id(self)))

    def stopWatchingAvatars(self):
        taskMgr.remove('DistributedCogBattleAI-monitorAvatars-' + str(id(self)))

    def __monitorAvatars(self, task):
        for avId in self.avIds:
            if avId not in self.air.doId2do.keys() or self.air.doId2do.get(avId).zoneId != self.zoneId and avId in self.arrivedAvatars:
                self.notify.warning('Removing avatar {0} from DistributedCogBattleAI-{1}...'.format(avId, self.doId))
                for turret in self.turretMgr.turretId2turret.values():
                    if turret.getOwner() == avId:
                        self.turretMgr.killTurret(turret.doId)

                self.avIds.remove(avId)

        if len(self.avIds) == 0:
            self.notify.warning('All avatars have left DistributedCogBattleAI-{0}, deleting DO...'.format(self.doId))
            self.disable()
            self.requestDelete()
            return task.done
        task.delayTime = 5
        return task.again

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.suitManager = DistributedSuitManagerAI(self.air)
        self.suitManager.setBattle(self)
        self.suitManager.generateWithRequired(self.zoneId)
        self.turretMgr = DistributedPieTurretManagerAI(self.air)
        self.turretMgr.generateWithRequired(self.zoneId)

    def disable(self):
        self.stopWatchingAvatars()
        if self.gagShop:
            self.gagShop.disable()
            self.gagShop.requestDelete()
            self.gagShop = None
        if self.suitManager:
            self.suitManager.disable()
            self.suitManager.requestDelete()
            self.suitManager = None
        if self.battleShop:
            self.battleShop.disable()
            self.battleShop.requestDelete()
            self.battleShop = None
        if self.turretMgr:
            self.turretMgr.disable()
            self.turretMgr.requestDelete()
            self.turretMgr = None
        self.avIds = None
        self.hoodIndex = None
        self.numPlayers = None
        self.totalCogs = None
        self.cogsRemaining = None
        self.suitManager = None
        self.hoodMgr = None
        self.arrivedAvatars = None
        base.air.deallocateZone(self.zoneId)
        return