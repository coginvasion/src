# Embedded file name: lib.coginvasion.hood.BRHoodAI
from direct.directnotify.DirectNotifyGlobal import directNotify
import ToonHoodAI
from lib.coginvasion.globals import CIGlobals

class BRHoodAI(ToonHoodAI.ToonHoodAI):
    notify = directNotify.newCategory('BRHoodAI')

    def __init__(self, air):
        ToonHoodAI.ToonHoodAI.__init__(self, air, CIGlobals.TheBrrrghId, CIGlobals.TheBrrrgh)
        self.startup()

    def startup(self):
        self.notify.info('Creating hood {0}...'.format(CIGlobals.TheBrrrgh))
        self.dnaFiles = ['phase_8/dna/the_burrrgh_3100.dna',
         'phase_8/dna/the_burrrgh_3200.dna',
         'phase_8/dna/the_burrrgh_3300.dna',
         'phase_8/dna/the_burrrgh_sz.dna']
        ToonHoodAI.ToonHoodAI.startup(self)
        self.notify.info('Finished creating hood %s' % CIGlobals.TheBrrrgh)

    def shutdown(self):
        self.notify.info('Shutting down hood %s' % CIGlobals.TheBrrrgh)
        ToonHoodAI.ToonHoodAI.shutdown(self)
        self.notify.info('Finished shutting down hood %s' % CIGlobals.TheBrrrgh)