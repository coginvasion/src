# Embedded file name: lib.coginvasion.hood.QuietZoneState
"""
  
  Filename: QuietZoneState.py
  Created by: blach (30Nov14)
  
"""
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.fsm.StateData import StateData
from lib.coginvasion.distributed.CogInvasionMsgTypes import *

class QuietZoneState(StateData):
    Queue = []

    def __init__(self, doneEvent):
        StateData.__init__(self, doneEvent)
        self.fsm = ClassicFSM('quietZone', [State('off', self.enterOff, self.exitOff, ['waitForQuietZoneResponse']),
         State('waitForQuietZoneResponse', self.enterWaitForQuietZoneResponse, self.exitWaitForQuietZoneResponse, ['waitForSetZoneResponse']),
         State('waitForSetZoneResponse', self.enterWaitForSetZoneResponse, self.exitWaitForSetZoneResponse, ['waitForSetZoneComplete']),
         State('waitForSetZoneComplete', self.enterWaitForSetZoneComplete, self.exitWaitForSetZoneComplete, ['off'])], 'off', 'off')
        self.fsm.enterInitialState()
        self._enqueueCount = 0

    @classmethod
    def enqueueState(cls, state, requestStatus):
        cls.Queue = [(state, requestStatus)] + cls.Queue
        state._enqueueCount += 1
        if len(cls.Queue) == 1:
            cls.startNextQueuedState()

    @classmethod
    def dequeueState(cls, state):
        s, requestStatus = cls.Queue.pop()
        s._enqueueCount -= 1
        if len(cls.Queue) > 0:
            cls.startNextQueuedState()

    @classmethod
    def startNextQueuedState(cls):
        state, requestStatus = cls.Queue[-1]
        state._start(requestStatus)

    def _dequeue(self):
        newQ = []
        for item in self.__class__.Queue:
            state, requestStatus = item
            if state is not self:
                newQ.append(item)

        self.__class__.Queue = newQ

    def _start(self, requestStatus):
        base.transitions.fadeScreen(1.0)
        base.localAvatar.b_setAnimState('off')
        self.fsm.request('waitForQuietZoneResponse')

    def getSetZoneCompleteEvent(self):
        return 'setZoneComplete-%s' % id(self)

    def getQuietZoneResponseEvent(self):
        return 'quietZoneResponse-%s' % id(self)

    def getEnterWaitForSetZoneResponseMsg(self):
        return 'enterWaitForSetZoneResponse-%s' % id(self)

    def unload(self):
        StateData.unload(self)
        self._dequeue()
        del self.fsm

    def enter(self, requestStatus):
        StateData.enter(self)
        self._requestStatus = requestStatus
        self.enqueueState(self, requestStatus)

    def exit(self):
        StateData.exit(self)
        del self._requestStatus
        base.transitions.noTransitions()
        self.fsm.request('off')
        self._dequeue()

    def getDoneStatus(self):
        return self._requestStatus

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def handleWaitForQuietZoneResponse(self, msgType, di):
        if msgType == CLIENT_ENTER_OBJECT_REQUIRED:
            base.cr.handleQuietZoneGenerateWithRequired(di)
        elif msgType == CLIENT_ENTER_OBJECT_REQUIRED_OTHER:
            base.cr.handleQuietZoneGenerateWithRequiredOther(di)
        elif msgType == CLIENT_OBJECT_SET_FIELD:
            base.cr.handleQuietZoneUpdateField(di)
        else:
            base.cr.astronHandle(di)

    def enterWaitForQuietZoneResponse(self):
        self.setZoneDoneEvent = base.cr.getNextSetZoneDoneEvent()
        self.acceptOnce(self.setZoneDoneEvent, self._handleQuietZoneResponse)
        base.cr.sendQuietZoneRequest()

    def _handleQuietZoneResponse(self):
        self.fsm.request('waitForSetZoneResponse')

    def exitWaitForQuietZoneResponse(self):
        self.ignore(self.setZoneDoneEvent)
        del self.setZoneDoneEvent

    def enterWaitForZoneRedirect(self):
        self.fsm.request('waitForSetZoneResponse')

    def exitWaitForZoneRedirect(self):
        pass

    def enterWaitForSetZoneResponse(self):
        messenger.send(self.getEnterWaitForSetZoneResponseMsg(), [self._requestStatus])
        zoneId = self._requestStatus['zoneId']
        base.cr.sendSetZoneMsg(zoneId)
        self.fsm.request('waitForSetZoneComplete')

    def exitWaitForSetZoneResponse(self):
        pass

    def enterWaitForSetZoneComplete(self):
        self.setZoneDoneEvent = base.cr.getLastSetZoneDoneEvent()
        self.acceptOnce(self.setZoneDoneEvent, self._announceDone)

    def exitWaitForSetZoneComplete(self):
        self.ignore(self.setZoneDoneEvent)
        del self.setZoneDoneEvent

    def _announceDone(self):
        doneEvent = self.doneEvent
        requestStatus = self._requestStatus
        messenger.send(self.getSetZoneCompleteEvent(), [requestStatus])
        messenger.send(doneEvent)
        self._dequeue()

    def getRequestStatus(self):
        return self._requestStatus