# Embedded file name: lib.coginvasion.distributed.CogInvasionInternalRepository
"""

  Filename: CogInvasionUberRepository.py
  Created by: blach (10Dec14)

"""
from direct.distributed.AstronInternalRepository import AstronInternalRepository
from direct.directnotify.DirectNotifyGlobal import directNotify
from lib.coginvasion.distributed.CogInvasionDoGlobals import *

class CogInvasionInternalRepository(AstronInternalRepository):
    notify = directNotify.newCategory('CIInternalRepository')
    GameGlobalsId = DO_ID_COGINVASION
    dbId = 4003

    def getAccountIdFromSender(self):
        return self.getMsgSender() >> 32 & 4294967295L

    def getAvatarIdFromSender(self):
        return self.getMsgSender() & 4294967295L