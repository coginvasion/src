# Embedded file name: lib.coginvasion.hood.Place
"""

  Filename: Place.py
  Created by: blach (15Dec14)
  
  Description: Handles the avatar events that happen while the avatar is
               in a place such as a playground.

"""
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.fsm.StateData import StateData
from direct.directnotify.DirectNotifyGlobal import directNotify
from lib.coginvasion.globals import CIGlobals
from PublicWalk import PublicWalk

class Place(StateData):
    notify = directNotify.newCategory('Place')

    def __init__(self, loader, doneEvent):
        StateData.__init__(self, doneEvent)
        self.loader = loader
        self.zoneId = None
        return

    def enterStart(self):
        pass

    def exitStart(self):
        pass

    def enterFinal(self):
        pass

    def exitFinal(self):
        pass

    def enterStop(self):
        base.localAvatar.b_setAnimState('neutral')
        base.localAvatar.attachCamera()
        base.localAvatar.createLaffMeter()
        base.localAvatar.createMoney()
        base.localAvatar.enablePies(0)

    def exitStop(self):
        base.localAvatar.detachCamera()
        base.localAvatar.disableLaffMeter()
        base.localAvatar.disableMoney()
        base.localAvatar.disablePies()

    def load(self):
        StateData.load(self)
        self.walkDoneEvent = 'walkDone'
        self.walkStateData = PublicWalk(self.fsm, self.walkDoneEvent)
        self.walkStateData.load()

    def unload(self):
        StateData.unload(self)
        del self.walkDoneEvent
        self.walkStateData.unload()
        del self.walkStateData
        del self.loader

    def enterTeleportIn(self, requestStatus):
        base.transitions.irisIn()
        self.nextState = requestStatus.get('nextState', 'walk')
        base.localAvatar.attachCamera()
        base.localAvatar.startSmartCamera()
        base.localAvatar.startPosHprBroadcast()
        globalClock.tick()
        base.localAvatar.b_setAnimState('teleportIn', callback=self.teleportInDone)
        base.localAvatar.d_broadcastPositionNow()
        base.localAvatar.b_setParent(CIGlobals.SPRender)

    def exitTeleportIn(self):
        base.localAvatar.stopSmartCamera()
        base.localAvatar.detachCamera()
        base.localAvatar.stopPosHprBroadcast()

    def teleportInDone(self):
        if hasattr(self, 'fsm'):
            self.fsm.request(self.nextState, [1])

    def enterDied(self, requestStatus, callback = None):
        if callback == None:
            callback = self.__diedDone
        base.localAvatar.createLaffMeter()
        base.localAvatar.attachCamera()
        base.localAvatar.b_setAnimState('died', callback, [requestStatus])
        return

    def __diedDone(self, requestStatus):
        self.doneStatus = requestStatus
        messenger.send(self.doneEvent)

    def exitDied(self):
        base.localAvatar.disableLaffMeter()
        base.localAvatar.detachCamera()

    def enterWalk(self, teleportIn = 0):
        self.walkStateData.enter()
        if teleportIn == 0:
            self.walkStateData.fsm.request('walking')
        self.acceptOnce(self.walkDoneEvent, self.handleWalkDone)
        self.walkStateData.fsm.request('walking')

    def exitWalk(self):
        self.walkStateData.exit()
        self.ignore(self.walkDoneEvent)
        if base.cr.playGame.hood.titleText != None:
            base.cr.playGame.hood.hideTitleText()
        return

    def handleWalkDone(self, doneStatus):
        pass

    def enterTeleportOut(self, callback, requestStatus):
        base.localAvatar.attachCamera()
        base.localAvatar.startSmartCamera()
        base.localAvatar.startPosHprBroadcast()
        base.localAvatar.d_broadcastPositionNow()
        base.localAvatar.b_setAnimState('teleportOut', callback, [requestStatus])

    def exitTeleportOut(self):
        base.localAvatar.disableLaffMeter()
        base.localAvatar.stopSmartCamera()
        base.localAvatar.detachCamera()
        base.localAvatar.stopPosHprBroadcast()