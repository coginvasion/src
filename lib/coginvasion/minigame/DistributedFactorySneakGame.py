# Embedded file name: lib.coginvasion.minigame.DistributedFactorySneakGame
from direct.directnotify.DirectNotifyGlobal import directNotify
from lib.coginvasion.globals import CIGlobals
from DistributedToonFPSGame import DistributedToonFPSGame
from FactorySneakWorld import FactorySneakWorld

class DistributedFactorySneakGame(DistributedToonFPSGame):
    notify = directNotify.newCategory('DistributedFactorySneakGame')

    def __init__(self, cr):
        DistributedToonFPSGame.__init__(self, cr)
        self.gameWorld = None
        return

    def load(self):
        self.setMinigameMusic('phase_4/audio/bgm/MG_Escape.mp3')
        self.setDescription('Sneak around the Sellbot Factory and collect jellybean barrels. Avoid the guards and exit by the Factory Foreman to redeem your jellybeans.')
        DistributedToonFPSGame.load(self)

    def enterPlay(self):
        self.gameWorld.enablePlayerControls()
        DistributedToonFPSGame.enterPlay(self)

    def exitPlay(self):
        DistributedToonFPSGame.exitPlay(self)
        self.gameWorld.disablePlayerControls()

    def announceGenerate(self):
        DistributedToonFPSGame.announceGenerate(self)
        base.camLens.setMinFov(CIGlobals.GunGameFOV / (4.0 / 3.0))
        base.camLens.setFar(250)
        self.gameWorld = FactorySneakWorld(self)
        self.gameWorld.loadWorld()
        self.gameWorld.loadJellybeanBarrels()
        self.gameWorld.makeGuards()
        self.gameWorld.showWorld()
        self.gameWorld.setupPlayer()
        self.load()

    def disable(self):
        if self.gameWorld:
            self.gameWorld.cleanup()
            self.gameWorld = None
        base.camLens.setMinFov(CIGlobals.DefaultCameraFov / (4.0 / 3.0))
        base.camLens.setFar(CIGlobals.DefaultCameraFar)
        DistributedToonFPSGame.disable(self)
        return