# Embedded file name: lib.coginvasion.hood.TTSafeZoneLoader
from pandac.PandaModules import *
from direct.actor.Actor import Actor
import SafeZoneLoader
import TTPlayground
import random
from lib.coginvasion.globals import CIGlobals

class TTSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playground = TTPlayground.TTPlayground
        self.pgMusicFilename = 'phase_4/audio/bgm/TC_nbrhood.mid'
        self.interiorMusicFilename = 'phase_3.5/audio/bgm/TC_SZ_activity.mid'
        self.battleMusicFile = 'phase_3.5/audio/bgm/encntr_general_bg.mid'
        self.invasionMusicFiles = ['phase_12/audio/bgm/BossBot_CEO_v1.mid', 'phase_9/audio/bgm/encntr_suit_winning.mid']
        self.tournamentMusicFiles = ['phase_3.5/audio/bgm/encntr_nfsmw_bg_1.mp3',
         'phase_3.5/audio/bgm/encntr_nfsmw_bg_2.mp3',
         'phase_3.5/audio/bgm/encntr_nfsmw_bg_3.mp3',
         'phase_3.5/audio/bgm/encntr_nfsmw_bg_4.mp3']
        self.bossBattleMusicFile = 'phase_7/audio/bgm/encntr_suit_winning_indoor.mid'
        self.dnaFile = 'phase_4/dna/new_ttc_sz.dna'
        self.szStorageDNAFile = 'phase_4/dna/storage_TT_sz.dna'
        self.telescope = None
        self.birdNoises = ['phase_4/audio/sfx/SZ_TC_bird1.mp3', 'phase_4/audio/sfx/SZ_TC_bird2.mp3', 'phase_4/audio/sfx/SZ_TC_bird3.mp3']
        return

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.geom.find('**/toontown_central_beta_DNARoot').setTwoSided(1)
        self.geom.find('**/ground_center').setBin('ground', 18)
        self.geom.find('**/ground_sidewalk').setBin('ground', 18)
        self.geom.find('**/ground').setBin('ground', 18)
        self.geom.find('**/ground_center_coll').setCollideMask(CIGlobals.FloorBitmask)
        self.geom.find('**/ground_sidewalk_coll').setCollideMask(CIGlobals.FloorBitmask)
        for tunnel in self.geom.findAllMatches('**/linktunnel_tt*'):
            tunnel.find('**/tunnel_floor_1').setTexture(loader.loadTexture('phase_4/models/neighborhoods/tex/sidewalkbrown.jpg'), 1)

        for tree in self.geom.findAllMatches('**/prop_green_tree_*_DNARoot'):
            newShadow = loader.loadModel('phase_3/models/props/drop_shadow.bam')
            newShadow.reparentTo(tree)
            newShadow.setScale(1.5)
            newShadow.setColor(0, 0, 0, 0.5, 1)