# Embedded file name: lib.coginvasion.gui.CIProgressScreen
"""
  
  Filename: CIProgressScreen.py
  Created by: blach (12Aug14)
  
"""
from lib.coginvasion.globals import CIGlobals
from direct.directnotify.DirectNotify import DirectNotify
from panda3d.core import TextNode
from direct.gui.DirectGui import OnscreenImage, DirectWaitBar, DirectLabel
notify = DirectNotify().newCategory('CIProgressScreen')

class CIProgressScreen:

    def __init__(self):
        self.bg = loader.loadTexture('phase_3/maps/loading-background.png')
        self.logo = loader.loadTexture('phase_3/maps/CogInvasion_Logo.png')
        self.logoImg = OnscreenImage(image=self.logo, scale=(0.5, 0, 0.3), pos=(0, 0, 0.65), parent=hidden)
        self.logoImg.setTransparency(True)
        self.bg_img = OnscreenImage(image=self.bg, parent=hidden)
        self.bg_img.setSx(1.35)
        self.progress_bar = DirectWaitBar(value=0, pos=(0, 0, -0.85), parent=hidden, text_pos=(0, 0, 0.2))
        self.progress_bar.setSx(1.064)
        self.progress_bar.setSz(0.38)
        self.loading_lbl = DirectLabel(text='', relief=None, scale=0.5, text_scale=0.25, pos=(0, 0, -0.8), text_align=TextNode.ARight, sortOrder=100, text_fg=(1, 0.2, 0.2, 0.7), text_font=CIGlobals.getMickeyFont(), parent=aspect2d)
        self.loading_lbl.hide()
        return

    def begin(self, hood, range, wantGui):
        render.hide()
        self.renderFrames()
        base.setBackgroundColor(0, 0, 0)
        if hood == 'localAvatarEnterGame':
            self.progress_bar['text'] = 'Entering...'
        elif hood == 'init':
            self.progress_bar['text'] = 'Loading...'
        else:
            self.progress_bar['text'] = 'Loading %s...' % hood
        self.progress_bar['text_align'] = TextNode.ALeft
        self.progress_bar['text_pos'] = (-1.01, 0.15)
        self.progress_bar['text_scale'] = (0.095, 0.25)
        self.progress_bar['text_font'] = CIGlobals.getMickeyFont()
        self.progress_bar['text_fg'] = (1, 0.2, 0.2, 0.7)
        self.progress_bar['range'] = range
        self.bg_img.reparentTo(render2d)
        self.logoImg.reparentTo(aspect2d)
        self.progress_bar.reparentTo(aspect2d)
        self.__count = 0
        self.__expectedCount = range
        taskMgr.add(self.renderFramesTask, 'renderFrames')
        self.progress_bar.update(self.__count)

    def renderFramesTask(self, task):
        self.renderFrames()
        return task.cont

    def end(self):
        base.setBackgroundColor(CIGlobals.DefaultBackgroundColor)
        taskMgr.remove('renderFrames')
        render.show()
        self.progress_bar.finish()
        self.bg_img.reparentTo(hidden)
        self.logoImg.reparentTo(hidden)
        self.loading_lbl.hide()
        self.progress_bar.reparentTo(hidden)
        self.renderFrames()

    def destroy(self):
        self.bg_img.destroy()
        self.loading_lbl.destroy()
        self.progress_bar.destroy()
        self.bgm.destroy()
        del self.bg_img
        del self.loading_lbl
        del self.progress_bar
        del self.bgm

    def renderFrames(self):
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()

    def tick(self):
        self.__count += 1
        self.progress_bar.update(self.__count)