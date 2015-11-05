# Embedded file name: lib.coginvasion.uber.LauncherLoginManagerUD
"""

  Filename: LauncherLoginManagerUD.py
  Created by: DuckyDuck1553 (08Dec14)

"""
from panda3d.core import *
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from lib.coginvasion.uber import LoginTokenGenerator

class LauncherLoginManagerUD(DistributedObjectGlobalUD):

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

    def requestLogin(self, username, password):
        sender = self.air.getMsgSender()
        dg = self.air.getDatagram(Datagram())
        ip = NetDatagram(dg).getAddress()
        if self.isValidAccount(username, password):
            self.d_loginAccepted(sender, ip)
        else:
            self.d_loginRejected(sender)

    def d_loginAccepted(self, sender, ip):
        tokenObject = LoginTokenGenerator.generateLoginToken(ip)
        token = tokenObject.getToken()
        if self.air.storeToken(tokenObject, sender) == 1:
            self.sendUpdateToChannel(sender, 'loginAccepted', [token])

    def d_loginRejected(self, sender):
        self.sendUpdateToChannel(sender, 'loginRejected', [])