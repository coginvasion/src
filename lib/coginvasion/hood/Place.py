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
from direct.interval.IntervalGlobal import Parallel, LerpHprInterval, Sequence, Wait, Func, LerpPosInterval, LerpQuatInterval
from lib.coginvasion.globals import CIGlobals
from PublicWalk import PublicWalk
from lib.coginvasion.book.ShtickerBook import ShtickerBook
from lib.coginvasion.gui.Dialog import GlobalDialog
import LinkTunnel
import ZoneUtil

class Place(StateData):
    notify = directNotify.newCategory('Place')

    def __init__(self, loader, doneEvent):
        StateData.__init__(self, doneEvent)
        self.loader = loader
        self.zoneId = None
        self.track = None
        return

    def maybeUpdateAdminPage(self):
        if self.fsm:
            if self.fsm.getCurrentState():
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

    def enterStart(self):
        pass

    def exitStart(self):
        pass

    def enterFinal(self):
        pass

    def exitFinal(self):
        pass

    def enter(self):
        StateData.enter(self)
        base.localAvatar.createChatInput()

    def exit(self):
        base.localAvatar.disableChatInput()
        StateData.exit(self)

    def enterDoorIn(self, distDoor):
        base.localAvatar.attachCamera()
        requestStatus = {}
        requestStatus['zoneId'] = distDoor.getToZone()
        requestStatus['hoodId'] = base.cr.playGame.hood.id
        requestStatus['how'] = 'doorOut'
        requestStatus['shardId'] = None
        requestStatus['doorIndex'] = distDoor.getDoorIndex()
        foundBlock = False
        for interior in base.cr.doFindAll('DistributedToonInterior'):
            if interior.zoneId == base.localAvatar.zoneId:
                foundBlock = True
                requestStatus['block'] = interior.getBlock()
                break

        if not foundBlock:
            requestStatus['block'] = distDoor.getBlock()
        requestStatus['where'] = ZoneUtil.getWhereName(requestStatus['zoneId'])
        requestStatus['loader'] = base.cr.playGame.hood.fsm.getCurrentState().getName()
        requestStatus['avId'] = base.localAvatar.doId
        self.acceptOnce('DistributedDoor_localAvatarWentInDoor', self.handleDoorInDone, [requestStatus])
        self.acceptOnce('DistributedDoor_localAvatarGoingInDoor', base.transitions.irisOut)
        return

    def exitDoorIn(self):
        base.localAvatar.detachCamera()
        self.ignore('DistributedDoor_localAvatarWentInDoor')
        self.ignore('DistributedDoor_localAvatarGoingInDoor')

    def handleDoorInDone(self, requestStatus):
        self.doneStatus = requestStatus
        messenger.send(self.doneEvent)

    def __waitOnDoor(self, door, task):
        if door.ready:
            self.__doorReady(door)
            return task.done
        return task.cont

    def enterDoorOut(self, requestStatus):
        base.localAvatar.attachCamera()
        base.localAvatar.startSmartCamera()
        base.localAvatar.d_clearSmoothing()
        base.localAvatar.stopPosHprBroadcast()
        base.localAvatar.walkControls.setCollisionsActive(0)
        block = requestStatus['block']
        zoneId = requestStatus['zoneId']
        doorIndex = requestStatus['doorIndex']
        doorToExitFrom = None
        for door in base.cr.doFindAll('DistributedDoor'):
            if door.zoneId == zoneId:
                if door.getBlock() == block:
                    if door.getDoorIndex() == doorIndex:
                        doorToExitFrom = door
                        break

        if not doorToExitFrom:
            self.notify.error('Could not find a DistributedDoor to exit from!')
        elif not doorToExitFrom.ready:
            base.taskMgr.add(self.__waitOnDoor, 'Place.waitOnDoor', extraArgs=[doorToExitFrom], appendTask=True)
            return
        self.__doorReady(doorToExitFrom)
        return

    def __doorReady(self, door):
        door.sendUpdate('requestExit', [])
        self.nextState = 'walk'
        self.acceptOnce('DistributedDoor_localAvatarCameOutOfDoor', self.handleDoorOutDone)

    def exitDoorOut(self):
        base.taskMgr.remove('Place.waitOnDoor')
        base.localAvatar.stopSmartCamera()
        base.localAvatar.detachCamera()
        self.ignore('DistributedDoor_localAvatarCameOutOfDoor')

    def handleDoorOutDone(self):
        base.transitions.irisIn()
        base.localAvatar.walkControls.setCollisionsActive(1)
        self.fsm.request(self.nextState)

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
        elif doneStatus['mode'] == 'switchShard':
            base.localAvatar.b_setAnimState('closeBook', self.__handleBookCloseSwitchShard, [doneStatus])

    def __handleBookCloseSwitchShard(self, requestStatus):
        base.localAvatar.b_setAnimState('teleportOut', self.__handleBookSwitchShard, [requestStatus])

    def __handleBookSwitchShard(self, requestStatus):
        params = []
        params.append(requestStatus['shardId'])
        params.append(base.cr.playGame.hood.id)
        params.append(ZoneUtil.getZoneId(base.cr.playGame.hood.id))
        params.append(base.localAvatar.doId)
        base.cr.gameFSM.request('switchShards', params)

    def __handleBookCloseResume(self):
        self.fsm.request('walk')

    def __handleBookCloseTeleport(self, requestStatus):
        self.fsm.request('teleportOut', [requestStatus])

    def __teleportOutDone(self, requestStatus):
        self.doneStatus = requestStatus
        messenger.send(self.doneEvent)

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

    def enterStop(self, doNeutral = 1):
        if doNeutral:
            base.localAvatar.b_setAnimState('neutral')
        base.localAvatar.attachCamera()
        base.localAvatar.startSmartCamera()
        base.localAvatar.createLaffMeter()
        base.localAvatar.createMoney()
        base.localAvatar.enablePies(0)

    def exitStop(self):
        base.localAvatar.stopSmartCamera()
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
        if requestStatus['avId'] != base.localAvatar.doId:
            av = base.cr.doId2do.get(requestStatus['avId'])
            if av:
                base.localAvatar.gotoNode(av)
                base.localAvatar.b_setChat('Hi, %s.' % av.getName())
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

    def enterAcknowledgeDeath(self, foo = 0):
        base.localAvatar.attachCamera()
        base.localAvatar.startSmartCamera()
        message = 'You were defeated by the Cogs! Collect treasures in the Playground to refill your Laff meter.'
        self.dialog = GlobalDialog(message=message, style=3, doneEvent='ackDeathDone')
        self.dialog.show()
        self.acceptOnce('ackDeathDone', self.handleAckDeathDone)

    def handleAckDeathDone(self):
        self.fsm.request('walk', [1])

    def exitAcknowledgeDeath(self):
        self.ignore('ackDeathDone')
        self.dialog.cleanup()
        del self.dialog
        base.localAvatar.stopSmartCamera()
        base.localAvatar.detachCamera()

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
        self.watchTunnelSeq = Sequence(Wait(1.0), Func(LinkTunnel.globalAcceptCollisions))
        self.watchTunnelSeq.start()
        base.localAvatar.setBusy(0)
        base.localAvatar.enablePicking()
        base.localAvatar.showFriendButton()

    def exitWalk(self):
        self.walkStateData.exit()
        self.ignore(self.walkDoneEvent)
        if base.cr.playGame.hood.titleText != None:
            base.cr.playGame.hood.hideTitleText()
        self.watchTunnelSeq.pause()
        del self.watchTunnelSeq
        base.localAvatar.setBusy(1)
        base.localAvatar.disablePicking()
        base.localAvatar.hideFriendButton()
        base.localAvatar.friendsList.fsm.requestFinalState()
        base.localAvatar.panel.fsm.requestFinalState()
        return

    def handleWalkDone(self, doneStatus):
        pass

    def enterTeleportOut(self, requestStatus, callback = None):
        if not callback:
            callback = self.__teleportOutDone
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

    def enterTunnelIn(self, linkTunnel):
        base.localAvatar.attachCamera()
        base.localAvatar.playMovementSfx('run')
        pivotPoint = linkTunnel.inPivotPoint
        self.pivotPointNode = linkTunnel.tunnel.attachNewNode('tunnelPivotPoint')
        self.pivotPointNode.setPos(pivotPoint)
        currCamPos = camera.getPos(linkTunnel.tunnel)
        currCamHpr = camera.getHpr(linkTunnel.tunnel)
        currPos = base.localAvatar.getPos(self.pivotPointNode)
        currHpr = base.localAvatar.getHpr(self.pivotPointNode)
        if linkTunnel.__class__.__name__ == 'SafeZoneLinkTunnel':
            base.localAvatar.setHpr(180, 0, 0)
        else:
            base.localAvatar.setHpr(0, 0, 0)
        base.localAvatar.setPos(currPos)
        base.localAvatar.reparentTo(self.pivotPointNode)
        base.localAvatar.walkControls.setCollisionsActive(0)
        base.localAvatar.detachCamera()
        camera.reparentTo(linkTunnel.tunnel)
        tunnelCamPos = linkTunnel.camPos
        tunnelCamHpr = linkTunnel.camHpr
        self.track = Parallel(LerpPosInterval(camera, duration=0.7, pos=tunnelCamPos, startPos=currCamPos, blendType='easeOut'), LerpQuatInterval(camera, duration=0.7, quat=tunnelCamHpr, startHpr=currCamHpr, blendType='easeOut'), Sequence(Func(base.localAvatar.b_setAnimState, 'run'), Wait(2.0), Func(base.transitions.irisOut)), Sequence(LerpHprInterval(self.pivotPointNode, duration=2.0, hpr=linkTunnel.inPivotEndHpr, startHpr=linkTunnel.inPivotStartHpr), LerpPosInterval(self.pivotPointNode, duration=1.0, pos=(linkTunnel.inPivotEndX, self.pivotPointNode.getY(), self.pivotPointNode.getZ()), startPos=(linkTunnel.inPivotStartX, self.pivotPointNode.getY(), self.pivotPointNode.getZ()))), name='Place.enterTunnelIn')
        requestStatus = {}
        requestStatus['zoneId'] = linkTunnel.data['zoneId']
        if linkTunnel.__class__.__name__ == 'SafeZoneLinkTunnel':
            requestStatus['where'] = 'street'
            requestStatus['loader'] = 'townLoader'
            requestStatus['hoodId'] = base.cr.playGame.hood.id
            requestStatus['shardId'] = None
            requestStatus['avId'] = base.localAvatar.doId
            requestStatus['how'] = 'tunnelOut'
            requestStatus['fromZone'] = base.localAvatar.zoneId
        elif linkTunnel.__class__.__name__ == 'StreetLinkTunnel':
            requestStatus['where'] = 'playground'
            requestStatus['loader'] = 'safeZoneLoader'
            requestStatus['hoodId'] = base.cr.playGame.hood.id
            requestStatus['shardId'] = None
            requestStatus['avId'] = base.localAvatar.doId
            requestStatus['how'] = 'tunnelOut'
            requestStatus['fromZone'] = base.localAvatar.zoneId
        elif linkTunnel.__class__.__name__ == 'NeighborhoodLinkTunnel':
            requestStatus['where'] = 'street'
            requestStatus['loader'] = 'townLoader'
            hoodId = ZoneUtil.getHoodId(linkTunnel.data['zoneId'], 1)
            requestStatus['hoodId'] = hoodId
            requestStatus['shardId'] = None
            requestStatus['avId'] = base.localAvatar.doId
            requestStatus['how'] = 'tunnelOut'
            requestStatus['fromZone'] = base.localAvatar.zoneId
        self.track.setDoneEvent(self.track.getName())
        self.acceptOnce(self.track.getDoneEvent(), self.__handleTunnelInDone, [requestStatus])
        self.track.start()
        return

    def __handleTunnelInDone(self, requestStatus):
        self.doneStatus = requestStatus
        messenger.send(self.doneEvent)

    def exitTunnelIn(self):
        base.localAvatar.playMovementSfx(None)
        if self.track:
            self.ignore(self.track.getDoneEvent())
            self.track.finish()
            self.track = None
        base.localAvatar.reparentTo(render)
        self.pivotPointNode.removeNode()
        del self.pivotPointNode
        base.localAvatar.detachCamera()
        base.localAvatar.walkControls.setCollisionsActive(1)
        return

    def enterTunnelOut(self, requestStatus):
        base.localAvatar.playMovementSfx('run')
        base.transitions.irisIn()
        self.nextState = requestStatus.get('nextState', 'walk')
        linkTunnel = LinkTunnel.getTunnelThatGoesToZone(requestStatus['fromZone'])
        pivotPoint = linkTunnel.outPivotPoint
        self.pivotPointNode = linkTunnel.tunnel.attachNewNode('tunnelPivotPoint')
        self.pivotPointNode.setPos(pivotPoint)
        self.pivotPointNode.setHpr(linkTunnel.outPivotStartHpr)
        base.localAvatar.walkControls.setCollisionsActive(0)
        base.localAvatar.reparentTo(self.pivotPointNode)
        base.localAvatar.setHpr(linkTunnel.toonOutHpr)
        base.localAvatar.setPos(linkTunnel.toonOutPos)
        base.localAvatar.detachCamera()
        camera.reparentTo(linkTunnel.tunnel)
        tunnelCamPos = linkTunnel.camPos
        tunnelCamHpr = linkTunnel.camHpr
        camera.setPos(tunnelCamPos)
        camera.setHpr(tunnelCamHpr)
        self.track = Parallel(Sequence(Func(base.localAvatar.b_setAnimState, 'run'), LerpPosInterval(self.pivotPointNode, duration=1.0, pos=(linkTunnel.outPivotEndX, self.pivotPointNode.getY(), self.pivotPointNode.getZ()), startPos=(linkTunnel.outPivotStartX, self.pivotPointNode.getY(), self.pivotPointNode.getZ())), LerpHprInterval(self.pivotPointNode, duration=2.0, hpr=linkTunnel.outPivotEndHpr, startHpr=linkTunnel.outPivotStartHpr)), name='Place.enterTunnelOut')
        self.track.setDoneEvent(self.track.getName())
        self.acceptOnce(self.track.getDoneEvent(), self.__handleTunnelOutDone)
        self.track.start()

    def __handleTunnelOutDone(self):
        base.localAvatar.walkControls.setCollisionsActive(1)
        self.fsm.request(self.nextState)

    def exitTunnelOut(self):
        base.localAvatar.playMovementSfx(None)
        base.localAvatar.walkControls.setCollisionsActive(1)
        if self.track:
            self.ignore(self.track.getDoneEvent())
            self.track.finish()
            self.track = None
        base.localAvatar.setPos(base.localAvatar.getPos(render))
        base.localAvatar.setHpr(base.localAvatar.getHpr(render))
        base.localAvatar.reparentTo(render)
        self.pivotPointNode.removeNode()
        del self.pivotPointNode
        base.localAvatar.detachCamera()
        del self.nextState
        return