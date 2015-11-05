# Embedded file name: lib.coginvasion.distributed.DistributedDistrictAI
"""

  Filename: DistributedDistrictAI.py
  Created by: blach (14Dec14)

"""
from direct.distributed.DistributedObjectAI import DistributedObjectAI
import time

class DistributedDistrictAI(DistributedObjectAI):

    def __init__(self, air):
        try:
            self.DistributedDistrictAI_initialized
            return
        except:
            self.DistributedDistrictAI_intialized = 1

        DistributedObjectAI.__init__(self, air)
        self.available = 0
        self.avatarIds = []
        self.population = 0
        self.popRecord = 0
        self.name = ''

    def setDistrictName(self, name):
        self.name = name

    def d_setDistrictName(self, name):
        self.sendUpdate('setDistrictName', [name])

    def b_setDistrictName(self, name):
        self.d_setDistrictName(name)
        self.setDistrictName(name)

    def getDistrictName(self):
        return self.name

    def setPopRecord(self, record):
        self.popRecord = record

    def d_setPopRecord(self, record):
        self.sendUpdate('setPopRecord', [record])

    def b_setPopRecord(self, record):
        self.d_setPopRecord(record)
        self.setPopRecord(record)

    def getPopRecord(self):
        return self.popRecord

    def announceGenerate(self):
        taskMgr.add(self.monitorAvatars, 'monitorAvatars')
        DistributedObjectAI.announceGenerate(self)

    def setPopulation(self, amount):
        self.population = amount
        if amount > self.getPopRecord():
            print 'New Population Record: ' + str(amount)
            population_file = open('astron/databases/record_population.txt', 'w')
            population_file.write(str(amount))
            population_file.flush()
            population_file.close()
            del population_file
            self.b_setPopRecord(amount)

    def d_setPopulation(self, amount):
        self.sendUpdate('setPopulation', [amount])

    def b_setPopulation(self, amount):
        self.d_setPopulation(amount)
        self.setPopulation(amount)

    def getPopulation(self):
        return self.population

    def joining(self):
        avId = self.air.getAvatarIdFromSender()
        print '[' + str(time.strftime('%m-%d-%Y %H:%M:%S')) + '] ' + str(avId) + ' is joining my district!'
        self.avatarIds.append(avId)
        self.b_setPopulation(self.getPopulation() + 1)
        self.air.districtNameMgr.d_toonJoined(avId)

    def monitorAvatars(self, task):
        for avId in self.avatarIds:
            if avId not in self.air.doId2do.keys():
                print '[' + str(time.strftime('%m-%d-%Y %H:%M:%S')) + '] ' + str(avId) + ' is leaving my district!'
                self.avatarIds.remove(avId)
                self.b_setPopulation(self.getPopulation() - 1)
                self.air.districtNameMgr.d_toonLeft(avId)

        task.delayTime = 0.5
        return task.again

    def systemMessageCommand(self, adminToken, message):
        avId = self.air.getAvatarIdFromSender()
        tokens = [0, 1]
        av = self.air.doId2do.get(avId, None)
        if av:
            if adminToken in tokens and av.getAdminToken() in tokens and av.getAdminToken() == adminToken:
                print "DistributedDistrictAI: Sending update 'systemMessage' with message: " + message
                self.sendUpdate('systemMessage', [message])
        else:
            print 'DistributedDistrictAI: Could not find the avatar that requested a system message...'
        return

    def setAvailable(self, available):
        self.available = available

    def d_setAvailable(self, available):
        self.sendUpdate('setAvailable', [available])

    def b_setAvailable(self, available):
        self.d_setAvailable(available)
        self.setAvailable(available)

    def getAvailable(self):
        return self.available

    def disable(self):
        DistributedObjectAI.disable(self)
        self.available = 0

    def delete(self):
        DistributedObjectAI.delete(self)
        del self.available