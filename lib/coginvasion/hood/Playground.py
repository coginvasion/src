# Embedded file name: lib.coginvasion.hood.Playground
"""

  Filename: Playground.py
  Created by: blach (14Dec14)

"""
import Place
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.directnotify.DirectNotifyGlobal import directNotify
from lib.coginvasion.book.ShtickerBook import ShtickerBook
from lib.coginvasion.globals import CIGlobals

class Playground(Place.Place):
    notify = directNotify.newCategory('Playground')

    def __init__(self, loader, parentFSM, doneEvent):
        Place.Place.__init__(self, loader, doneEvent)
        self.fsm = ClassicFSM('Playground', [State('start', self.enterStart, self.exitStart, ['walk', 'teleportIn']),
         State('teleportIn', self.enterTeleportIn, self.exitTeleportIn, ['walk']),
         State('walk', self.enterWalk, self.exitWalk, ['teleportOut',
          'stop',
          'shtickerBook',
          'died']),
         State('teleportOut', self.enterTeleportOut, self.exitTeleportOut, ['teleportIn', 'stop']),
         State('stop', self.enterStop, self.exitStop, ['walk', 'died']),
         State('shtickerBook', self.enterShtickerBook, self.exitShtickerBook, ['teleportOut', 'walk']),
         State('final', self.enterFinal, self.exitFinal, ['start']),
         State('died', self.enterDied, self.exitDied, ['final'])], 'start', 'final')
        self.parentFSM = parentFSM

    def enter(self, requestStatus):
        self.fsm.enterInitialState()
        messenger.send('enterPlayground')
        if self.loader.music:
            base.playMusic(self.loader.music, looping=1, volume=0.8)
        self.loader.geom.reparentTo(render)
        self.loader.hood.startSky()
        self.zoneId = requestStatus['zoneId']
        if base.cr.playGame.suitManager:
            base.cr.playGame.suitManager.d_requestSuitInfo()
        how = requestStatus['how']
        self.fsm.request(how, [requestStatus])

    def exit(self):
        self.ignoreAll()
        messenger.send('exitPlayground')
        self.loader.geom.reparentTo(hidden)
        self.loader.hood.stopSky()
        if self.loader.music:
            self.loader.music.stop()
        if self.loader.bossBattleMusic:
            self.loader.bossBattleMusic.stop()
        if self.loader.battleMusic:
            self.loader.battleMusic.stop()
        if self.loader.invasionMusic:
            self.loader.invasionMusic.stop()

    def load(self):
        Place.Place.load(self)
        self.parentFSM.getStateNamed('playground').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('playground').removeChild(self.fsm)
        del self.parentFSM
        del self.fsm
        self.ignoreAll()
        Place.Place.unload(self)

    def enterWalk(self, teleportIn = 0):
        Place.Place.enterWalk(self, teleportIn)
        if base.localAvatar.zoneId != CIGlobals.RecoverAreaId:
            base.localAvatar.startMonitoringHP()

    def exitWalk(self):
        if base.localAvatar.zoneId != CIGlobals.RecoverAreaId:
            base.localAvatar.stopMonitoringHP()
        Place.Place.exitWalk(self)

    def maybeUpdateAdminPage(self):
        if self.fsm.getCurrentState().getName() == 'shtickerBook':
            if hasattr(self, 'shtickerBookStateData'):
                if self.shtickerBookStateData.fsm.getCurrentState().getName() == 'adminPage':
                    if base.cr.playGame.suitManager:
                        text2Change2 = 'Turn Suit Spawner '
                        if base.cr.playGame.suitManager.getSpawner():
                            text2Change2 += 'Off'
                        else:
                            text2Change2 += 'On'
                        self.shtickerBookStateData.adminPageStateData.suitSpawnerBtn['text'] = text2Change2

    def enterShtickerBook(self):
        base.localAvatar.attachCamera()
        base.localAvatar.createLaffMeter()
        base.localAvatar.startSmartCamera()
        base.localAvatar.startPosHprBroadcast()
        base.localAvatar.d_broadcastPositionNow()
        base.localAvatar.b_setAnimState('openBook', self.enterShtickerBookGui)

    def enterShtickerBookGui(self):
        doneEvent = 'shtickerBookDone'
        self.shtickerBookStateData = ShtickerBook(self.fsm, doneEvent)
        self.acceptOnce(doneEvent, self.__shtickerBookDone)
        self.shtickerBookStateData.load()
        self.shtickerBookStateData.enter()
        base.localAvatar.showBookButton(1)
        base.localAvatar.b_setAnimState('readBook')

    def __shtickerBookDone(self):
        doneStatus = self.shtickerBookStateData.getDoneStatus()
        base.localAvatar.hideBookButton()
        self.shtickerBookStateData.exit()
        if doneStatus['mode'] == 'exit':
            base.localAvatar.b_setAnimState('closeBook', self.__handleBookCloseExit)
        elif doneStatus['mode'] == 'teleport':
            base.localAvatar.b_setAnimState('closeBook', self.__handleBookCloseTeleport, [doneStatus])
        elif doneStatus['mode'] == 'resume':
            base.localAvatar.b_setAnimState('closeBook', self.__handleBookCloseResume)

    def __handleBookCloseResume(self):
        self.fsm.request('walk')

    def __handleBookCloseTeleport(self, requestStatus):
        self.fsm.request('teleportOut', [requestStatus])

    def __handleBookCloseExit(self):
        base.localAvatar.b_setAnimState('teleportOut', self.__handleBookExitTeleport)

    def __handleBookExitTeleport(self):
        base.transitions.fadeOut(0.0)
        base.cr.gameFSM.request('closeShard')

    def exitShtickerBook(self):
        base.localAvatar.detachCamera()
        base.localAvatar.stopSmartCamera()
        base.localAvatar.stopPosHprBroadcast()
        base.localAvatar.disableLaffMeter()
        self.ignore(self.shtickerBookStateData.doneEvent)
        self.shtickerBookStateData.exit()
        self.shtickerBookStateData.unload()
        del self.shtickerBookStateData
        base.localAvatar.hideBookButton()

    def enterTeleportOut(self, requestStatus):
        Place.Place.enterTeleportOut(self, self.__teleportOutDone, requestStatus)

    def __teleportOutDone(self, requestStatus):
        self.doneStatus = requestStatus
        messenger.send(self.doneEvent)

    def enterTeleportIn(self, requestStatus):
        requestStatus['nextState'] = 'walk'
        x, y, z, h, p, r = base.cr.hoodMgr.getPlaygroundCenterFromId(self.loader.hood.id)
        base.localAvatar.detachNode()
        base.localAvatar.setPosHpr(render, x, y, z, h, p, r)
        Place.Place.enterTeleportIn(self, requestStatus)