# Embedded file name: lib.coginvasion.hood.DistributedDLTreasureAI
import DistributedTreasureAI

class DistributedDLTreasureAI(DistributedTreasureAI.DistributedTreasureAI):

    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedTreasureAI.DistributedTreasureAI.__init__(self, air, treasurePlanner, x, y, z)