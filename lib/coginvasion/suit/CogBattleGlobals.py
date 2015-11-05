# Embedded file name: lib.coginvasion.suit.CogBattleGlobals
from lib.coginvasion.globals.CIGlobals import BattleTTC, TheBrrrgh, DonaldsDreamland, DonaldsDock
from lib.coginvasion.hood import ZoneUtil
HoodId2HoodIndex = {BattleTTC: 0,
 TheBrrrgh: 1,
 DonaldsDreamland: 2,
 DonaldsDock: 5}
HoodIndex2HoodName = {v:k for k, v in HoodId2HoodIndex.items()}
HoodIndex2HoodId = None
if HoodIndex2HoodId == None:
    HoodIndex2HoodId = {}
    for hoodName in HoodId2HoodIndex.keys():
        index = HoodId2HoodIndex[hoodName]
        zone = ZoneUtil.getZoneId(hoodName)
        HoodIndex2HoodId[index] = zone

hi2hi = HoodId2HoodIndex
HoodIndex2LevelRange = {hi2hi[BattleTTC]: list(range(1, 6)),
 hi2hi[TheBrrrgh]: list(range(5, 10)),
 hi2hi[DonaldsDreamland]: list(range(6, 10)),
 hi2hi[DonaldsDock]: range(2, 7)}
HoodIndex2TotalCogs = {hi2hi[BattleTTC]: 40,
 hi2hi[TheBrrrgh]: 45,
 hi2hi[DonaldsDreamland]: 50,
 hi2hi[DonaldsDock]: 45}
WaiterHoodIndex = hi2hi[TheBrrrgh]
SkeletonHoodIndex = 10