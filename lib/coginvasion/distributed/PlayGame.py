# Embedded file name: lib.coginvasion.distributed.PlayGame
"""

  Filename: PlayGame.py
  Created by: blach (28Nov14)

"""
from lib.coginvasion.globals import CIGlobals
from lib.coginvasion.distributed.CogInvasionMsgTypes import *
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.fsm.StateData import StateData
from direct.directnotify.DirectNotifyGlobal import directNotify
from lib.coginvasion.hood import ZoneUtil
from panda3d.core import *
from lib.coginvasion.hood import TTHood
from lib.coginvasion.hood import MGHood
from lib.coginvasion.hood import RecoverHood
from lib.coginvasion.hood.QuietZoneState import QuietZoneState
from lib.coginvasion.dna.DNAParser import *

class PlayGame(StateData):
    notify = directNotify.newCategory('PlayGame')
    Hood2HoodClass = {CIGlobals.ToontownCentral: TTHood.TTHood,
     CIGlobals.MinigameArea: MGHood.MGHood,
     CIGlobals.RecoverArea: RecoverHood.RecoverHood}
    Hood2HoodState = {CIGlobals.ToontownCentral: 'TTHood',
     CIGlobals.MinigameArea: 'MGHood',
     CIGlobals.RecoverArea: 'RecoverHood'}

    def __init__(self, parentFSM, doneEvent):
        StateData.__init__(self, 'playGameDone')
        self.doneEvent = doneEvent
        self.fsm = ClassicFSM('PlayGame', [State('off', self.enterOff, self.exitOff, ['quietZone']),
         State('quietZone', self.enterQuietZone, self.exitQuietZone, ['TTHood', 'MGHood', 'RecoverHood']),
         State('TTHood', self.enterTTHood, self.exitTTHood, ['quietZone']),
         State('MGHood', self.enterMGHood, self.exitMGHood, ['quietZone']),
         State('RecoverHood', self.enterRecoverHood, self.exitRecoverHood, ['quietZone'])], 'off', 'off')
        self.fsm.enterInitialState()
        self.parentFSM = parentFSM
        self.parentFSM.getStateNamed('playGame').addChild(self.fsm)
        self.hoodDoneEvent = 'hoodDone'
        self.hood = None
        self.quietZoneDoneEvent = uniqueName('quietZoneDone')
        self.quietZoneStateData = None
        self.place = None
        self.suitManager = None
        return

    def enter(self, hoodId, zoneId, avId):
        StateData.enter(self)
        whereName = ZoneUtil.getWhereName(zoneId)
        loaderName = ZoneUtil.getLoaderName(zoneId)
        self.fsm.request('quietZone', [{'zoneId': zoneId,
          'hoodId': hoodId,
          'where': whereName,
          'how': 'teleportIn',
          'avId': avId,
          'shardId': None,
          'loader': loaderName}])
        return

    def exit(self):
        StateData.exit(self)

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterTTHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitTTHood(self):
        self.ignore(self.hoodDoneEvent)
        self.hood.exit()
        self.hood.unload()
        self.hood = None
        return

    def enterMGHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitMGHood(self):
        self.ignore(self.hoodDoneEvent)
        self.hood.exit()
        self.hood.unload()
        self.hood = None
        return

    def enterRecoverHood(self, requestStatus):
        print 'entering recover hood'
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitRecoverHood(self):
        self.ignore(self.hoodDoneEvent)
        self.hood.exit()
        self.hood.unload()
        self.hood = None
        return

    def setPlace(self, place):
        self.place = place

    def getPlace(self):
        return self.place

    def loadDNAStore(self):
        if not hasattr(self, 'dnaStore'):
            self.dnaStore = DNAStorage()
            loadDNAFile(self.dnaStore, 'phase_4/dna/storage.dna')
            loadDNAFile(self.dnaStore, 'phase_3.5/dna/storage_interior.dna')

    def enterQuietZone(self, requestStatus):
        self.acceptOnce(self.quietZoneDoneEvent, self.handleQuietZoneDone)
        self.quietZoneStateData = QuietZoneState(self.quietZoneDoneEvent)
        self.quietZoneStateData.load()
        self.quietZoneStateData.enter(requestStatus)
        self._enterWaitForSetZoneResponseMsg = self.quietZoneStateData.getEnterWaitForSetZoneResponseMsg()
        self.acceptOnce(self._enterWaitForSetZoneResponseMsg, self.handleWaitForSetZoneResponse)

    def handleWaitForSetZoneResponse(self, requestStatus):
        hoodId = requestStatus['hoodId']
        hoodClass = self.Hood2HoodClass[hoodId]
        base.transitions.noTransitions()
        loader.beginBulkLoad('hood', hoodId, 100)
        self.loadDNAStore()
        self.hood = hoodClass(self.fsm, self.hoodDoneEvent, self.dnaStore, hoodId)
        self.hood.load()

    def handleLeftQuietZone(self):
        status = self.quietZoneStateData.getRequestStatus()
        hoodId = status['hoodId']
        hoodState = self.Hood2HoodState[hoodId]
        self.fsm.request(hoodState, [status])
        loader.endBulkLoad('hood')

    def handleQuietZoneDone(self):
        self.handleLeftQuietZone()

    def handleHoodDone(self):
        doneStatus = self.hood.getDoneStatus()
        if doneStatus['zoneId'] == None:
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
        else:
            self.fsm.request('quietZone', [doneStatus])
        return

    def exitQuietZone(self):
        self.ignore(self.quietZoneDoneEvent)
        self.ignore(self._enterWaitForSetZoneResponseMsg)
        self.quietZoneStateData.exit()
        self.quietZoneStateData.unload()
        del self._enterWaitForSetZoneResponseMsg
        self.quietZoneStateData = None
        return