# Embedded file name: lib.coginvasion.distributed.DistributedDistrict
"""

  Filename: DistributedDistrict.py
  Created by: blach (14Dec14)

"""
from direct.distributed.DistributedObject import DistributedObject
from lib.coginvasion.gui.Whisper import Whisper

class DistributedDistrict(DistributedObject):

    def __init__(self, cr):
        try:
            self.DistributedDistrict_initialized
            return
        except:
            self.DistributedDistrict_initialized = 1

        DistributedObject.__init__(self, cr)
        self.available = 0
        self.population = 0
        self.popRecord = 0
        self.name = None
        return

    def setDistrictName(self, name):
        self.name = name

    def getDistrictName(self):
        return self.name

    def setPopRecord(self, record):
        self.popRecord = record

    def getPopRecord(self):
        return self.popRecord

    def setPopulation(self, population):
        self.population = population

    def getPopulation(self):
        return self.population

    def d_joining(self):
        self.sendUpdate('joining', [])

    def systemMessage(self, message):
        Whisper().createSystemMessage(message)

    def setAvailable(self, available):
        self.available = available

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.cr.activeDistricts[self.doId] = self

    def disable(self):
        DistributedObject.disable(self)
        self.available = 0
        if self.cr.myDistrict is self:
            self.cr.myDistrict = None
        else:
            del self.cr.activeDistricts[self.doId]
        return

    def delete(self):
        DistributedObject.delete(self)
        del self.available