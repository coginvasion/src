# Embedded file name: lib.coginvasion.hood.TTPlayground
import Playground
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.interval.SoundInterval import SoundInterval
import random

class TTPlayground(Playground.Playground):
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
        taskMgr.add(self.birdTask, 'TTPlayground-birdTask')

    def stopBirds(self):
        taskMgr.remove('TTPlayground-birdTask')
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