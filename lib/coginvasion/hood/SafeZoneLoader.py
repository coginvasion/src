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
import ToonInterior
import LinkTunnel

class SafeZoneLoader(StateData):
    notify = directNotify.newCategory('SafeZoneLoader')

    def __init__(self, hood, parentFSMState, doneEvent):
        StateData.__init__(self, doneEvent)
        self.hood = hood
        self.parentFSMState = parentFSMState
        self.fsm = ClassicFSM('safeZoneLoader', [State('off', self.enterOff, self.exitOff),
         State('playground', self.enterPlayground, self.exitPlayground, ['quietZone']),
         State('toonInterior', self.enterToonInterior, self.exitToonInterior, ['quietZone']),
         State('quietZone', self.enterQuietZone, self.exitQuietZone, ['playground', 'toonInterior'])], 'off', 'off')
        self.placeDoneEvent = 'placeDone'
        self.place = None
        self.playground = None
        self.battleMusic = None
        self.invasionMusic = None
        self.invasionMusicFiles = None
        self.interiorMusic = None
        self.bossBattleMusic = None
        self.music = None
        self.tournamentMusic = None
        self.linkTunnels = []
        return

    def findAndMakeLinkTunnels(self):
        for tunnel in self.geom.findAllMatches('**/*linktunnel*'):
            dnaRootStr = tunnel.getName()
            link = LinkTunnel.SafeZoneLinkTunnel(tunnel, dnaRootStr)
            self.linkTunnels.append(link)

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
        if self.tournamentMusicFiles:
            self.tournamentMusic = None
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
        del self.tournamentMusic
        self.ignoreAll()
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()

    def enter(self, requestStatus):
        StateData.enter(self)
        if base.localAvatar.zoneId < 61000:
            self.findAndMakeLinkTunnels()
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
        for link in self.linkTunnels:
            link.cleanup()

        self.linkTunnels = []

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
        self.makeDictionaries(self.hood.dnaStore)
        if self.__class__.__name__ not in ('TTSafeZoneLoader',):
            self.geom.flattenMedium()
        gsg = base.win.getGsg()
        if gsg:
            self.geom.prepareScene(gsg)

    def makeDictionaries(self, dnaStore):
        self.nodeList = []
        for i in xrange(dnaStore.getNumDNAVisGroups()):
            groupFullName = dnaStore.getDNAVisGroupName(i)
            groupName = base.cr.hoodMgr.extractGroupName(groupFullName)
            groupNode = self.geom.find('**/' + groupFullName)
            if groupNode.isEmpty():
                self.notify.error('Could not find visgroup')
            if self.__class__.__name__ not in ('TTSafeZoneLoader',):
                groupNode.flattenMedium()
            self.nodeList.append(groupNode)

        self.hood.dnaStore.resetPlaceNodes()
        self.hood.dnaStore.resetDNAGroups()
        self.hood.dnaStore.resetDNAVisGroups()
        self.hood.dnaStore.resetDNAVisGroupsAI()

    def enterPlayground(self, requestStatus):
        try:
            self.hood.stopSuitEffect()
        except:
            pass

        self.acceptOnce(self.placeDoneEvent, self.handlePlaygroundDone)
        self.place = self.playground(self, self.fsm, self.placeDoneEvent)
        self.place.load()

    def exitPlayground(self):
        self.ignore(self.placeDoneEvent)
        self.place.exit()
        self.place.unload()
        self.place = None
        base.cr.playGame.setPlace(self.place)
        return

    def handlePlaygroundDone(self):
        status = self.place.doneStatus
        if self.hood.isSameHood(status) and status['loader'] == 'safeZoneLoader' and status['where'] not in ('minigame',):
            self.fsm.request('quietZone', [status])
        else:
            self.doneStatus = status
            messenger.send(self.doneEvent)

    def enterToonInterior(self, requestStatus):
        self.acceptOnce(self.placeDoneEvent, self.handleToonInteriorDone)
        self.place = ToonInterior.ToonInterior(self, self.fsm, self.placeDoneEvent)
        self.place.load()

    def enterThePlace(self, requestStatus):
        base.cr.playGame.setPlace(self.place)
        self.place.enter(requestStatus)

    def exitToonInterior(self):
        self.ignore(self.placeDoneEvent)
        self.place.exit()
        self.place.unload()
        self.place = None
        base.cr.playGame.setPlace(self.place)
        return

    def handleToonInteriorDone(self):
        status = self.place.doneStatus
        if status['loader'] == 'safeZoneLoader' and self.hood.isSameHood(status) and status['shardId'] == None or status['how'] == 'doorOut':
            self.fsm.request('quietZone', [status])
        else:
            self.doneStatus = status
            messenger.send(self.doneEvent)
        return

    def enterQuietZone(self, requestStatus):
        self.fsm.request(requestStatus['where'], [requestStatus], exitCurrent=0)
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
        self.exitQuietZone()
        if status['where'] == 'estate' or status['loader'] == 'townLoader':
            self.doneStatus = status
            messenger.send(self.doneEvent)
        else:
            self.enterThePlace(status)

    def enterOff(self):
        pass

    def exitOff(self):
        pass