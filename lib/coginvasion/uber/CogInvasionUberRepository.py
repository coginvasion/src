# Embedded file name: lib.coginvasion.uber.CogInvasionUberRepository
"""

  Filename: CogInvasionUberRepository.py
  Created by: DuckyDuck1553 (03Dec14)

"""
from lib.coginvasion.distributed.CogInvasionInternalRepository import CogInvasionInternalRepository
from direct.directnotify.DirectNotifyGlobal import directNotify
from lib.coginvasion.distributed.DistributedRootAI import DistributedRootAI
from lib.coginvasion.distributed.CogInvasionDoGlobals import *
from direct.distributed.ParentMgr import ParentMgr
from direct.task import Task
import LoginToken
STORE_LOGIN_TOKEN = 100

class CogInvasionUberRepository(CogInvasionInternalRepository):
    notify = directNotify.newCategory('CIUberRepository')
    GameGlobalsId = DO_ID_COGINVASION

    def __init__(self, baseChannel, serverId):
        CogInvasionInternalRepository.__init__(self, baseChannel, serverId, ['astron/direct.dc', 'astron/toon.dc'], dcSuffix='UD')
        self.notify.setInfo(True)
        self.activeTokens = []
        self.parentMgr = ParentMgr()

    def getParentMgr(self, zone):
        return self.parentMgr

    def handleDatagram(self, di):
        msgType = self.getMsgType()
        if msgType == STORE_LOGIN_TOKEN:
            self.__handleLoginToken(di)
        else:
            CogInvasionInternalRepository.handleDatagram(self, di)

    def __handleLoginToken(self, di):
        token = di.getString()
        ip = di.getString()
        tokenObj = LoginToken.LoginToken(token, ip)
        self.storeToken(tokenObj)

    def isValidToken(self, token, ip):
        """
        Validate a login token.
        """
        print ip
        for tokenObj in self.activeTokens:
            if token == tokenObj.getToken():
                self.deleteToken(tokenObj)
                return 1

        return 0

    def storeToken(self, tokenObj):
        """
        Store and activate a new login token.
        """
        for token in self.activeTokens:
            if token.getIP() == tokenObj.getIP():
                self.deleteToken(token)

        self.activeTokens.append(tokenObj)
        print 'Activated token: %s' % tokenObj
        print 'Token: %s, IP: %s' % (tokenObj.getToken(), tokenObj.getIP())
        print 'Tokens: %s' % self.activeTokens
        taskMgr.doMethodLater(self.getActiveTokenLength(), self.deleteTokenTask, tokenObj.getDeleteTask(), extraArgs=[tokenObj], appendTask=True)
        return 1

    def deleteTokenTask(self, obj, task):
        self.deleteToken(obj)
        return task.done

    def deleteToken(self, token):
        """
        Delete an active login token from the activeTokens list.
        """
        taskMgr.remove(token.getDeleteTask())
        print 'Deactivated token: %s' % token
        print 'Token: %s, IP: %s' % (token.getToken(), token.getIP())
        token.cleanup()
        self.activeTokens.remove(token)
        print 'Tokens: %s' % self.activeTokens

    def isBanned(self, ip):
        return False

    def getActiveTokenLength(self):
        return 300

    def handleConnected(self):
        rootObj = DistributedRootAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)
        self.createObjects()
        self.storeToken(LoginToken.LoginToken('asdasd$asdasdASfdasdgdaAsassa4234QW34324436REGdfnjGFb', '0.0.0.0'))
        self.notify.info('Done.')

    def createObjects(self):
        self.csm = self.generateGlobalObject(DO_ID_CLIENT_SERVICES_MANAGER, 'ClientServicesManager')
        self.dnm = self.generateGlobalObject(DO_ID_DISTRICT_NAME_MANAGER, 'DistrictNameManager')
        self.friendsManager = self.generateGlobalObject(DO_ID_FRIENDS_MANAGER, 'FriendsManager')