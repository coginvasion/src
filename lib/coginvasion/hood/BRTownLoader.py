# Embedded file name: lib.coginvasion.hood.BRTownLoader
import TownLoader
import BRStreet

class BRTownLoader(TownLoader.TownLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = BRStreet.BRStreet
        self.musicFile = 'phase_8/audio/bgm/TB_SZ.mid'
        self.interiorMusicFile = 'phase_8/audio/bgm/TB_SZ_activity.mid'
        self.townStorageDNAFile = 'phase_8/dna/storage_BR_town.dna'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        dnaFile = 'phase_8/dna/the_burrrgh_' + str(self.branchZone) + '.dna'
        self.createHood(dnaFile)