# Embedded file name: lib.coginvasion.hood.BRSafeZoneLoader
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.actor.Actor import Actor
from lib.coginvasion.toon import ParticleLoader
import SafeZoneLoader
import BRPlayground

class BRSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):
    notify = directNotify.newCategory('BRSafeZoneLoader')

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playground = BRPlayground.BRPlayground
        self.pgMusicFilename = 'phase_8/audio/bgm/TB_nbrhood.mid'
        self.interiorMusicFilename = 'phase_8/audio/bgm/TB_SZ_activity.mid'
        self.battleMusicFile = 'phase_3.5/audio/bgm/encntr_general_bg.mid'
        self.invasionMusicFiles = ['phase_12/audio/bgm/BossBot_CEO_v1.mid', 'phase_9/audio/bgm/encntr_suit_winning.mid']
        self.tournamentMusicFiles = ['phase_3.5/audio/bgm/encntr_nfsmw_bg_1.mp3',
         'phase_3.5/audio/bgm/encntr_nfsmw_bg_2.mp3',
         'phase_3.5/audio/bgm/encntr_nfsmw_bg_3.mp3',
         'phase_3.5/audio/bgm/encntr_nfsmw_bg_4.mp3']
        self.bossBattleMusicFile = 'phase_7/audio/bgm/encntr_suit_winning_indoor.mid'
        self.dnaFile = 'phase_8/dna/the_burrrgh_sz.dna'
        self.szStorageDNAFile = 'phase_8/dna/storage_BR_sz.dna'
        self.telescope = None
        self.snow = None
        self.windNoises = ['phase_8/audio/sfx/SZ_TB_wind_1.mp3', 'phase_8/audio/sfx/SZ_TB_wind_2.mp3', 'phase_8/audio/sfx/SZ_TB_wind_3.mp3']
        return

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.snow = ParticleLoader.loadParticleEffect('phase_8/etc/snowdisk.ptf')
        self.snow.setPos(0, 0, 5)
        self.snowRender = self.geom.attachNewNode('snowRender')
        self.snowRender.setDepthWrite(0)
        self.snowRender.setBin('fixed', 1)
        hq = self.geom.find('**/*toon_landmark_hqBR*')
        hq.find('**/doorFrameHoleLeft_0').stash()
        hq.find('**/doorFrameHoleRight_0').stash()
        hq.find('**/doorFrameHoleLeft_1').stash()
        hq.find('**/doorFrameHoleRight_1').stash()

    def unload(self):
        self.snow = None
        del self.snowRender
        SafeZoneLoader.SafeZoneLoader.unload(self)
        return

    def enter(self, requestStatus):
        SafeZoneLoader.SafeZoneLoader.enter(self, requestStatus)
        self.snow.start(parent=camera, renderParent=self.snowRender)

    def exit(self):
        self.snow.cleanup()
        self.snowRender.removeNode()
        SafeZoneLoader.SafeZoneLoader.exit(self)