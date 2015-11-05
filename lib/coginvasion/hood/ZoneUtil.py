# Embedded file name: lib.coginvasion.hood.ZoneUtil
from lib.coginvasion.globals import CIGlobals

def getWhereName(zoneId):
    if int(str(zoneId)[1]) == 0:
        return 'playground'
    if int(str(zoneId)[1]) > 0:
        return 'street'
    if int(str(zoneId)[3]) > 0 or int(str(zoneId)[2]) > 0:
        return 'interior'


def getLoaderName(zoneId):
    if getWhereName(zoneId) == 'playground':
        return 'safeZoneLoader'
    else:
        return None
        return None


def getHoodId(zoneId):
    if zoneId == CIGlobals.ToontownCentralId:
        return CIGlobals.ToontownCentral
    if zoneId == CIGlobals.MinigameAreaId:
        return CIGlobals.MinigameArea
    if zoneId == CIGlobals.RecoverAreaId:
        return CIGlobals.RecoverArea