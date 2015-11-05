# Embedded file name: lib.coginvasion.hood.SafeZoneLoader
"""

  Filename: SafeZoneLoader.py
  Created by: blach (14Dec14)

"""
from pandac.PandaModules import *
from direct.fsm.StateData import StateData
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from QuietZoneState import QuietZoneState
from lib.coginvasion.manager.SettingsManager import SettingsManager
from direct.directnotify.DirectNotifyGlobal import directNotify
from lib.coginvasion.base.ShadowCreator import ShadowCreator

class SafeZoneLoader(StateData):
    notify = directNotify.newCategory('SafeZoneLoader')

    def __init__(self, hood, parentFSMState, doneEvent):
        StateData.__init__(self, doneEvent)
        self.hood = hood
        self.parentFSMState = parentFSMState
        self.fsm = ClassicFSM('safeZoneLoader', [State('off', self.enterOff, self.exitOff), State('playground', self.enterPlayground, self.exitPlayground, ['quietZone']), State('quietZone', self.enterQuietZone, self.exitQuietZone, ['playground'])], 'off', 'off')
        self.placeDoneEvent = 'placeDone'
        self.place = None
        self.playground = None
        self.battleMusic = None
        self.invasionMusic = None
        self.invasionMusicFiles = None
        self.interiorMusic = None
        self.bossBattleMusic = None
        self.music = None
        return

    def load(self):
        StateData.load(self)
        if self.pgMusicFilename:
            self.music = base.loadMusic(self.pgMusicFilename)
        if self.battleMusicFile:
            self.battleMusic = base.loadMusic(self.battleMusicFile)
        if self.invasionMusicFiles:
            self.invasionMusic = None
        if self.bossBattleMusicFile:
            self.bossBattleMusic = base.loadMusic(self.bossBattleMusicFile)
        if self.interiorMusicFilename:
            self.interiorMusic = base.loadMusic(self.interiorMusicFilename)
        self.createSafeZone(self.dnaFile)
        self.parentFSMState.addChild(self.fsm)
        width, height, fs, music, sfx, tex_detail, model_detail, aa, af = SettingsManager().getSettings('settings.json')
        if af == 'on':
            self.notify.info('Anisotropic Filtering is on, applying to textures.')
            for nodepath in self.geom.findAllMatches('*'):
                try:
                    for node in nodepath.findAllMatches('**'):
                        try:
                            node.findTexture('*').setAnisotropicDegree(8)
                        except:
                            pass

                except:
                    continue

        return

    def unload(self):
        StateData.unload(self)
        self.parentFSMState.removeChild(self.fsm)
        del self.parentFSMState
        self.geom.removeNode()
        del self.geom
        del self.fsm
        del self.hood
        del self.playground
        del self.music
        del self.interiorMusic
        del self.battleMusic
        del self.bossBattleMusic
        self.ignoreAll()
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()

    def enter(self, requestStatus):
        StateData.enter(self)
        self.fsm.enterInitialState()
        messenger.send('enterSafeZone')
        self.setState(requestStatus['where'], requestStatus)
        partyGate = self.geom.find('**/prop_party_gate_DNARoot')
        if not partyGate.isEmpty():
            partyGate.removeNode()
        del partyGate
        petShop = self.geom.find('**/prop_pet_shop_DNARoot')
        if not petShop.isEmpty():
            petShop.removeNode()
        del petShop

    def exit(self):
        StateData.exit(self)
        messenger.send('exitSafeZone')

    def setState(self, stateName, requestStatus):
        self.fsm.request(stateName, [requestStatus])

    def createSafeZone(self, dnaFile):
        if self.szStorageDNAFile:
            loader.loadDNAFile(self.hood.dnaStore, self.szStorageDNAFile)
        node = loader.loadDNAFile(self.hood.dnaStore, dnaFile)
        if node.getNumParents() == 1:
            self.geom = NodePath(node.getParent(0))
            self.geom.reparentTo(hidden)
        else:
            self.geom = hidden.attachNewNode(node)
        self.geom.flattenMedium()
        gsg = base.win.getGsg()
        if gsg:
            self.geom.prepareScene(gsg)

    def enterPlayground(self, requestStatus):
        self.acceptOnce(self.placeDoneEvent, self.handlePlaygroundDone)
        self.place = self.playground(self, self.fsm, self.placeDoneEvent)
        self.place.load()
        self.place.enter(requestStatus)
        base.cr.playGame.setPlace(self.place)

    def exitPlayground(self):
        self.ignore(self.placeDoneEvent)
        self.place.exit()
        self.place.unload()
        self.place = None
        base.cr.playGame.setPlace(self.place)
        return

    def handlePlaygroundDone(self):
        status = self.place.doneStatus
        print self.hood.isSameHood(status)
        if self.hood.isSameHood(status) and status['where'] != 'minigame':
            self.fsm.request('quietZone', [status])
        else:
            self.doneStatus = status
            messenger.send(self.doneEvent)

    def enterQuietZone(self, requestStatus):
        self.quietZoneDoneEvent = uniqueName('quietZoneDone')
        self.acceptOnce(self.quietZoneDoneEvent, self.handleQuietZoneDone)
        self.quietZoneStateData = QuietZoneState(self.quietZoneDoneEvent)
        self.quietZoneStateData.load()
        self.quietZoneStateData.enter(requestStatus)

    def exitQuietZone(self):
        self.ignore(self.quietZoneDoneEvent)
        del self.quietZoneDoneEvent
        self.quietZoneStateData.exit()
        self.quietZoneStateData.unload()
        self.quietZoneStateData = None
        return

    def handleQuietZoneDone(self):
        status = self.quietZoneStateData.getDoneStatus()
        if status['where'] == 'estate':
            self.doneStatus = status
            messenger.send(self.doneEvent)
        else:
            self.fsm.request(status['where'], [status])

    def enterOff(self):
        pass

    def exitOff(self):
        pass