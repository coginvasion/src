# Embedded file name: lib.coginvasion.hood.DLSafeZoneLoader
from direct.directnotify.DirectNotifyGlobal import directNotify
from SafeZoneLoader import SafeZoneLoader
from DLPlayground import DLPlayground

class DLSafeZoneLoader(SafeZoneLoader):
    notify = directNotify.newCategory('DLSafeZoneLoader')

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playground = DLPlayground
        self.pgMusicFilename = 'phase_8/audio/bgm/DL_nbrhood.mid'
        self.interiorMusicFilename = 'phase_8/audio/bgm/DL_SZ_activity.mid'
        self.battleMusicFile = 'phase_3.5/audio/bgm/encntr_general_bg.mid'
        self.invasionMusicFiles = ['phase_12/audio/bgm/BossBot_CEO_v1.mid', 'phase_9/audio/bgm/encntr_suit_winning.mid']
        self.tournamentMusicFiles = ['phase_3.5/audio/bgm/encntr_nfsmw_bg_1.mp3',
         'phase_3.5/audio/bgm/encntr_nfsmw_bg_2.mp3',
         'phase_3.5/audio/bgm/encntr_nfsmw_bg_3.mp3',
         'phase_3.5/audio/bgm/encntr_nfsmw_bg_4.mp3']
        self.bossBattleMusicFile = 'phase_7/audio/bgm/encntr_suit_winning_indoor.mid'
        self.dnaFile = 'phase_8/dna/donalds_dreamland_sz.dna'
        self.szStorageDNAFile = 'phase_8/dna/storage_DL_sz.dna'
        self.telescope = None
        return

    def load(self):
        SafeZoneLoader.load(self)
        hq = self.geom.find('**/*toon_landmark_hqDL*')
        hq.find('**/doorFrameHoleLeft_0').stash()
        hq.find('**/doorFrameHoleRight_0').stash()
        hq.find('**/doorFrameHoleLeft_1').stash()
        hq.find('**/doorFrameHoleRight_1').stash()