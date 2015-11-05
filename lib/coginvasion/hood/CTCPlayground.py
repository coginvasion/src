# Embedded file name: lib.coginvasion.hood.CTCPlayground
"""

  Filename: CTCPlayground.py
  Created by: blach (14Dec14)

"""
import Playground
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.interval.SoundInterval import SoundInterval
import random

class CTCPlayground(Playground.Playground):
    notify = directNotify.newCategory('TTPlayground')

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)
        self.birdSfx = None
        return

    def load(self):
        Playground.Playground.load(self)

    def unload(self):
        Playground.Playground.unload(self)

    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)
        self.startBirds()

    def startBirds(self):
        taskMgr.add(self.birdTask, 'CTCPlayground-birdTask')

    def stopBirds(self):
        taskMgr.remove('CTCPlayground-birdTask')
        if self.birdSfx:
            self.birdSfx.finish()
            self.birdSfx = None
        return

    def birdTask(self, task):
        noiseFile = random.choice(self.loader.birdNoises)
        noise = base.loadSfx(noiseFile)
        if self.birdSfx:
            self.birdSfx.finish()
            self.birdSfx = None
        self.birdSfx = SoundInterval(noise)
        self.birdSfx.start()
        task.delayTime = random.random() * 20 + 1
        return task.again

    def exit(self):
        self.stopBirds()
        Playground.Playground.exit(self)