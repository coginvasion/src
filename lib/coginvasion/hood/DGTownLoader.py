# Embedded file name: lib.coginvasion.hood.DGTownLoader
import TownLoader
import DGStreet

class DGTownLoader(TownLoader.TownLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = DGStreet.DGStreet
        self.musicFile = 'phase_8/audio/bgm/DG_SZ.mid'
        self.interiorMusicFile = self.musicFile
        self.townStorageDNAFile = 'phase_8/dna/storage_DG_town.dna'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        dnaFile = 'phase_8/dna/daisys_garden_' + str(self.branchZone) + '.dna'
        self.createHood(dnaFile)