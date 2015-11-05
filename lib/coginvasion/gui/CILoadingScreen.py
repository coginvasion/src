# Embedded file name: lib.coginvasion.gui.CILoadingScreen
"""
  
  Filename: CILoadingScreen.py
  Created by: blach (17June14)
  
"""
from lib.coginvasion.base.CIStart import *
from lib.coginvasion.globals import CIGlobals
from panda3d.core import *
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.directnotify.DirectNotify import *
from direct.showbase.Transitions import Transitions
from lib.coginvasion.base import FileUtility
import glob
loadernotify = DirectNotify().newCategory('CILoadingScreen')

class CILoadingScreen:

    def __init__(self):
        self.transitions = Transitions(loader)

    def createMenu(self):
        """
        self.menuBg = loader.loadModel("phase_3/models/gui/loading-background.bam")
        self.menuBg.find('**/fg').removeNode()
        
        #self.trolleyTex = loader.loadTexture("phase_3.5/maps/trolley.jpg", "phase_3.5/maps/trolley_a.rgb")
        #self.trolley = OnscreenImage(image=self.trolleyTex, scale=(0.5, 0, 0.6))
        #self.trolley.setTransparency(True)
        
        #self.logo = loader.loadTexture("phase_3/maps/toontown_online_logo.tif")
        #self.logoImg = OnscreenImage(image=self.logo, scale=(0.6, 0, 0.225), pos=(0, 0, 0.5))
        #self.logoImg.setTransparency(True)
        
        self.logo = loader.loadTexture("phase_3/maps/CogInvasion_Logo.png")
        self.logoImg = OnscreenImage(image = self.logo, scale = (1.0, 0, 0.6))
        self.logoImg.setTransparency(True)
        self.logoImg.reparentTo(hidden)
        
        self.bg_img = OnscreenImage(image=self.menuBg, parent=render2d)
        """
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        self.version_lbl = OnscreenText(text='ver-' + game.version, scale=0.06, pos=(-1.32, -0.97, -0.97), align=TextNode.ALeft, fg=(0.9, 0.9, 0.9, 7))

    def beginLoadGame(self):
        phasesToScan = ['models',
         'phase_3/models',
         'phase_3.5/models',
         'phase_4/models']
        self.models = FileUtility.findAllModelFilesInVFS(phasesToScan)
        for model in self.models:
            loader.loadModel(model)
            loader.progressScreen.tick()

        doneInitLoad()
        self.destroy()

    def loadModelDone(self, array):
        self.modelsLoaded += 1
        if self.modelsLoaded == len(self.models):
            doneInitLoad()
            self.destroy()

    def destroy(self):
        self.version_lbl.destroy()