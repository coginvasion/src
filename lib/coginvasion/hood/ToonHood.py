# Embedded file name: lib.coginvasion.hood.ToonHood
"""

  Filename: ToonHood.py
  Created by: blach (14Dec14)

"""
import Hood
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State

class ToonHood(Hood.Hood):

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        Hood.Hood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.safeZoneLoader = None
        self.fsm = ClassicFSM('Hood', [State('off', self.enterOff, self.exitOff), State('safeZoneLoader', self.enterSafeZoneLoader, self.exitSafeZoneLoader, ['quietZone']), State('quietZone', self.enterQuietZone, self.exitQuietZone, ['safeZoneLoader'])], 'off', 'off')
        self.fsm.enterInitialState()
        return

    def loadLoader(self, requestStatus):
        loader = requestStatus['loader']
        if loader == 'safeZoneLoader':
            if self.safeZoneLoader:
                self.loader = self.safeZoneLoader(self, self.fsm.getStateNamed('safeZoneLoader'), self.loaderDoneEvent)
                self.loader.load()
            else:
                self.notify.error('ToonHood.ToonHood.safeZoneLoader cannot be None!' % loader)
        else:
            self.notify.error('Unknown loader %s!' % loader)

    def load(self):
        Hood.Hood.load(self)

    def unload(self):
        del self.safeZoneLoader
        Hood.Hood.unload(self)

    def enter(self, requestStatus):
        self.loadLoader(requestStatus)
        Hood.Hood.enter(self, requestStatus)

    def exit(self):
        Hood.Hood.exit(self)