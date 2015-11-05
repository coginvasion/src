# Embedded file name: lib.coginvasion.minigame.DistributedGroupStationAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.interval.IntervalGlobal import Sequence, Wait, Func

class DistributedGroupStationAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedGroupStationAI')

    def __init__(self, air):
        try:
            self.DistributedGroupStationAI_initialized
            return
        except:
            self.DistributedGroupStationAI_initialized = 1

        DistributedObjectAI.__init__(self, air)
        self.avatars = []
        self.maxAvatars = 0
        self.time = 10
        self.location_point = 0
        self.availableSlots = 0
        self.maximumSlots = 0
        self.slotsAvailable = []
        self.timerSeq = None
        return

    def resetAvailableSlots(self):
        self.slotsAvailable = []
        for i in range(self.maxAvatars):
            self.slotsAvailable.append(i + 1)

    def d_setTimerTime(self, time):
        self.time = time
        self.sendUpdate('setTimerTime', [time])

    def setLocationPoint(self, lp):
        self.location_point = lp

    def b_setLocationPoint(self, lp):
        self.d_setLocationPoint(lp)
        self.setLocationPoint(lp)

    def d_setLocationPoint(self, lp):
        self.sendUpdate('setLocationPoint', [lp])

    def getLocationPoint(self):
        return self.location_point

    def monitorAvatars(self, task):
        for avatar in self.avatars:
            if avatar not in self.air.doId2do.values():
                self.clearAvatar(avatar.doId)

        return task.cont

    def isAvatarPresent(self, doId):
        """ Is the avatar currently in our station? """
        for avatar in self.avatars:
            if avatar.doId == doId:
                return True

        return False

    def setAvailableSlots(self, slots):
        self.availableSlots = slots

    def getAvailableSlots(self):
        return self.availableSlots

    def getAnAvailableSlot(self):
        slot = 0
        if 1 in self.slotsAvailable:
            slot = 0
        elif 2 in self.slotsAvailable:
            slot = 1
        elif 3 in self.slotsAvailable:
            slot = 2
        elif 4 in self.slotsAvailable:
            slot = 3
        elif 5 in self.slotsAvailable:
            slot = 4
        elif 6 in self.slotsAvailable:
            slot = 5
        elif 7 in self.slotsAvailable:
            slot = 6
        elif 8 in self.slotsAvailable:
            slot = 7
        return self.slotsAvailable[0]

    def appendAvatar(self, doId):
        if not self.isAvatarPresent(doId):
            for key in self.air.doId2do.keys():
                obj = self.air.doId2do[key]
                if obj.doId == doId:
                    self.avatars.append(obj)

    def clearAvatar(self, doId):
        for avatar in self.avatars:
            if avatar.doId == doId:
                self.avatars.remove(avatar)
                self.availableSlots += 1
                if len(self.avatars) == 0:
                    self.stopTimer()
                    self.resetAvailableSlots()
                else:
                    self.resetTimer()

    def startTimer(self):
        seq = Sequence()
        for second in range(11):
            seq.append(Func(self.d_setTimerTime, 10 - second))
            seq.append(Wait(1.0))

        seq.start()
        self.timerSeq = seq

    def stopTimer(self):
        self.d_setTimerTime(10)
        if self.timerSeq:
            self.timerSeq.pause()
            self.timerSeq = None
        return

    def resetTimer(self):
        self.stopTimer()
        self.startTimer()

    def requestEnter(self):
        doId = self.air.getAvatarIdFromSender()
        if self.getAvailableSlots() > 0 and not self.isAvatarPresent(doId):
            availableSlot = self.getAnAvailableSlot()
            self.appendAvatar(doId)
            self.d_slotOpen(availableSlot, doId)
            self.slotsAvailable.remove(availableSlot)
            self.availableSlots -= 1
            if len(self.avatars) == 1:
                self.resetTimer()
                taskMgr.add(self.monitorTime, self.taskName('monitorTime'))
        elif self.getAvailableSlots() <= 0 and not self.isAvatarPresent(doId):
            self.d_fullStation(doId)

    def requestAbort(self, slot):
        doId = self.air.getAvatarIdFromSender()
        if self.isAvatarPresent(doId):
            self.clearAvatar(doId)
            self.slotsAvailable.append(slot)
            self.d_abort(doId)

    def leaving(self):
        doId = self.air.getAvatarIdFromSender()
        if self.isAvatarPresent(doId):
            self.clearAvatar(doId)
            self.resetAvailableSlots()

    def d_abort(self, doId):
        self.sendUpdateToAvatarId(doId, 'abort', [])

    def d_slotOpen(self, slot, doId):
        self.sendUpdateToAvatarId(doId, 'slotOpen', [slot])

    def d_fullStation(self, doId):
        self.sendUpdateToAvatarId(doId, 'fullStation', [])

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        taskMgr.add(self.monitorAvatars, self.taskName('DistributedGroupStationAI.monitorAvatars'))

    def delete(self):
        taskMgr.remove(self.taskName('DistributedGroupStationAI.monitorAvatars'))
        self.avatars = None
        self.maxAvatars = None
        DistributedObjectAI.delete(self)
        return