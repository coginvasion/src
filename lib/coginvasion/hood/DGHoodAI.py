# Embedded file name: lib.coginvasion.hood.DGHoodAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from ToonHoodAI import ToonHoodAI
from lib.coginvasion.globals import CIGlobals

class DGHoodAI(ToonHoodAI):
    notify = directNotify.newCategory('DGHoodAI')

    def __init__(self, air):
        ToonHoodAI.__init__(self, air, CIGlobals.DaisyGardensId, CIGlobals.DaisyGardens)
        self.startup()

    def startup(self):
        self.dnaFiles = []
        self.dnaFiles = ['phase_8/dna/daisys_garden_5100.dna', 'phase_8/dna/daisys_garden_5300.dna', 'phase_8/dna/daisys_garden_sz.dna']
        ToonHoodAI.startup(self)