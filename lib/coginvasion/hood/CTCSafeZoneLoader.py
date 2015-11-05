# Embedded file name: lib.coginvasion.hood.CTCSafeZoneLoader
"""

  Filename: CTCSafeZoneLoader.py
  Created by: blach (14Dec14)

"""
from pandac.PandaModules import *
from direct.actor.Actor import Actor
import SafeZoneLoader
import CTCPlayground
import random

class CTCSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playground = CTCPlayground.CTCPlayground
        self.pgMusicFilename = 'phase_4/audio/bgm/TC_nbrhood.mid'
        self.interiorMusicFilename = 'phase_3.5/audio/bgm/TC_SZ_activity.mid'
        self.battleMusicFile = 'phase_3.5/audio/bgm/encntr_general_bg.mid'
        self.invasionMusicFiles = ['phase_12/audio/bgm/BossBot_CEO_v1.mid', 'phase_9/audio/bgm/encntr_suit_winning.mid']
        self.tournamentMusicFiles = ['phase_3.5/audio/bgm/encntr_nfsmw_bg_1.mp3',
         'phase_3.5/audio/bgm/encntr_nfsmw_bg_2.mp3',
         'phase_3.5/audio/bgm/encntr_nfsmw_bg_3.mp3',
         'phase_3.5/audio/bgm/encntr_nfsmw_bg_4.mp3']
        self.bossBattleMusicFile = 'phase_7/audio/bgm/encntr_suit_winning_indoor.mid'
        self.dnaFile = 'phase_4/dna/cog_toontown_central_sz.dna'
        self.szStorageDNAFile = 'phase_4/dna/storage_TT_sz.dna'
        self.telescope = None
        self.birdNoises = ['phase_4/audio/sfx/SZ_TC_bird1.mp3', 'phase_4/audio/sfx/SZ_TC_bird2.mp3', 'phase_4/audio/sfx/SZ_TC_bird3.mp3']
        return

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.geom.find('**/hill').setTransparency(TransparencyAttrib.MBinary, 1)

    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)

    def createSafeZone(self, dnaFile):
        loader.loadDNAFile(self.hood.dnaStore, 'phase_5/dna/storage_town.dna')
        SafeZoneLoader.SafeZoneLoader.createSafeZone(self, dnaFile)

    def enter(self, requestStatus):
        SafeZoneLoader.SafeZoneLoader.enter(self, requestStatus)
        taskMgr.add(self.telescopeTask, 'CTCSafeZoneLoader-telescopeTask')

    def telescopeTask(self, task):
        if self.telescope:
            self.telescope.play('chan')
            task.delayTime = 12.0
            return task.again
        else:
            return task.done

    def exit(self):
        taskMgr.remove('CTCSafeZoneLoader-telescopeTask')
        SafeZoneLoader.SafeZoneLoader.exit(self)