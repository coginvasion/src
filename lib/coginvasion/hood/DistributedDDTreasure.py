# Embedded file name: lib.coginvasion.hood.DistributedDDTreasure
import DistributedTreasure

class DistributedDDTreasure(DistributedTreasure.DistributedTreasure):

    def __init__(self, cr):
        DistributedTreasure.DistributedTreasure.__init__(self, cr)
        self.modelPath = 'phase_6/models/props/starfish_treasure.bam'
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.mp3'