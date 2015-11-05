# Embedded file name: lib.coginvasion.hood.DistributedDGTreasureAI
import DistributedTreasureAI

class DistributedDGTreasureAI(DistributedTreasureAI.DistributedTreasureAI):

    def __init__(self, air, planner, x, y, z):
        DistributedTreasureAI.DistributedTreasureAI.__init__(self, air, planner, x, y, z)