# Embedded file name: lib.coginvasion.hood.DistributedSZTreasure
"""

  Filename: DistributedSZTreasure.py
  Created by: DecodedLogic (15Jul15)

"""
from lib.coginvasion.hood.DistributedTreasure import DistributedTreasure

class DistributedSZTreasure(DistributedTreasure):

    def __init__(self, cr):
        DistributedTreasure.__init__(self, cr)

    def delete(self):
        DistributedTreasure.delete(self)