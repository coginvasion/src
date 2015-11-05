# Embedded file name: lib.coginvasion.hood.PublicWalk
"""

  Filename: PublicWalk.py
  Created by: blach (15Dec14)
  
  Description: PublicWalk is used for avatar movement in public areas such
               as playgrounds. All it does is inherent from Walk and enable
               the shticker book, laff meter, and pie throwing when we
               enter the StateData.

"""
import Walk
from direct.directnotify.DirectNotifyGlobal import directNotify

class PublicWalk(Walk.Walk):
    notify = directNotify.newCategory('PublicWalk')

    def __init__(self, parentFSM, doneEvent):
        Walk.Walk.__init__(self, doneEvent)
        self.parentFSM = parentFSM

    def enter(self):
        Walk.Walk.enter(self)
        base.localAvatar.showBookButton()
        base.localAvatar.createLaffMeter()
        base.localAvatar.showPieButton()
        base.localAvatar.enablePies(1)
        base.localAvatar.createMoney()

    def exit(self):
        Walk.Walk.exit(self)
        base.localAvatar.hideBookButton()
        base.localAvatar.disableLaffMeter()
        base.localAvatar.disablePies()
        base.localAvatar.hidePieButton()
        base.localAvatar.disableMoney()