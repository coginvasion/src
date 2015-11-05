# Embedded file name: lib.coginvasion.hood.RecoverPlayground
"""

  Filename: RecoverPlayground.py
  Created by: blach (3Apr15)

"""
import Playground
from direct.directnotify.DirectNotifyGlobal import directNotify

class RecoverPlayground(Playground.Playground):
    notify = directNotify.newCategory('RecoverPlayground')

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)