# Embedded file name: lib.coginvasion.hood.DistributedTBTreasure
"""

  Filename: DistributedTBTreasure.py
  Created by: DecodedLogic (15Jul15)

"""
from lib.coginvasion.hood.DistributedTreasure import DistributedTreasure

class DistributedTBTreasure(DistributedTreasure):

    def __init__(self, cr):
        DistributedTreasure.__init__(self, cr)
        self.modelPath = 'phase_8/models/props/snowflake_treasure.bam'
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.mp3'