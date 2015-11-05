# Embedded file name: lib.coginvasion.hood.ToonHoodAI
"""

  Filename: ToonHoodAI.py
  Created by: blach (05Jan15)

"""
from lib.coginvasion.globals import CIGlobals
from lib.coginvasion.hood.HoodAI import HoodAI
from lib.coginvasion.shop.DistributedGagShopAI import DistributedGagShopAI
from lib.coginvasion.suit.DistributedSuitManagerAI import DistributedSuitManagerAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from lib.coginvasion.suit.DistributedCogStationAI import DistributedCogStationAI
from lib.coginvasion.battle.DistributedBattleTrolleyAI import DistributedBattleTrolleyAI
from lib.coginvasion.suit import CogBattleGlobals

class ToonHoodAI(HoodAI):
    notify = directNotify.newCategory('ToonHoodAI')

    def __init__(self, air, zoneId, hood):
        HoodAI.__init__(self, air, zoneId, hood)
        self.gagShop = None
        self.suitManager = None
        self.cogStation = None
        return

    def startup(self):
        HoodAI.startup(self)
        if CogBattleGlobals.HoodId2HoodIndex.get(self.hood, None) != None or self.hood == CIGlobals.ToontownCentral:
            if self.hood == CIGlobals.ToontownCentral:
                hoodIndex = CogBattleGlobals.HoodId2HoodIndex[CIGlobals.BattleTTC]
            else:
                hoodIndex = CogBattleGlobals.HoodId2HoodIndex[self.hood]
            self.cogStation = DistributedBattleTrolleyAI(self.air, hoodIndex)
            self.cogStation.generateWithRequired(self.zoneId)
        else:
            self.notify.info('This ToonHood is not a cog battle area.')
        return

    def shutdown(self):
        if self.gagShop:
            self.notify.info('Shutting down gag shop...')
            self.gagShop.requestDelete()
            self.gagShop = None
        if self.suitManager:
            self.notify.info('Shutting down suit manager...')
            self.suitManager.requestDelete()
            self.suitManager = None
        HoodAI.shutdown(self)
        return