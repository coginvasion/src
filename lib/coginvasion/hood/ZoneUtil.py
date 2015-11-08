# Embedded file name: lib.coginvasion.hood.ZoneUtil
from lib.coginvasion.globals.CIGlobals import *

def isInInterior(zoneId):
    return int(str(zoneId)[1:]) >= 500 and int(str(zoneId)[1:]) <= 999


def getWhereName(zoneId):
    if str(zoneId)[-3:] == '000':
        return 'playground'
    elif int(str(zoneId)[1:]) < 400:
        return 'street'
    elif isInInterior(zoneId):
        return 'toonInterior'
    else:
        return 'street'


def getBranchZone(zoneId):
    branchZone = zoneId - zoneId % 100
    if zoneId % 1000 >= 500:
        branchZone -= 500
    return branchZone


def getLoaderName(zoneId):
    if str(getBranchZone(zoneId))[-3:] == '000':
        return 'safeZoneLoader'
    elif int(str(getBranchZone(zoneId))[1:]) >= 100 and int(str(getBranchZone(zoneId))[1:]) <= 300:
        return 'townLoader'
    else:
        return None
        return None


def isStreetInSameHood(zoneId):
    return str(zoneId)[0] == str(base.localAvatar.zoneId)[0]


def isStreet(zoneId):
    return getWhereName(zoneId) == 'street'


def getCanonicalBranchZone(zoneId):
    return getBranchZone(getCanonicalZoneId(zoneId))


def getCanonicalZoneId(zoneId):
    zoneId = zoneId % 2000
    if zoneId < 1000:
        zoneId = zoneId + ToontownCentralId
    else:
        zoneId = zoneId - 1000 + GoofySpeedwayId
    return zoneId


def getTrueZoneId(zoneId, currentZoneId):
    hoodId = getHoodId(zoneId)
    offset = currentZoneId - currentZoneId % 2000
    if hoodId == ToontownCentral:
        return zoneId - ToontownCentralId + offset
    if hoodId == GoofySpeedway:
        return zoneId - GoofySpeedwayId + offset + 1000
    return zoneId


def getHoodId(zoneId, street = 0):
    if street:
        if str(zoneId)[0] == '1' and len(str(zoneId)) == 4:
            return DonaldsDock
        if str(zoneId)[:2] == '11' and len(str(zoneId)) == 5:
            return MinigameArea
        if str(zoneId)[:2] == '12' and len(str(zoneId)) == 5:
            return CogTropolis
        if str(zoneId)[0] == '2':
            return ToontownCentral
        if str(zoneId)[0] == '3':
            return TheBrrrgh
        if str(zoneId)[0] == '4':
            return MinniesMelodyland
        if str(zoneId)[0] == '5':
            return DaisyGardens
        if str(zoneId)[0] == '9':
            return DonaldsDreamland
    else:
        if zoneId == ToontownCentralId:
            return ToontownCentral
        if zoneId == MinigameAreaId:
            return MinigameArea
        if zoneId == RecoverAreaId:
            return RecoverArea
        if zoneId == TheBrrrghId:
            return TheBrrrgh
        if zoneId == DonaldsDreamlandId:
            return DonaldsDreamland
        if zoneId == MinniesMelodylandId:
            return MinniesMelodyland
        if zoneId == DaisyGardensId:
            return DaisyGardens
        if zoneId == DonaldsDockId:
            return DonaldsDock
        if zoneId == CogTropolisId:
            return CogTropolis


def getZoneId(hoodId):
    if hoodId == ToontownCentral or hoodId == BattleTTC:
        return ToontownCentralId
    if hoodId == MinigameArea:
        return MinigameAreaId
    if hoodId == RecoverArea:
        return RecoverAreaId
    if hoodId == TheBrrrgh:
        return TheBrrrghId
    if hoodId == DonaldsDreamland:
        return DonaldsDreamlandId
    if hoodId == MinniesMelodyland:
        return MinniesMelodylandId
    if hoodId == DaisyGardens:
        return DaisyGardensId
    if hoodId == DonaldsDock:
        return DonaldsDockId
    if hoodId == CogTropolis:
        return CogTropolisId