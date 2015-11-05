# Embedded file name: lib.coginvasion.base.MotionBlur
"""

  Filename: MotionBlur.py
  Created by: blach (7Feb15)

"""
from pandac.PandaModules import *
from direct.task import Task

class MotionBlur:
    MIN_FPS = 30.0

    def __init__(self):
        self.tex = Texture()
        self.tex.setMinfilter(Texture.FTLinear)
        base.win.addRenderTexture(self.tex, GraphicsOutput.RTMTriggeredCopyTexture)
        self.backcam = base.makeCamera2d(base.win, sort=-10)
        self.background = NodePath('background')
        self.backcam.reparentTo(self.background)
        self.background.setDepthTest(0)
        self.background.setDepthWrite(0)
        self.backcam.node().getDisplayRegion(0).setClearDepthActive(0)
        self.fcard = base.win.getTextureCard()
        self.fcard.reparentTo(render2d)
        self.fcard.setTransparency(1)
        self.fcard.hide()

    def start(self):
        self.fcard.show()
        self.fcard.setColor(1.0, 1.0, 1.0, 0.5)
        self.fcard.setScale(1.0)
        self.fcard.setPos(0, 0, 0)
        self.fcard.setR(0)
        self.clickrate = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000L
        self.nextclick = 0
        taskMgr.add(self.takeSnapShot, 'takeSnapShot')

    def stop(self):
        taskMgr.remove('takeSnapShot')
        self.tex.clear()
        self.fcard.hide()
        self.clickrate = 0
        self.nextclick = 0

    def takeSnapShot(self, task):
        self.fcard.show()
        if globalClock.getAverageFrameRate() < self.MIN_FPS:
            self.tex.clear()
            self.fcard.hide()
            return Task.cont
        if task.time > self.nextclick:
            self.nextclick += 1.0 / self.clickrate * globalClock.getDt()
            if self.nextclick < task.time:
                self.nextclick = task.time * globalClock.getDt()
            base.win.triggerCopy()
        return Task.cont

    def cleanup(self):
        del self.clickrate
        del self.nextclick
        self.fcard.removeNode()
        del self.fcard