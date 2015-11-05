# Embedded file name: lib.coginvasion.hood.DistributedToonInteriorAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed import DistributedObjectAI
from lib.coginvasion.globals import CIGlobals
import DistributedDoorAI
from lib.coginvasion.toon import DistributedNPCToonAI, DistributedHQNPCToonAI, DistributedTailorNPCToonAI

class DistributedToonInteriorAI(DistributedObjectAI.DistributedObjectAI):
    notify = directNotify.newCategory('DistributedToonInteriorAI')

    def __init__(self, air, block, doorToZone):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.door = None
        self.doorToZone = doorToZone
        self.block = block
        self.npcs = []
        return

    def announceGenerate(self, doorType = 0):
        DistributedObjectAI.DistributedObjectAI.announceGenerate(self)
        self.door = DistributedDoorAI.DistributedDoorAI(self.air, self.block, self.doorToZone, doorType)
        self.door.generateWithRequired(self.zoneId)
        self.createNPCs()

    def createNPCs(self):
        npcIdList = CIGlobals.zone2NpcDict.get(self.zoneId, [])
        for npcId in npcIdList:
            while npcIdList.count(npcId) > 1:
                npcIdList.remove(npcId)

        for i in xrange(len(npcIdList)):
            npcId = npcIdList[i]
            npcData = CIGlobals.NPCToonDict.get(npcId)
            if npcData[3] not in [CIGlobals.NPC_REGULAR, CIGlobals.NPC_HQ, CIGlobals.NPC_TAILOR]:
                continue
            if npcData[3] == CIGlobals.NPC_REGULAR:
                npcClass = DistributedNPCToonAI.DistributedNPCToonAI
            elif npcData[3] == CIGlobals.NPC_HQ:
                npcClass = DistributedHQNPCToonAI.DistributedHQNPCToonAI
            elif npcData[3] == CIGlobals.NPC_TAILOR:
                npcClass = DistributedTailorNPCToonAI.DistributedTailorNPCToonAI
            npc = npcClass(self.air, npcId, len(self.npcs))
            npc.generateWithRequired(self.zoneId)
            self.npcs.append(npc)

    def delete(self):
        if self.door:
            self.door.requestDelete()
            self.door = None
        for npc in self.npcs:
            npc.requestDelete()

        self.npcs = None
        DistributedObjectAI.DistributedObjectAI.delete(self)
        return

    def setBlock(self, block):
        self.block = block

    def d_setBlock(self, block):
        self.sendUpdate('setBlock', [block])

    def b_setBlock(self, block):
        self.d_setBlock(block)
        self.setBlock(block)

    def getBlock(self):
        return self.block