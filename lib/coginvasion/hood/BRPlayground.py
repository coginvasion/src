# Embedded file name: lib.coginvasion.hood.BRPlayground
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.interval.SoundInterval import SoundInterval
import Playground
import BRWater
import random

class BRPlayground(Playground.Playground):
    notify = directNotify.newCategory('BRPlayground')
    InWaterZ = 0.93

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)
        self.windSfx = None
        self.water = None
        return

    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)
        self.water = BRWater.BRWater(self)
        self.startWind()

    def exit(self):
        self.stopWind()
        self.water.fsm.requestFinalState()
        Playground.Playground.exit(self)

    def unload(self):
        self.water.cleanup()
        self.water = None
        Playground.Playground.unload(self)
        return

    def startWaterWatch(self, enter = 1):
        taskMgr.add(self.__waterWatch, 'BRPlayground-waterWatch', extraArgs=[enter], appendTask=True)

    def __waterWatch(self, enter, task):
        if enter:
            if base.localAvatar.getZ(render) <= self.InWaterZ:
                self.water.fsm.request('freezeUp')
                return task.done
        elif base.localAvatar.getZ(render) > self.InWaterZ:
            if self.water.fsm.getCurrentState().getName() == 'freezeUp':
                self.water.fsm.request('coolDown')
                return task.done
        return task.cont

    def stopWaterWatch(self):
        taskMgr.remove('BRPlayground-waterWatch')

    def startWind(self):
        taskMgr.add(self.windTask, 'BRPlayground-windTask')

    def stopWind(self):
        taskMgr.remove('BRPlayground-windTask')
        if self.windSfx:
            self.windSfx.finish()
            self.windSfx = None
        return

    def windTask(self, task):
        noiseFile = random.choice(self.loader.windNoises)
        noise = base.loadSfx(noiseFile)
        if self.windSfx:
            self.windSfx.finish()
            self.windSfx = None
        self.windSfx = SoundInterval(noise)
        self.windSfx.start()
        task.delayTime = random.random() * 20 + 1
        return task.again