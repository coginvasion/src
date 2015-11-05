# Embedded file name: lib.coginvasion.hood.MGSafeZoneLoader
"""

  Filename: MGSafeZoneLoader.py
  Created by: blach (5Jan15)

"""
from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import directNotify
import SafeZoneLoader
import MGPlayground
import random

class MGSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):
    notify = directNotify.newCategory('MGSafeZoneLoader')

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playground = MGPlayground.MGPlayground
        self.pgMusicFilename = 'phase_13/audio/bgm/party_original_theme.mid'
        self.interiorMusicFilename = None
        self.battleMusicFile = None
        self.invasionMusicFiles = None
        self.bossBattleMusicFile = None
        self.dnaFile = 'phase_13/dna/party_sz.dna'
        self.szStorageDNAFile = 'phase_13/dna/storage_party_sz.dna'
        return

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)

    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)

    def enter(self, requestStatus):
        SafeZoneLoader.SafeZoneLoader.enter(self, requestStatus)

    def exit(self):
        """
        render.clearLight(self.light)
        render.clearLight(self.amb)
        """
        SafeZoneLoader.SafeZoneLoader.exit(self)