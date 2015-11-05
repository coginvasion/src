# Embedded file name: lib.coginvasion.toon.DistributedTailorNPCToonAI
from direct.directnotify.DirectNotifyGlobal import directNotify
import DistributedNPCToonAI

class DistributedTailorNPCToonAI(DistributedNPCToonAI.DistributedNPCToonAI):
    notify = directNotify.newCategory('DistributedTailorToonAI')