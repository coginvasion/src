# Embedded file name: lib.coginvasion.shop.BattleShop
"""

  Filename: BattleShop.py
  Created by: DecodedLogic (14Jul15)

"""
from direct.directnotify.DirectNotifyGlobal import directNotify
from lib.coginvasion.shop.Shop import Shop
from lib.coginvasion.shop.ItemType import ItemType

class BattleShop(Shop):
    notify = directNotify.newCategory('BattleShop')

    def __init__(self, distShop, doneEvent):
        Shop.__init__(self, distShop, doneEvent)
        self.distShop.addItem('Whole Cream \nPie', ItemType.UPGRADE, 200, 'phase_3.5/maps/cannon-icon.png', upgradeID=0, maxUpgrades=1)
        self.distShop.addItem('Whole Fruit \nPie', ItemType.UPGRADE, 150, 'phase_3.5/maps/cannon-icon.png', upgradeID=1, maxUpgrades=1)
        self.distShop.addItem('Birthday Cake', ItemType.UPGRADE, 500, 'phase_3.5/maps/cannon-icon.png', upgradeID=2, maxUpgrades=1)
        self.distShop.addItem('Wedding Cake', ItemType.UPGRADE, 750, 'phase_3.5/maps/cannon-icon.png', upgradeID=3, maxUpgrades=1)
        self.distShop.addItem('+20 Laff', ItemType.HEAL, 100, 'phase_3.5/maps/ice-cream-cone.png', heal=20, healCooldown=5, showTitle=True)
        self.items = self.distShop.getItems()

    def confirmPurchase(self):
        self.distShop.sendUpdate('confirmPurchase', [[base.localAvatar.getPUInventory()[0], base.localAvatar.getPUInventory()[1]], base.localAvatar.getMoney()])
        if self.upgradesPurchased:
            if base.localAvatar.getPUInventory()[0] > 0:
                if base.localAvatar.getMyBattle():
                    if base.localAvatar.getMyBattle().getTurretManager():
                        if not base.localAvatar.getMyBattle().getTurretManager().myTurret:
                            base.localAvatar.getMyBattle().getTurretManager().createTurretButton()
        Shop.confirmPurchase(self)

    def cancelPurchase(self):
        if self.upgradesPurchased:
            if self.originalUpgrades[0] < base.localAvatar.getPUInventory()[0]:
                if base.localAvatar.getMyBattle():
                    if base.localAvatar.getMyBattle().getTurretManager():
                        base.localAvatar.getMyBattle().getTurretManager().destroyGui()
        base.localAvatar.setPUInventory(self.originalUpgrades)
        Shop.cancelPurchase(self)

    def enter(self):
        self.originalUpgrades = base.localAvatar.getPUInventory()
        self.upgradesPurchased = False
        Shop.enter(self)

    def exit(self):
        Shop.exit(self)
        self.originalUpgrades = None
        self.upgradesPurchased = None
        return

    def update(self):
        Shop.update(self)