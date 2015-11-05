# Embedded file name: lib.coginvasion.distributed.CogInvasionClientRepository
"""

  Filename: CogInvasionClientRepository.py
  Created by: blach (7Nov14)
  
"""
from panda3d.core import *
from lib.coginvasion.gui.Dialog import *
from direct.gui.DirectGui import *
from direct.distributed.AstronClientRepository import AstronClientRepository
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.distributed.MsgTypes import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.interval.IntervalGlobal import *
from CogInvasionDoGlobals import *
from direct.task import Task
from pandac.PandaModules import UniqueIdAllocator
from lib.coginvasion.login.AvChooser import AvChooser
from lib.coginvasion.makeatoon.MakeAToon import MakeAToon
from lib.coginvasion.distributed.PlayGame import PlayGame
from lib.coginvasion.distributed.HoodMgr import HoodMgr
from lib.coginvasion.toon import LocalToon
from lib.coginvasion.base.EnterLoad import EnterLoad
from direct.distributed import DistributedSmoothNode
from CogInvasionErrorCodes import *
from lib.coginvasion.base import SpeedHackChecker
import types
import os
import sys
import random

class CogInvasionClientRepository(AstronClientRepository):
    notify = directNotify.newCategory('CIClientRepository')
    GameGlobalsId = DO_ID_COGINVASION
    SetZoneDoneEvent = 'CICRSetZoneDone'
    EmuSetZoneDoneEvent = 'CICREmuSetZoneDone'
    SetInterest = 'Set'
    ClearInterest = 'Clear'
    ClearInterestDoneEvent = 'CICRClearInterestDone'
    ITAG_PERM = 'perm'
    ITAG_AVATAR = 'avatar'
    ITAG_SHARD = 'shard'
    ITAG_WORLD = 'world'
    ITAG_GAME = 'game'

    def __init__(self, music, serverVersion):
        self.music = music
        self.serverVersion = serverVersion
        AstronClientRepository.__init__(self, ['phase_3/etc/direct.dc', 'phase_3/etc/toon.dc'])
        self.loginFSM = ClassicFSM('login', [State('off', self.enterOff, self.exitOff),
         State('connect', self.enterConnect, self.exitConnect),
         State('disconnect', self.enterDisconnect, self.exitDisconnect),
         State('avChoose', self.enterAvChoose, self.exitAvChoose),
         State('playingGame', self.enterPlayingGame, self.exitPlayingGame),
         State('serverUnavailable', self.enterServerUnavailable, self.exitServerUnavailable),
         State('makeAToon', self.enterMakeAToon, self.exitMakeAToon),
         State('submitNewToon', self.enterSubmitNewToon, self.exitSubmitNewToon),
         State('noShards', self.enterNoShards, self.exitNoShards),
         State('waitForSetAvatarResponse', self.enterWaitForSetAvatarResponse, self.exitWaitForSetAvatarResponse),
         State('waitForShardList', self.enterWaitForShardList, self.exitWaitForShardList),
         State('ejected', self.enterEjected, self.exitEjected),
         State('districtReset', self.enterDistrictReset, self.exitDistrictReset),
         State('died', self.enterDied, self.exitDied)], 'off', 'off')
        self.loginFSM.enterInitialState()
        self.gameFSM = ClassicFSM('game', [State('off', self.enterGameOff, self.exitGameOff),
         State('waitForGameEnterResponse', self.enterWaitForGameEnterResponse, self.exitWaitForGameEnterResponse),
         State('playGame', self.enterPlayGame, self.exitPlayGame),
         State('closeShard', self.enterCloseShard, self.exitCloseShard)], 'off', 'off')
        self.gameFSM.enterInitialState()
        self.avChooser = AvChooser(self.loginFSM)
        self.playGame = PlayGame(self.gameFSM, 'playGameDone')
        self.hoodMgr = HoodMgr()
        self.makeAToon = MakeAToon()
        self.loginToken = os.environ.get('LOGIN_TOKEN')
        self.serverAddress = os.environ.get('GAME_SERVER')
        self.serverURL = URLSpec('http://%s' % self.serverAddress)
        self.parentMgr.registerParent(CIGlobals.SPRender, render)
        self.parentMgr.registerParent(CIGlobals.SPHidden, hidden)
        self.adminAccess = False
        self.localAvChoice = None
        self.SuitsActive = 0
        self.BossActive = 0
        self.accServerTimesNA = 0
        self.maxAccServerTimesNA = 10
        self.setZonesEmulated = 0
        self.old_setzone_interest_handle = None
        self.setZoneQueue = Queue()
        self.accept(self.SetZoneDoneEvent, self._handleEmuSetZoneDone)
        self.handler = None
        self.__currentAvId = 0
        self.myDistrict = None
        self.activeDistricts = {}
        self.shardListHandle = None
        self.uberZoneInterest = None
        self.isShowingPlayerIds = False
        self.accountName = os.environ.get('ACCOUNT_NAME', '')
        self.csm = self.generateGlobalObject(DO_ID_CLIENT_SERVICES_MANAGER, 'ClientServicesManager')
        SpeedHackChecker.startChecking()
        self.loginFSM.request('connect')
        return

    def showPlayerIds(self):
        print 'Showing player ids...'
        self.isShowingPlayerIds = True
        for av in self.doId2do.values():
            if av.__class__.__name__ in ('DistributedToon', 'LocalToon'):
                av.showAvId()

    def hidePlayerIds(self):
        print 'Hiding player ids...'
        self.isShowingPlayerIds = False
        for av in self.doId2do.values():
            if av.__class__.__name__ in ('DistributedToon', 'LocalToon'):
                av.showName()

    def sendSetLocation(self, doId, parentId, zoneId):
        dg = PyDatagram()
        dg.addUint16(CLIENT_OBJECT_LOCATION)
        dg.addUint32(doId)
        dg.addUint32(parentId)
        dg.addUint32(zoneId)
        self.send(dg)

    def getNextSetZoneDoneEvent(self):
        return '%s-%s' % (self.EmuSetZoneDoneEvent, self.setZonesEmulated + 1)

    def getLastSetZoneDoneEvent(self):
        return '%s-%s' % (self.EmuSetZoneDoneEvent, self.setZonesEmulated)

    def getQuietZoneLeftEvent(self):
        return 'leftQuietZone-%s' % (id(self),)

    def sendSetZoneMsg(self, zoneId, visibleZoneList = None):
        event = self.getNextSetZoneDoneEvent()
        self.setZonesEmulated += 1
        parentId = base.localAvatar.defaultShard
        self.sendSetLocation(base.localAvatar.doId, parentId, zoneId)
        localAvatar.setLocation(parentId, zoneId)
        interestZones = zoneId
        if visibleZoneList is not None:
            interestZones = visibleZoneList
        self._addInterestOpToQueue(self.SetInterest, [parentId, interestZones, 'OldSetZoneEmulator'], event)
        return

    def resetInterestStateForConnectionLoss(self):
        self.old_setzone_interest_handle = None
        self.setZoneQueue.clear()
        return

    def _removeEmulatedSetZone(self, doneEvent):
        self._addInterestOpToQueue(self.ClearInterest, None, doneEvent)
        return

    def _addInterestOpToQueue(self, op, args, event):
        self.setZoneQueue.push([op, args, event])
        if len(self.setZoneQueue) == 1:
            self._sendNextSetZone()

    def _sendNextSetZone(self):
        op, args, event = self.setZoneQueue.top()
        if op == self.SetInterest:
            parentId, interestZones, name = args
            if self.old_setzone_interest_handle == None:
                self.old_setzone_interest_handle = self.addInterest(parentId, interestZones, name, self.SetZoneDoneEvent)
            else:
                self.alterInterest(self.old_setzone_interest_handle, parentId, interestZones, name, self.SetZoneDoneEvent)
        elif op == self.ClearInterest:
            self.removeInterest(self.old_setzone_interest_handle, self.SetZoneDoneEvent)
            self.old_setzone_interest_handle = None
        else:
            self.notify.error('unknown setZone op: %s' % op)
        return

    def _handleEmuSetZoneDone(self):
        op, args, event = self.setZoneQueue.pop()
        queueIsEmpty = self.setZoneQueue.isEmpty()
        if event is not None:
            messenger.send(event)
        if not queueIsEmpty:
            self._sendNextSetZone()
        return

    def enterCloseShard(self, nextState = 'avChoose'):
        self.setNoNewInterests(True)
        self._removeLocalAvFromStateServer(nextState)

    def exitCloseShard(self):
        self.setNoNewInterests(False)
        self.ignore(self.ClearInterestDoneEvent)

    def _removeLocalAvFromStateServer(self, nextState):
        self.sendSetAvatarIdMsg(0)
        self._removeAllOV()
        callback = Functor(self.loginFSM.request, nextState)
        self.removeShardInterest(callback)

    def removeShardInterest(self, callback):
        self._removeCurrentShardInterest(Functor(self._removeShardInterestComplete, callback))

    def _removeShardInterestComplete(self, callback):
        self.cache.flush()
        self.doDataCache.flush()
        callback()

    def _removeCurrentShardInterest(self, callback):
        if self.old_setzone_interest_handle is None:
            callback()
            return
        else:
            self.acceptOnce(self.ClearInterestDoneEvent, Functor(self._removeCurrentUberZoneInterest, callback))
            self._removeEmulatedSetZone(self.ClearInterestDoneEvent)
            return

    def _removeCurrentUberZoneInterest(self, callback):
        self.acceptOnce(self.ClearInterestDoneEvent, Functor(self._removeShardInterestDone, callback))
        self.removeInterest(self.uberZoneInterest, self.ClearInterestDoneEvent)

    def _removeShardInterestDone(self, callback):
        self.uberZoneInterest = None
        callback()
        return

    def _removeAllOV(self):
        owners = self.doId2ownerView.keys()
        for doId in owners:
            self.disableDoId(doId, ownerView=True)

    def enterDied(self):
        self.deathDialog = GlobalDialog(message=CIGlobals.SuitDefeatMsg, style=2, doneEvent='deathChoice')
        self.deathDialog.show()
        self.acceptOnce('deathChoice', self.handleDeathChoice)

    def handleDeathChoice(self):
        value = self.deathDialog.getValue()
        if value:
            self.loginFSM.request('avChoose')
        else:
            sys.exit()

    def exitDied(self):
        self.deathDialog.cleanup()
        del self.deathDialog
        self.ignore('deathChoice')

    def enterConnect(self):
        self.connectingDialog = GlobalDialog(message=CIGlobals.ConnectingMsg)
        self.connectingDialog.show()
        self.connect([self.serverURL], successCallback=self.handleConnected, failureCallback=self.handleConnectFail)

    def handleConnected(self):
        self.notify.info('Sending CLIENT_HELLO...')
        self.acceptOnce('CLIENT_HELLO_RESP', self.handleClientHelloResp)
        self.acceptOnce('CLIENT_EJECT', self.handleEjected)
        self.acceptOnce('LOST_CONNECTION', self.handleLostConnection)
        AstronClientRepository.sendHello(self, self.serverVersion)

    def handleLostConnection(self):
        self.deleteAllObjects()
        self.loginFSM.request('disconnect', [1])

    def deleteAllObjects(self):
        for doId in self.doId2do.keys():
            obj = self.doId2do[doId]
            if hasattr(base, 'localAvatar'):
                if doId != base.localAvatar.doId:
                    if obj.__class__.__name__ not in ('ClientServicesManager', 'DistributedDistrict'):
                        self.deleteObject(doId)
            else:
                self.deleteObject(doId)

    def handleEjected(self, errorCode, reason):
        self.notify.info('OMG I WAS EJECTED!')
        self.ignore('LOST_CONNECTION')
        errorMsg = ErrorCode2ErrorMsg.get(errorCode, None) or UnknownErrorMsg % errorCode
        self.loginFSM.request('ejected', [errorMsg])
        return

    def handleClientHelloResp(self):
        self.notify.info('Got CLIENT_HELLO_RESP!')
        self.acceptOnce(self.csm.getLoginAcceptedEvent(), self.handleLoginAccepted)
        self.csm.d_requestLogin(self.loginToken, self.accountName)

    def handleLoginAccepted(self):
        self.notify.info('Woo-hoo, I am authenticated!')
        self.loginFSM.request('waitForShardList')

    def handleConnectFail(self, foo1, foo2):
        self.notify.info('Could not connect to gameserver, notifying user.')
        self.connectingDialog.cleanup()
        self.connectingDialog = GlobalDialog(message=CIGlobals.NoConnectionMsg % self.serverAddress + ' ' + CIGlobals.TryAgain, style=2, doneEvent='connectFail')
        self.connectingDialog.show()
        self.acceptOnce('connectFail', self.handleConnectFailButton)

    def handleConnectFailButton(self):
        value = self.connectingDialog.getValue()
        if value:
            self.loginFSM.request('connect')
        else:
            sys.exit()

    def exitConnect(self):
        self.ignore('connectFail')
        self.ignore('CLIENT_HELLO_RESP')
        self.ignore(self.csm.getLoginAcceptedEvent())
        self.connectingDialog.cleanup()
        del self.connectingDialog

    def enterEjected(self, errorMsg):
        self.ejectDialog = GlobalDialog(message=errorMsg, style=3, doneEvent='ejectDone')
        self.ejectDialog.show()
        self.acceptOnce('ejectDone', sys.exit)

    def exitEjected(self):
        self.ignore('ejectDone')
        self.ejectDialog.cleanup()
        del self.ejectDialog

    def enterServerUnavailable(self):
        self.notify.info(CIGlobals.ServerUnavailable)
        self.serverNA = GlobalDialog(message=CIGlobals.ServerUnavailable, style=4, doneEvent='serverNAEvent')
        self.serverNA.show()
        self.acceptOnce('serverNAEvent', sys.exit)
        self.startServerNAPoll()

    def startServerNAPoll(self):
        self.notify.info('Starting server poll...')
        self.accServerTimesNA = 1
        taskMgr.add(self.serverNAPoll, 'serverNAPoll')

    def serverNAPoll(self, task):
        dg = PyDatagram()
        dg.addUint16(ACC_IS_SERVER_UP)
        self.send(dg)
        task.delayTime = 3.0
        return Task.again

    def __handleServerNAResp(self, resp):
        if resp == ACC_SERVER_UP:
            taskMgr.remove('serverNAPoll')
            self.loginFSM.request(self.loginFSM.getLastState().getName())
        else:
            self.accServerTimesNA += 1
            if self.accServerTimesNA >= self.maxAccServerTimesNA:
                taskMgr.remove('serverNAPoll')
                self.notify.info('Giving up on polling account server after %s times.' % self.accServerTimesNA)
                self.loginFSM.request('disconnect', enterArgList=[1])
                self.accServerTimesNA = 0

    def exitServerUnavailable(self):
        self.ignore('serverNAEvent')
        self.serverNA.cleanup()
        del self.serverNA

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterAvChoose(self):
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()
        self.avChooser.load()
        self.avChooser.enter()
        if not self.music:
            self.music = base.loadMusic(CIGlobals.ThemeSong)
            base.playMusic(self.music, volume=0.75, looping=1)
        self.accept('enterMakeAToon', self.loginFSM.request, ['makeAToon'])
        self.accept('avChooseDone', self.__handleAvChooseDone)

    def __handleAvChooseDone(self, avChoice):
        print '------- AvChooseDone -------'
        print 'Toon name: %s' % avChoice.getName()
        print 'Slot: %s' % avChoice.getSlot()
        print 'DNA: %s' % avChoice.getDNA()
        self.loginFSM.request('waitForSetAvatarResponse', [avChoice])

    def exitAvChoose(self):
        self.avChooser.exit()
        self.avChooser.unload()
        self.ignore('enterMakeAToon')
        self.ignore('avChooseDone')

    def handlePlayGame(self, msgType, di):
        if msgType == CLIENT_ENTER_OBJECT_REQUIRED_OTHER_OWNER:
            self.handleGenerateWithRequiredOtherOwner(msgType, di)
        else:
            AstronClientRepository.handleDatagram(self, di)

    def enterPlayingGame(self):
        status = {'hoodId': CIGlobals.MinigameArea,
         'zoneId': CIGlobals.MinigameAreaId,
         'avId': self.localAvId}
        shardId = self.myDistrict.doId
        self.gameFSM.request('waitForGameEnterResponse', [status, shardId])

    def exitPlayingGame(self):
        self.deleteAllObjects()
        self.handler = None
        self.gameFSM.request('off')
        if hasattr(base, 'localAvatar'):
            camera.reparentTo(render)
            camera.setPos(0, 0, 0)
            camera.setHpr(0, 0, 0)
            del base.localAvatar
            del __builtins__['localAvatar']
        self.localAvChoice = None
        if loader.inBulkBlock:
            loader.endBulkLoad(loader.blockName)
        return

    def enterNoShards(self):
        self.noShardDialog = GlobalDialog(message=CIGlobals.NoShardsMsg + ' ' + CIGlobals.TryAgain, style=2, doneEvent='noShardsDone')
        self.noShardDialog.show()
        self.acceptOnce('noShardsDone', self.handleNoShardsDone)

    def handleNoShardsDone(self):
        value = self.noShardDialog.getValue()
        if value:
            self.loginFSM.request('waitForShardList')
        else:
            sys.exit()

    def exitNoShards(self):
        self.noShardDialog.cleanup()
        del self.noShardDialog
        self.ignore('noShardsDone')

    def enterWaitForShardList(self):
        self.shardListHandle = self.addTaggedInterest(self.GameGlobalsId, CIGlobals.DistrictZone, self.ITAG_PERM, 'localShardList', event='shardList_complete')
        self.acceptOnce('shardList_complete', self._handleShardListComplete)

    def _handleShardListComplete(self):
        if self._shardsAreAvailable():
            self.myDistrict = self._chooseAShard()
            self.loginFSM.request('avChoose')
            taskMgr.add(self.monitorDistrict, 'monitorMyDistrict')
        else:
            self.loginFSM.request('noShards')

    def monitorDistrict(self, task):
        if self.myDistrict is None and self.isConnected():
            self.loginFSM.request('districtReset')
            return task.done
        else:
            return task.cont

    def _shardsAreAvailable(self):
        for shard in self.activeDistricts.values():
            if shard.available:
                return True

        return False

    def _chooseAShard(self):
        choices = []
        for shard in self.activeDistricts.values():
            choices.append(shard)

        return random.choice(choices)

    def exitWaitForShardList(self):
        self.ignore('shardList_complete')

    def enterDistrictReset(self):
        self.districtResetDialog = GlobalDialog(message=CIGlobals.DistrictResetMsg, style=3, doneEvent='distresetdone')
        self.districtResetDialog.show()
        self.acceptOnce('distresetdone', sys.exit)

    def exitDistrictReset(self):
        self.districtResetDialog.cleanup()
        del self.districtResetDialog

    def enterWaitForSetAvatarResponse(self, choice):
        self.sendSetAvatarMsg(choice)

    def enterLoadDone(self):
        self.loginFSM.request('playingGame')

    def __handleSetAvatarResponse(self, avId, di):
        print 'Entering game...'
        enterLoad = EnterLoad(self.enterLoadDone)
        dclass = self.dclassesByName['DistributedToon']
        localAvatar = LocalToon.LocalToon(base.cr)
        localAvatar.dclass = dclass
        base.localAvatar = localAvatar
        __builtins__['localAvatar'] = base.localAvatar
        localAvatar.doId = avId
        self.localAvId = avId
        parentId = None
        zoneId = None
        localAvatar.setLocation(parentId, zoneId)
        localAvatar.generateInit()
        localAvatar.generate()
        dclass.receiveUpdateBroadcastRequiredOwner(localAvatar, di)
        localAvatar.announceGenerate()
        localAvatar.postGenerateMessage()
        self.doId2do[avId] = localAvatar
        enterLoad.load()
        del enterLoad
        return

    def exitWaitForSetAvatarResponse(self):
        self.ignore(self.csm.getSetAvatarEvent())

    def enterWaitForGameEnterResponse(self, status, shardId):
        if shardId is not None:
            district = self.activeDistricts[shardId]
        else:
            district = None
        if not district:
            self.loginFSM.request('noShards')
            return
        else:
            self.myDistrict = district
            self.notify.info('Entering shard %s' % shardId)
            localAvatar.setLocation(shardId, status['zoneId'])
            localAvatar.defaultShard = shardId
            self.handleEnteredShard(status)
            return

    def handleEnteredShard(self, status):
        self.uberZoneInterest = self.addInterest(localAvatar.defaultShard, CIGlobals.UberZone, 'uberZone', 'uberZoneInterestComplete')
        self.acceptOnce('uberZoneInterestComplete', self.uberZoneInterestComplete, [status])

    def uberZoneInterestComplete(self, status):
        self.__gotTimeSync = 0
        if self.timeManager == None:
            self.notify.info('There is no time manager.')
            DistributedSmoothNode.globalActivateSmoothing(0, 0)
            self.gotTimeSync(status)
        else:
            DistributedSmoothNode.globalActivateSmoothing(1, 0)
            if self.timeManager.synchronize('startup'):
                self.accept('gotTimeSync', self.gotTimeSync, [status])
            else:
                self.gotTimeSync(status)
        return

    def exitWaitForGameEnterResponse(self):
        self.ignore('uberZoneInterestComplete')

    def gotTimeSync(self, status):
        self.notify.info('gotTimeSync')
        self.ignore('gotTimeSync')
        self.__gotTimeSync = 1
        self.prepareToEnter(status)

    def prepareToEnter(self, status):
        if not self.__gotTimeSync:
            self.notify.info('still waiting for time sync')
            return
        self.gameFSM.request('playGame', [status])

    def enterMakeAToon(self):
        slot = self.avChooser.pickAToon.slot
        if self.music:
            self.music.stop()
            self.music = None
        self.makeAToon.setSlot(slot)
        self.makeAToon.loadEnviron()
        self.makeAToon.load()
        self.makeAToon.matFSM.request('genderShop')
        self.acceptOnce('quitCreateAToon', self.__handleMakeAToonQuit)
        self.acceptOnce('createAToonFinished', self.__handleMakeAToonDone)
        return

    def __handleMakeAToonQuit(self):
        self.loginFSM.request('avChoose')

    def __handleMakeAToonDone(self, dnaStrand, slot, name):
        self.loginFSM.request('submitNewToon', enterArgList=[dnaStrand, slot, name])

    def exitMakeAToon(self):
        self.makeAToon.setSlot(-1)
        self.makeAToon.enterExit(None)
        self.ignore('quitCreateAToon')
        self.ignore('createAToonFinished')
        return

    def enterSubmitNewToon(self, dnaStrand, slot, name):
        self.submittingDialog = GlobalDialog(message=CIGlobals.Submitting)
        self.submittingDialog.show()
        self.acceptOnce(self.csm.getToonCreatedEvent(), self.__handleSubmitNewToonResp)
        self.csm.sendSubmitNewToon(dnaStrand, slot, name)

    def __handleSubmitNewToonResp(self, avId):
        self.loginFSM.request('avChoose')

    def exitSubmitNewToon(self):
        self.ignore(self.csm.getToonCreatedEvent())
        self.submittingDialog.cleanup()
        del self.submittingDialog

    def enterGameOff(self):
        pass

    def exitGameOff(self):
        pass

    def enterPlayGame(self, status):
        if self.music:
            self.music.stop()
            self.music = None
        base.transitions.noFade()
        if self.localAvChoice == None:
            self.notify.error('called enterPlayGame() without self.localAvChoice being set!')
            return
        else:
            zoneId = status['zoneId']
            hoodId = status['hoodId']
            avId = status['avId']
            self.playGame.load()
            self.playGame.enter(hoodId, zoneId, avId)
            self.myDistrict.d_joining()
            return

    def exitPlayGame(self):
        if self.music:
            self.music.stop()
            self.music = None
        self.playGame.exit()
        self.playGame.unload()
        return

    def enterDisconnect(self, isPlaying, booted = 0, bootReason = None):
        self.notify.info('Disconnect details: isPlaying = %s, booted = %s, bootReason = %s' % (isPlaying, booted, bootReason))
        style = 3
        if isPlaying == 1:
            if not booted:
                msg = CIGlobals.DisconnectionMsg
        elif not booted:
            msg = CIGlobals.JoinFailureMsg
        if self.isConnected():
            self.sendDisconnect()
        self.disconnectDialog = GlobalDialog(message=msg, style=style, doneEvent='disconnectDone')
        self.disconnectDialog.show()
        if style == 3:
            self.acceptOnce('disconnectDone', sys.exit)
        else:
            self.acceptOnce('disconnectDone', self.handleDisconnectDone)

    def handleDisconnectDone(self):
        value = self.disconnectDialog.getValue()
        if value:
            self.loginFSM.request('connect')
        else:
            sys.exit()

    def exitDisconnect(self):
        self.ignore('disconnectDone')
        self.disconnectDialog.cleanup()
        del self.disconnectDialog

    def renderFrame(self):
        gsg = base.win.getGsg()
        if gsg:
            render2d.prepareScene(gsg)
        base.graphicsEngine.renderFrame()

    def handleDatagram(self, di):
        if self.notify.getDebug():
            print 'ClientRepository received datagram:'
        msgType = self.getMsgType()
        self.currentSenderId = None
        if self.handler == None:
            self.astronHandle(di)
        else:
            self.handler(msgType, di)
        self.considerHeartbeat()
        return

    def astronHandle(self, di):
        AstronClientRepository.handleDatagram(self, di)

    def handleQuietZoneGenerateWithRequired(self, di):
        doId = di.getUint32()
        parentId = di.getUint32()
        zoneId = di.getUint32()
        classId = di.getUint16()
        dclass = self.dclassesByNumber[classId]
        if dclass.getClassDef().neverDisable:
            dclass.startGenerate()
            distObj = self.generateWithRequiredFields(dclass, doId, di, parentId, zoneId)
            dclass.stopGenerate()

    def handleQuietZoneGenerateWithRequiredOther(self, di):
        doId = di.getUint32()
        parentId = di.getUint32()
        zoneId = di.getUint32()
        classId = di.getUint16()
        dclass = self.dclassesByNumber[classId]
        if dclass.getClassDef().neverDisable:
            dclass.startGenerate()
            distObj = self.generateWithRequiredOtherFields(dclass, doId, di, parentId, zoneId)
            dclass.stopGenerate()

    def handleQuietZoneUpdateField(self, di):
        di2 = DatagramIterator(di)
        doId = di2.getUint32()
        if doId in self.deferredDoIds:
            args, deferrable, dg0, updates = self.deferredDoIds[doId]
            dclass = args[2]
            if not dclass.getClassDef().neverDisable:
                return
        else:
            do = self.getDo(doId)
            if do:
                if not do.neverDisable:
                    return
        AstronClientRepository.handleUpdateField(self, di)

    def handleDelete(self, di):
        doId = di.getUint32()
        self.deleteObject(doId)

    def _abandonShard(self):
        for doId, obj in self.doId2do.items():
            if obj.parentId == localAvatar.defaultShard and obj is not localAvatar:
                self.deleteObject(doId)

    def handleEnterObjectRequiredOwner(self, di):
        if self.loginFSM.getCurrentState().getName() == 'waitForSetAvatarResponse':
            doId = di.getUint32()
            parentId = di.getUint32()
            zoneId = di.getUint32()
            dclassId = di.getUint16()
            self.__handleSetAvatarResponse(doId, di)

    def addTaggedInterest(self, parentId, zoneId, mainTag, desc, otherTags = [], event = None):
        return self.addInterest(parentId, zoneId, desc, event)

    def sendSetAvatarMsg(self, choice):
        avId = choice.getAvId()
        self.sendSetAvatarIdMsg(avId)
        self.localAvChoice = choice

    def sendSetAvatarIdMsg(self, avId):
        if avId != self.__currentAvId:
            self.__currentAvId = avId
            self.csm.sendSetAvatar(avId)

    def sendQuietZoneRequest(self):
        self.sendSetZoneMsg(CIGlobals.QuietZone)

    def handleFullServer(self):
        messenger.send('serverFull')

    def handleGagShopEnter(self, di):
        if self.isLocalId(di.getUint32()):
            messenger.send('enterGagShop')

    def handleServerLocked(self, di):
        self.notify.warning('the server is locked, we cannot join.')
        messenger.send('serverLocked', ['locked'])

    def handleServerUnlocked(self, di):
        self.notify.info('the server is unlocked, proceeding into game...')
        messenger.send('serverUnlocked')

    def handleSystemMessage(self, di):
        messenger.send('SysMsg', [di.getString()])

    def askServerInfo(self):
        pkg = PyDatagram()
        pkg.addUint16(SERVER_INFO)
        self.send(pkg)

    def handleAdminAccess(self, di):
        if self.isLocalId(int(di.getString())):
            self.adminAccess = True

    def hasAdminAccess(self):
        if self.adminAccess:
            return True
        else:
            return False

    def setCurrentHood(self, hood):
        self.hood = hood

    def getCurrentHood(self):
        return self.hood

    def handleSuitInfo(self, di):
        self.SuitsActive = di.getUint32()
        self.invasionSize = di.getUint32()

    def handleBossSpawned(self):
        self.BossActive = 1
        messenger.send('bossSpawned')

    def handleBossInfo(self, di):
        self.BossActive = di.getUint8()

    def handleSuitsInactive(self, di):
        messenger.send('SuitsInactive')
        self.SuitsActive = 0

    def handleSuitsActive(self, di):
        self.invasionSize = di.getUint32()
        messenger.send('SuitsActive', [self.invasionSize])
        self.SuitsActive = 1

    def handleKickDoId(self, di):
        if self.isLocalId(int(di.getString())):
            self.disconnect()
            AstronClientRepository.lostConnection(self)