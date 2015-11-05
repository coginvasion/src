# Embedded file name: lib.coginvasion.base.ShadowCreator
"""

  Filename: ShadowCreator.py
  Created by: blach (6Apr15)

"""
from pandac.PandaModules import BitMask32, NodePath
from direct.filter.CommonFilters import CommonFilters
from direct.gui.OnscreenImage import OnscreenImage

class ShadowCreator:

    def __init__(self):
        self.shadowBuffer = base.win.makeTextureBuffer('Shadow Buffer', 2048, 2048)
        self.shadowBuffer.setClearColorActive(True)
        self.shadowBuffer.setClearColor((0, 0, 0, 1))
        self.shadowCamera = base.makeCamera(self.shadowBuffer)
        self.shadowCamera.reparentTo(render)
        self.lens = base.camLens
        self.lens.setAspectRatio(1 / 1)
        self.shadowCamera.node().setLens(self.lens)
        self.shadowCamera.node().setCameraMask(BitMask32.bit(1))
        self.initial = NodePath('initial')
        self.initial.setColor(0.75, 0.75, 0.75, 1, 1)
        self.initial.setTextureOff(2)
        self.initial.setMaterialOff(2)
        self.initial.setLightOff(2)
        self.shadowCamera.node().setInitialState(self.initial.getState())
        self.shadowCamera.setPos(-10, 0, 20)
        self.shadowCamera.lookAt(0, 0, 0)
        self.filters = CommonFilters(self.shadowBuffer, self.shadowCamera)
        self.filters.setBlurSharpen(0.1)
        self.shadowTexture = self.shadowBuffer.getTexture()
        self.imageObject = OnscreenImage(image=self.shadowTexture, pos=(-0.75, 0, 0.75), scale=0.2)