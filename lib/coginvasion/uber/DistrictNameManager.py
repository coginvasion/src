# Embedded file name: lib.coginvasion.uber.DistrictNameManager
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistrictNameManager(DistributedObjectGlobal):
    notify = directNotify.newCategory('DistrictNameManager')