# Embedded file name: lib.coginvasion.hood.DistributedMLTreasure
import DistributedTreasure

class DistributedMLTreasure(DistributedTreasure.DistributedTreasure):

    def __init__(self, cr):
        DistributedTreasure.DistributedTreasure.__init__(self, cr)
        self.modelPath = 'phase_6/models/props/music_treasure.bam'
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.mp3'