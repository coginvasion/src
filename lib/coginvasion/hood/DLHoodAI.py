# Embedded file name: lib.coginvasion.hood.DLHoodAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from ToonHoodAI import ToonHoodAI
from lib.coginvasion.globals import CIGlobals

class DLHoodAI(ToonHoodAI):
    notify = directNotify.newCategory('DLHoodAI')

    def __init__(self, air):
        ToonHoodAI.__init__(self, air, CIGlobals.DonaldsDreamlandId, CIGlobals.DonaldsDreamland)
        self.startup()

    def startup(self):
        self.dnaFiles = ['phase_8/dna/donalds_dreamland_9100.dna', 'phase_8/dna/donalds_dreamland_9200.dna', 'phase_8/dna/donalds_dreamland_sz.dna']
        ToonHoodAI.startup(self)