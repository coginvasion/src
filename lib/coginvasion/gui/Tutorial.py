# Embedded file name: lib.coginvasion.gui.Tutorial
"""
  
  Filename: Tutorial.py
  Created by: blach (15Sep14)
  
"""
from panda3d.core import *
from lib.coginvasion.globals import CIGlobals
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.Transitions import *

class Tutorial:

    def __init__(self, pat):
        self.t = Transitions(loader)
        self.pickAToon = pat

    def askTutorial(self):
        self.firstTimeMsg = YesNoDialog(text=CIGlobals.FirstTimeMsg, text_scale=0.07, text_wordwrap=18, buttonGeomList=[CIGlobals.getOkayBtnGeom(), CIGlobals.getCancelBtnGeom()], button_relief=None, button_text_pos=(0, -0.1), command=self.handleTutorialDecision, image_color=CIGlobals.DialogColor, fadeScreen=1)
        return

    def handleTutorialDecision(self, value):
        if value:
            self.firstTimeMsg.destroy()
            self.startTutorial()
            base.hoodBGM.stop()
        else:
            self.firstTimeMsg.destroy()
            self.enablePatButtons()

    def enablePatButtons(self):
        for btn in self.pickAToon.btnList:
            btn['state'] = DGG.NORMAL

        self.pickAToon.quit_btn['state'] = DGG.NORMAL

    def startTutorial(self):
        self.t.fadeOut(1)
        Sequence(Wait(1.2), Func(self.playVideo)).start()

    def playVideo(self):
        self.t.fadeIn(0)
        self.pickAToon.removeGui()
        self.movieTex = MovieTexture('tutorial')
        raise self.movieTex.read('tutorial.avi') or AssertionError('Failed to load tutorial video')
        cm = CardMaker('tutorialCard')
        cm.setFrameFullscreenQuad()
        self.card = NodePath(cm.generate())
        self.card.reparentTo(render2d)
        self.card.setTexture(self.movieTex)
        self.card.setTexScale(TextureStage.getDefault(), self.movieTex.getTexScale())
        self.movieSound = loader.loadSfx('tutorial.avi')
        self.movieTex.synchronizeTo(self.movieSound)
        self.movieSound.play()
        taskMgr.add(self.checkMovieStatus, 'checkMovieStatus')

    def checkMovieStatus(self, task):
        if self.movieSound.status() == AudioSound.READY:
            self.stopVideo()
            return task.done
        return task.cont

    def stopVideo(self):
        self.movieSound.stop()
        self.card.removeNode()
        self.t.fadeOut(0)
        self.pickAToon.createGui(1)
        Sequence(Wait(0.2), Func(self.t.fadeIn, 1)).start()