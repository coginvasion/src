# Embedded file name: lib.coginvasion.hood.LinkTunnel
from direct.showbase.DirectObject import DirectObject
import ZoneUtil
CollisionName = 'tunnel_trigger'
TunnelNode2LinkTunnel = {}

def __handleTunnelCollision(entry):
    intoNP = entry.getIntoNodePath()
    parent = intoNP.getParent()
    linkTunnel = TunnelNode2LinkTunnel.get(parent)
    if linkTunnel:
        zoneId = linkTunnel.data['zoneId']
        if base.cr.playGame.getPlace():
            base.cr.playGame.getPlace().fsm.request('tunnelIn', [linkTunnel])


def globalAcceptCollisions():
    base.acceptOnce('enter' + CollisionName, __handleTunnelCollision)


def globalIgnoreCollisions():
    base.ignore('enter' + CollisionName)


def getTunnelThatGoesToZone(zoneId):
    for linkTunnel in TunnelNode2LinkTunnel.values():
        if linkTunnel.data['zoneId'] == zoneId:
            return linkTunnel


def getZoneFromDNARootStr(string):
    for segment in string.split('_'):
        if segment.isdigit():
            return int(segment)


def maybeFixZone(zone):
    zone = str(zone)
    if zone[2] != '0':
        zone = zone[0] + zone[1]
        zone += '00'
    return int(zone)


class LinkTunnel(DirectObject):

    def __init__(self, tunnel, dnaRootStr):
        self.tunnel = tunnel
        TunnelNode2LinkTunnel[tunnel] = self
        self.dnaRootStr = dnaRootStr
        self.data = {}
        self.toZone = 0

    def cleanup(self):
        del TunnelNode2LinkTunnel[self.tunnel]
        del self.dnaRootStr
        del self.data
        del self.toZone


class SafeZoneLinkTunnel(LinkTunnel):
    """The tunnel in playgrounds that go to streets"""
    ToZoneLastTwo = '00'

    def __init__(self, tunnel, dnaRootStr):
        LinkTunnel.__init__(self, tunnel, dnaRootStr)
        self.inPivotPoint = (45, 91, 6.7)
        self.outPivotPoint = (35, 91, 6.7)
        self.inPivotStartHpr = (0, 0, 0)
        self.inPivotEndHpr = (-90, 0, 0)
        self.inPivotStartX = 45
        self.inPivotEndX = 35
        self.outPivotStartHpr = (90, 0, 0)
        self.outPivotEndHpr = (180, 0, 0)
        self.outPivotStartX = 35
        self.outPivotEndX = 45
        self.toonOutPos = (-15, -5, 0)
        self.toonOutHpr = (180, 0, 0)
        self.camPos = (60, 130.31, 25.34)
        self.camHpr = (180, 342.9, 0)
        toZoneFirstTwo = None
        for segment in dnaRootStr.split('_'):
            if segment.isdigit():
                toZoneFirstTwo = segment[:2]
                toZone = toZoneFirstTwo + self.ToZoneLastTwo
                self.toZone = int(segment)

        self.data['zoneId'] = self.toZone
        return


class StreetLinkTunnel(LinkTunnel):
    """The tunnel in streets that go to playgrounds"""

    def __init__(self, tunnel, dnaRootStr):
        LinkTunnel.__init__(self, tunnel, dnaRootStr)
        self.outPivotPoint = (45, 5, 0)
        self.inPivotPoint = (35, 5, 0)
        self.outPivotStartHpr = (-90, 0, 0)
        self.outPivotEndHpr = (0, 0, 0)
        self.outPivotStartX = 45
        self.outPivotEndX = 35
        self.toonOutPos = (-15, -5, 0)
        self.toonOutHpr = (180, 0, 0)
        self.inPivotStartHpr = (0, 0, 0)
        self.inPivotEndHpr = (-90, 0, 0)
        self.inPivotStartX = 35
        self.inPivotEndX = 45
        self.camPos = (19.7, -34.9, 19.08)
        self.camHpr = (0, 345.96, 0)
        for segment in dnaRootStr.split('_'):
            if segment.isdigit():
                self.toZone = int(segment)

        self.data['zoneId'] = self.toZone


class NeighborhoodLinkTunnel(LinkTunnel):
    """Goes from Street to Street (changes neighborhoods)"""
    ToZoneLastTwo = '00'

    def __init__(self, tunnel, dnaRootStr):
        LinkTunnel.__init__(self, tunnel, dnaRootStr)
        self.outPivotPoint = (25, 5, 0)
        self.inPivotPoint = (15, 5, 0)
        self.outPivotStartHpr = (-90, 0, 0)
        self.outPivotEndHpr = (0, 0, 0)
        self.outPivotStartX = 25
        self.outPivotEndX = 15
        self.toonOutPos = (-15, -5, 0)
        self.toonOutHpr = (180, 0, 0)
        self.inPivotStartHpr = (0, 0, 0)
        self.inPivotEndHpr = (-90, 0, 0)
        self.inPivotStartX = 15
        self.inPivotEndX = 25
        self.camPos = (0, -34.18, 15.32)
        self.camHpr = (0, 349.7, 0)
        for segment in dnaRootStr.split('_'):
            if segment.isdigit():
                self.toZone = int(segment)

        self.data['zoneId'] = self.toZone
        self.data['hoodId'] = ZoneUtil.getHoodId(self.toZone, 1)


def getRecommendedTunnelClassFromZone(zone):
    if ZoneUtil.getWhereName(zone) == 'playground':
        return StreetLinkTunnel
    if ZoneUtil.getWhereName(zone) == 'street':
        if ZoneUtil.getHoodId(zone) == base.cr.playGame.hood.id:
            return SafeZoneLinkTunnel
        else:
            return NeighborhoodLinkTunnel