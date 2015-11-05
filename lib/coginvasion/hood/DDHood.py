# Embedded file name: lib.coginvasion.hood.DDHood
from panda3d.core import Fog
from lib.coginvasion.globals import CIGlobals
import DDTownLoader
import DDSafeZoneLoader
from ToonHood import ToonHood

class DDHood(ToonHood):

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = CIGlobals.DonaldsDock
        self.safeZoneLoader = DDSafeZoneLoader.DDSafeZoneLoader
        self.townLoader = DDTownLoader.DDTownLoader
        self.storageDNAFile = 'phase_6/dna/storage_DD.dna'
        self.skyFilename = 'phase_3.5/models/props/BR_sky.bam'
        self.spookySkyFile = 'phase_3.5/models/props/BR_sky.bam'
        self.titleColor = (0.8, 0.6, 0.5, 1.0)
        self.loaderDoneEvent = 'DDHood-loaderDone'
        self.fog = None
        return

    def load(self):
        ToonHood.load(self)
        self.fog = Fog('DDFog')
        self.parentFSM.getStateNamed('DDHood').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('DDHood').removeChild(self.fsm)
        del self.fog
        ToonHood.unload(self)