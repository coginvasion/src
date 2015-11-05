# Embedded file name: lib.coginvasion.hood.DistributedDDTreasureAI
import DistributedTreasureAI

class DistributedDDTreasureAI(DistributedTreasureAI.DistributedTreasureAI):

    def __init__(self, air, planner, x, y, z):
        DistributedTreasureAI.DistributedTreasureAI.__init__(self, air, planner, x, y, z)