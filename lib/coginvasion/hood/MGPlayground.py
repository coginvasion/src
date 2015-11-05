# Embedded file name: lib.coginvasion.hood.MGPlayground
"""

  Filename: MGPlayground.py
  Created by: blach (5Jan15)

"""
from Playground import Playground
from direct.fsm.State import State
from direct.directnotify.DirectNotifyGlobal import directNotify

class MGPlayground(Playground):
    notify = directNotify.newCategory('MGPlayground')

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.__init__(self, loader, parentFSM, doneEvent)
        self.fsm.addState(State('station', self.enterStation, self.exitStation, ['walk', 'teleportOut']))
        self.fsm.getStateNamed('stop').addTransition('station')

    def enterStation(self):
        base.localAvatar.startPosHprBroadcast()
        base.localAvatar.d_broadcastPositionNow()

    def exitStation(self):
        base.localAvatar.stopPosHprBroadcast()