# Embedded file name: lib.coginvasion.globals.CIGlobals
"""
  
  Filename: CIGlobals.py
  Created by: blach (17June14)
  
"""
from panda3d.core import *
from lib.coginvasion.manager.SettingsManager import SettingsManager
GeneralAnimPlayRate = 1.0
BackwardsAnimPlayRate = -1.0
OpenBookFromFrame = 29
OpenBookToFrame = 37
ReadBookFromFrame = 38
ReadBookToFrame = 118
CloseBookFromFrame = 119
CloseBookToFrame = 155
ChatBubble = 'phase_3/models/props/chatbox.bam'
ThoughtBubble = 'phase_3/models/props/chatbox_thought_cutout.bam'
ToonFont = None
SuitFont = None
MickeyFont = None
FloorOffset = 0.025
NPCWalkSpeed = 0.02
NPCRunSpeed = 0.04
OriginalCameraFov = 40.0
DefaultCameraFov = 52.0
DefaultCameraFar = 2000.0
DefaultCameraNear = 1.0
PortalScale = 1.5
SPInvalid = 0
SPHidden = 1
SPRender = 2
SPDynamic = 5
AICollisionPriority = 10
AICollMovePriority = 8
Suit = 'Cog'
Toon = 'Toon'
CChar = 'cchar'
Goofy = 'Goofy'
Mickey = 'Mickey'
Minnie = 'Minnie'
Suits = 'Cogs'
Skelesuit = 'Skelecog'
Pluto = 'Pluto'
Donald = 'Donald'
Playground = 'Playground'
RaceGame = 'Race Game'
UnoGame = 'Uno Game'
UnoCall = 'UNO!'
GunGame = 'Toon Battle'
GunGameFOV = 70.0
FactoryGame = 'Factory Prowl'
ThemeSong = 'phase_3/audio/bgm/ci_theme_old.mp3'
FloorBitmask = BitMask32(2)
WallBitmask = BitMask32(1)
EventBitmask = BitMask32(3)
DialogColor = (1, 1, 0.75, 1)
DefaultBackgroundColor = (0.3, 0.3, 0.3, 1)
PositiveTextColor = (0, 1, 0, 1)
NegativeTextColor = (1, 0, 0, 1)
Estate = 'The Estate'
ToontownCentral = 'Toontown Central'
DonaldsDock = "Donald's Dock"
MinniesMelodyland = "Minnie's Melodyland"
TheBrrrgh = 'The Brrrgh'
DonaldsDreamland = "Donald's Dreamland"
GoofySpeedway = 'Goofy Speedway'
CashbotHQ = 'Cashbot HQ'
SellbotHQ = 'Sellbot HQ'
LawbotHQ = 'Lawbot HQ'
BossbotHQ = 'Bossbot HQ'
MinigameArea = 'Minigame Area'
OutdoorZone = 'Outdoor Area'
GolfZone = 'Minigolf Area'
DaisyGardens = 'Daisy Gardens'
Minigame = 'Minigame'
RecoverArea = 'Recover Area'
ToontownCentralId = 1000
MinigameAreaId = 2000
RecoverAreaId = 3000
QuietZone = 1
UberZone = 2
DistrictZone = 3
DynamicZonesBegin = 61000
DynamicZonesEnd = 1048576
safeZoneLSRanges = {ToontownCentral: 6,
 MinigameArea: 6,
 RecoverArea: 8}
ToonStandableGround = 0.707
ToonSpeedFactor = 1.25
ToonForwardSpeed = 16.0 * ToonSpeedFactor
ToonJumpForce = 24.0
ToonReverseSpeed = 8.0 * ToonSpeedFactor
ToonRotateSpeed = 80.0 * ToonSpeedFactor
ToonForwardSlowSpeed = 6.0
ToonJumpSlowForce = 4.0
ToonReverseSlowSpeed = 2.5
ToonRotateSlowSpeed = 33.0
ErrorCode2ErrorMsg = {}
SecretPlace = 'Secret Place'
TryAgain = 'Try again?'
NoConnectionMsg = 'Could not connect to %s.'
DisconnectionMsg = 'Your internet connection to the servers has been unexpectedly broken.'
JoinFailureMsg = 'There was a problem getting you into ' + config.GetString('game-name') + '. Please restart the game.'
SuitDefeatMsg = 'You have been defeated by the ' + Suits + '! Try again?'
ConnectingMsg = 'Connecting...'
ServerUnavailable = 'The server appears to be temporarily unavailable. Still trying...'
JoiningMsg = 'Retrieving server info...'
OutdatedFilesMsg = 'Your game files are out of date. Please run the game from the launcher.'
ServerLockedMsg = 'The server is locked.'
NoShardsMsg = 'There are no available shards.'
InvalidName = 'Sorry, that name will not work.'
Submitting = 'Submitting...'
AlreadyLoggedInMsg = 'You have been disconnected because someone else has logged into this account from another computer.'
DistrictResetMsg = 'The district you were playing in has been reset. Everybody playing in that district has been logged out.'
SuitFlyingDownMsg = 'A ' + Suit + ' is flying down!'
SuitInvasionMsg = 'A ' + Suit + ' Invasion has begun!'
SuitInvasionInProgMsg = 'There is a ' + Suit + ' Invasion in progress!'
SuitTournamentInProgMsg = 'There is a ' + Suit + ' Tournament in progress!'
SuitBreakMsgArray = ['The ' + Suits + " are going on break now... but they'll be back!",
 "You've defeated them all, but they'll be back...",
 'The ' + Suits + " are rethinking their plans. They'll be back soon.",
 'The ' + Suits + ' are taking a break for a few minutes.',
 'The ' + Suits + " are exhausted from all the battling! They'll be back momentarily.",
 'The ' + Suits + ' are taking a break! This is a good time to refill on gags and Laff!']
SuitBackFromBreakMsgArray = ['The ' + Suits + ' have returned from their break!', 'The ' + Suits + ' are back!', 'The ' + Suits + ' are back from their break!']
DialogOk = 'OK'
DialogCancel = 'Cancel'
DialogNo = 'No'
DialogYes = 'Yes'
BootedMsg = 'You have been booted out by the server. Code: %s'
GameVersionURL = 'https://dl.dropboxusercontent.com/u/239921115/ToontownOnlineMultifiles/gameversion.txt'
MatNAMsg = 'Make-A-Toon is currently unavailable right now. Do you want to be given a random Toon?'
FirstTimeMsg = 'It looks like it is your first time playing. Do you want to watch a tutorial video?'
UpdateReg5Min = 'The Cog Invasion server will be restarting for an update in 5 minutes.'
UpdateReg1Min = 'The Cog Invasion server will be restarting for an update in 60 seconds.'
UpdateRegClosed = 'The Cog Invasion server will be restarting now.'
UpdateEmg5Min = 'The Cog Invasion server will be closing for an emergency update in 5 minutes.'
UpdateEmg1Min = 'The Cog Invasion server will be closing for an emergency update in 60 seconds.'
UpdateEmgClosed = "The Cog Invasion server is now closing for an emergency update. It shouldn't be too long until the server is back up."
TutorialCoachDialogue = {'intro': ["Ay, my name's Coach, and welcome to da Cog Invasion tutorial!",
           'Dis will prepare ya for da real stuff, ya know?',
           "Now since ya knew here, I'm just gon' go ovah da basics.",
           "I'll teach ya about ya gags, and dose pesky " + Suits + '.',
           "Den I'll send in some " + Suits + ' for ya to take out.',
           "Oh no, don't worry, dey ain't real.",
           "Go 'head and click dat 'OK' button when ya ready to continue."],
 'ready': ["Aight, let's get dis show on da road!"],
 'cogs': ['So deez ' + Suits + " are robots created by deez evil scientists somewhere. I got no idea who deez guys ah, I don't think anybody does.",
          "Anyway, we don't want deez '" + Suits + "' messin' wit us, so we found ah own way to take 'em down.",
          'We use pastries and otha weeyad stuff.',
          "I think it clogs der internals or somethin'."],
 'gags': ["So here's a quick look at da gags.",
          'Da LBT' + Suits[0] + "A (Let's Bust Those " + Suits + ' Association), has approved da use of only four items at da moment.',
          'Dose ah: Cream Pie Slice, Whole Cream Pie, Birthday Cake, and TNT',
          "Da TNT can only be used by purchasin' it at Goofy's Gag Shop in Toontown Central. But, for tutorial purposes, I'm gonna give ya one later on to use.",
          'Da LBT' + Suits[0] + "A requiyez all new Toons in town to specialize in all four gags before enterin'.",
          "Go 'head and click dat 'OK' button when ya ready to continue."],
 'tut1': ["Aight, so I've equipped ya wit all four gags.",
          'As you can see on da right side of ya screen, deres da gags!',
          'To select anotha gag to use, eitha press da key on ya keyboard dat matches da numba, ' + 'use da scroll wheel on ya mouse, or just simply click on da gag.',
          "Go 'head and switch ya gag to a Cream Pie Slice in any way you desiyeh."],
 'tut1complete': ["Dat was difficult, wasn't it?", "Yeah, dat's what I thought.", "Go 'head and click dat 'OK' button when ya ready to continue."],
 'tut2': ['Ya should see a ' + Suit + ' flying down somewhere.',
          'Der it is!',
          'Now, use da arrow keys to move around.',
          'Good! Walk ovah to dat ' + Suit + " and click da 'Throw Gag' button or press delete on ya keyboard to use any gag ya want on dis guy.",
          'Awesome job!',
          'Whoa, what is dat?! It looks like dat ' + Suit + ' was a naughty one and stole some of ah jellybeans.',
          'Simply walk into da item to collect it.',
          "You can use dose jellybeans you just collected der to purchase gags at Goofy's Gag Shop."],
 'tut2complete': ["Dat was difficult, wasn't it?", "Go 'head and click dat 'OK' button when ya ready to continue."],
 'tut3': ['Anotha ' + Suit + ' is flying down.',
          'Dis ' + Suit + ' is a little angry and wants to attack ya!',
          "Try to avoid a few of dis guy's attacks.",
          "Wow, you're better at dis den I thought!",
          'Now, take dis ' + Suit + ' down!'],
 'tut3complete': ['Sweet!', "Go 'head and click dat 'OK' button when ya ready to continue."],
 'tut4': ["Here's dat TNT I promised ya!", "Aight, I'm sending in a group of " + Suits + ' for ya.', "Now, throw dat TNT in a place dat you think will take 'em all out!"],
 'tut4complete': ["Kaboom! Good job!Go 'head and click dat 'OK' button when ya ready to continue."],
 'outro': ['I think ya ready for da real stuff!',
           'Oh, one last thing. If ya lose all ya Laff points, ya go sad!',
           "Once that happens, ya sent to an area similah to dis one, but it's got delicious ice cream cones everywhere.",
           'Collect dose ice cream cones in da same way you collected da stolen jellybeans, to refill ya Laff points!See ya later!']}
ModelPolys = {CChar: {'high': 1200,
         'medium': 800,
         'low': 400},
 Toon: {'high': 1000,
        'medium': 500,
        'low': 250}}
ModelDetail = None
OkayBtnGeom = None
CancelBtnGeom = None
DefaultBtnGeom = None

def getToonFont():
    global ToonFont
    if not ToonFont:
        ToonFont = loader.loadFont('phase_3/models/fonts/ImpressBT.ttf', lineHeight=1.0)
    return ToonFont


def getSuitFont():
    global SuitFont
    if not SuitFont:
        SuitFont = loader.loadFont('phase_3/models/fonts/vtRemingtonPortable.ttf', pixelsPerUnit=40, spaceAdvance=0.25, lineHeight=1.0)
    return SuitFont


def getMickeyFont():
    global MickeyFont
    if not MickeyFont:
        MickeyFont = loader.loadFont('phase_3/models/fonts/MickeyFont.bam')
    return MickeyFont


def getModelDetail(avatar):
    global ModelDetail
    width, height, fs, music, sfx, tex_detail, model_detail, aa, af = SettingsManager().getSettings('settings.json')
    ModelDetail = ModelPolys[avatar][model_detail]
    return ModelDetail


def getOkayBtnGeom():
    global OkayBtnGeom
    if not OkayBtnGeom:
        OkayBtnGeom = (loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui.bam').find('**/ChtBx_OKBtn_UP'), loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui.bam').find('**/ChtBx_OKBtn_DN'), loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui.bam').find('**/ChtBx_OKBtn_Rllvr'))
    return OkayBtnGeom


def getCancelBtnGeom():
    global CancelBtnGeom
    if not CancelBtnGeom:
        CancelBtnGeom = (loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui.bam').find('**/CloseBtn_UP'), loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui.bam').find('**/CloseBtn_DN'), loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui.bam').find('**/CloseBtn_Rllvr'))
    return CancelBtnGeom


def getDefaultBtnGeom():
    global DefaultBtnGeom
    if not DefaultBtnGeom:
        btn = loader.loadModel('phase_3/models/gui/quit_button.bam')
        DefaultBtnGeom = (btn.find('**/QuitBtn_UP'), btn.find('**/QuitBtn_DN'), btn.find('**/QuitBtn_RLVR'))
    return DefaultBtnGeom


NameTagColors = {Suit: {'fg': (0.2, 0.2, 0.2, 1.0),
        'bg': (0.8, 0.8, 0.8, 0.5)},
 Toon: {'fg': (0.8, 0.4, 0.0, 1.0),
        'bg': (0.8, 0.8, 0.8, 0.5)},
 CChar: {'fg': (0.2, 0.5, 0.0, 1.0),
         'bg': (0.8, 0.8, 0.8, 0.5)}}
LocalNameTagColor = (0.3, 0.3, 0.7, 1.0)
ShadowScales = {Suit: 0.4,
 Toon: 0.4,
 CChar: 0.55}
ToonColors = [(1.0, 1.0, 1.0, 1.0),
 (0.96875, 0.691406, 0.699219, 1.0),
 (0.933594, 0.265625, 0.28125, 1.0),
 (0.863281, 0.40625, 0.417969, 1.0),
 (0.710938, 0.234375, 0.4375, 1.0),
 (0.570312, 0.449219, 0.164062, 1.0),
 (0.640625, 0.355469, 0.269531, 1.0),
 (0.996094, 0.695312, 0.511719, 1.0),
 (0.832031, 0.5, 0.296875, 1.0),
 (0.992188, 0.480469, 0.167969, 1.0),
 (0.996094, 0.898438, 0.320312, 1.0),
 (0.996094, 0.957031, 0.597656, 1.0),
 (0.855469, 0.933594, 0.492188, 1.0),
 (0.550781, 0.824219, 0.324219, 1.0),
 (0.242188, 0.742188, 0.515625, 1.0),
 (0.304688, 0.96875, 0.402344, 1.0),
 (0.433594, 0.90625, 0.835938, 1.0),
 (0.347656, 0.820312, 0.953125, 1.0),
 (0.191406, 0.5625, 0.773438, 1.0),
 (0.558594, 0.589844, 0.875, 1.0),
 (0.285156, 0.328125, 0.726562, 1.0),
 (0.460938, 0.378906, 0.824219, 1.0),
 (0.546875, 0.28125, 0.75, 1.0),
 (0.726562, 0.472656, 0.859375, 1.0),
 (0.898438, 0.617188, 0.90625, 1.0),
 (0.7, 0.7, 0.8, 1.0),
 (0.3, 0.3, 0.35, 1.0)]
ShirtColors = [(1.0, 1.0, 1.0, 1.0),
 (0.96875, 0.691406, 0.699219, 1.0),
 (0.933594, 0.265625, 0.28125, 1.0),
 (0.863281, 0.40625, 0.417969, 1.0),
 (0.710938, 0.234375, 0.4375, 1.0),
 (0.570312, 0.449219, 0.164062, 1.0),
 (0.640625, 0.355469, 0.269531, 1.0),
 (0.996094, 0.695312, 0.511719, 1.0),
 (0.832031, 0.5, 0.296875, 1.0),
 (0.992188, 0.480469, 0.167969, 1.0),
 (0.996094, 0.898438, 0.320312, 1.0),
 (0.996094, 0.957031, 0.597656, 1.0),
 (0.855469, 0.933594, 0.492188, 1.0),
 (0.550781, 0.824219, 0.324219, 1.0),
 (0.242188, 0.742188, 0.515625, 1.0),
 (0.304688, 0.96875, 0.402344, 1.0),
 (0.433594, 0.90625, 0.835938, 1.0),
 (0.347656, 0.820312, 0.953125, 1.0),
 (0.191406, 0.5625, 0.773438, 1.0),
 (0.558594, 0.589844, 0.875, 1.0),
 (0.285156, 0.328125, 0.726562, 1.0),
 (0.460938, 0.378906, 0.824219, 1.0),
 (0.546875, 0.28125, 0.75, 1.0),
 (0.726562, 0.472656, 0.859375, 1.0),
 (0.898438, 0.617188, 0.90625, 1.0),
 (0.7, 0.7, 0.8, 1.0),
 (0.3, 0.3, 0.35, 1.0),
 (1.0, 1.0, 1.0, 1.0),
 (0.96875, 0.691406, 0.699219, 1.0),
 (0.933594, 0.265625, 0.28125, 1.0),
 (0.863281, 0.40625, 0.417969, 1.0),
 (0.710938, 0.234375, 0.4375, 1.0),
 (0.570312, 0.449219, 0.164062, 1.0),
 (0.640625, 0.355469, 0.269531, 1.0),
 (0.996094, 0.695312, 0.511719, 1.0),
 (0.832031, 0.5, 0.296875, 1.0),
 (0.992188, 0.480469, 0.167969, 1.0),
 (0.996094, 0.898438, 0.320312, 1.0),
 (0.996094, 0.957031, 0.597656, 1.0),
 (0.855469, 0.933594, 0.492188, 1.0),
 (0.550781, 0.824219, 0.324219, 1.0),
 (0.242188, 0.742188, 0.515625, 1.0),
 (0.304688, 0.96875, 0.402344, 1.0),
 (0.433594, 0.90625, 0.835938, 1.0),
 (0.347656, 0.820312, 0.953125, 1.0),
 (0.191406, 0.5625, 0.773438, 1.0),
 (0.558594, 0.589844, 0.875, 1.0),
 (0.285156, 0.328125, 0.726562, 1.0),
 (0.460938, 0.378906, 0.824219, 1.0),
 (0.546875, 0.28125, 0.75, 1.0),
 (0.726562, 0.472656, 0.859375, 1.0),
 (0.898438, 0.617188, 0.90625, 1.0),
 (0.7, 0.7, 0.8, 1.0),
 (0.3, 0.3, 0.35, 1.0)]
SuitHealTaunt = 'Here, take this med-kit.'
SuitGeneralTaunts = ["It's my day off.",
 "I believe you're in the wrong office.",
 'Have your people call my people.',
 "You're in no position to meet with me.",
 'Talk to my assistant.',
 "I don't take meetings with Toons.",
 'I excel at Toon disposal.',
 "You'll have to go through me first.",
 "You're not going to like the way I work.",
 "Let's see how you rate my job performance.",
 "I'd like some feedback on my performance.",
 'Surprised to hear from me?',
 "You've got big trouble on the line."]
SuitAttackTaunts = {'canned': ['Do you like it out of the can?',
            '"Can" you handle this?',
            "This one's fresh out of the can!",
            'Ever been attacked by canned goods before?',
            "I'd like to donate this canned good to you!",
            'Get ready to "Kick the can"!',
            'You think you "can", you think you "can".',
            "I'll throw you in the can!",
            "I'm making me a can o' toon-a!",
            "You don't taste so good out of the can."],
 'clipontie': ['Better dress for our meeting.',
               "You can't go OUT without your tie.",
               'The best dressed Cogs wear them.',
               'Try this on for size.',
               'You should dress for success.',
               'No tie, no service.',
               'Do you need help putting this on?',
               'Nothing says powerful like a good tie.',
               "Let's see if this fits.",
               'This is going to choke you up.',
               "You'll want to dress up before you go OUT.",
               "I think I'll tie you up."],
 'glowerpower': ['You looking at me?',
                 "I'm told I have very piercing eyes.",
                 'I like to stay on the cutting edge.',
                 "Jeepers, Creepers, don't you love my peepers?",
                 "Here's looking at you kid.",
                 "How's this for expressive eyes?",
                 'My eyes are my strongest feature.',
                 'The eyes have it.',
                 'Peeka-boo, I see you.',
                 'Look into my eyes...',
                 'Shall we take a peek at your future?'],
 'marketcrash': ["I'm going to crash your party.",
                 "You won't survive the crash.",
                 "I'm more than the market can bear.",
                 "I've got a real crash course for you!",
                 "Now I'll come crashing down.",
                 "I'm a real bull in the market.",
                 'Looks like the market is going down.',
                 'You had better get out quick!',
                 'Sell! Sell! Sell!',
                 'Shall I lead the recession?',
                 "Everybody's getting out, shouldn't you?"],
 'playhardball': ['So you wanna play hardball?',
                  "You don't wanna play hardball with me.",
                  'Batter up!',
                  'Hey batter, batter!',
                  "And here's the pitch...",
                  "You're going to need a relief pitcher.",
                  "I'm going to knock you out of the park.",
                  "Once you get hit, you'll run home.",
                  'This is your final inning!',
                  "You can't play with me!",
                  "I'll strike you out.",
                  "I'm throwing you a real curve ball!"],
 'sacked': ["Looks like you're getting sacked.",
            "This one's in the bag.",
            "You've been bagged.",
            'Paper or plastic?',
            'My enemies shall be sacked!',
            'I hold the Toontown record in sacks per game.',
            "You're no longer wanted around here.",
            "Your time is up around here, you're being sacked!",
            'Let me bag that for you.',
            'No defense can match my sack attack!'],
 'pickpocket': ['Let me check your valuables.',
                "Hey, what's that over there?",
                'Like taking candy from a baby.',
                'What a steal.',
                "I'll hold this for you.",
                'Watch my hands at all times.',
                'The hand is quicker than the eye.',
                "There's nothing up my sleeve.",
                'The management is not responsible for lost items.',
                "Finder's keepers.",
                "You'll never see it coming.",
                'One for me, none for you.',
                "Don't mind if I do.",
                "You won't be needing this..."],
 'fountainpen': ['This is going to leave a stain.',
                 "Let's ink this deal.",
                 'Be prepared for some permanent damage.',
                 "You're going to need a good dry cleaner.",
                 'You should change.',
                 'This fountain pen has such a nice font.',
                 "Here, I'll use my pen.",
                 'Can you read my writing?',
                 'I call this the plume of doom.',
                 "There's a blot on your performance.",
                 "Don't you hate when this happens?"],
 'hangup': ["You've been disconnected.",
            'Good bye!',
            "It's time I end our connection.",
            " ...and don't call back!",
            'Click!',
            'This conversation is over.',
            "I'm severing this link.",
            'I think you have a few hang ups.',
            "It appears you've got a weak link.",
            'Your time is up.',
            'I hope you receive this loud and clear.',
            'You got the wrong number.']}
SuitAttackDamageFactors = {'canned': 5.5,
 'clipontie': 13,
 'sacked': 7,
 'glowerpower': 5.5,
 'playhardball': 5.5,
 'marketcrash': 8,
 'pickpocket': 10,
 'fountainpen': 9,
 'hangup': 7}
SuitTimeUntilToss = {'canned': {'A': 3,
            'B': 3,
            'C': 2.2},
 'playhardball': {'A': 3,
                  'B': 3,
                  'C': 2.2},
 'clipontie': {'A': 3,
               'B': 3,
               'C': 2.2},
 'marketcrash': {'A': 3,
                 'B': 3,
                 'C': 2.2},
 'sacked': {'A': 3,
            'B': 3,
            'C': 2.2},
 'glowerpower': {'A': 1,
                 'B': 1,
                 'C': 1}}
SuitHandColors = {'c': (0.95, 0.75, 0.75, 1.0),
 's': (0.95, 0.75, 0.95, 1.0),
 'l': (0.75, 0.75, 0.95, 1.0),
 'm': (0.65, 0.95, 0.85, 1.0)}
SuitNameTagPos = {'tightwad': 5.8,
 'moneybags': 7.4,
 'micromanager': 3.5,
 'gladhander': 6.7,
 'flunky': 5.2,
 'coldcaller': 4.9,
 'ambulancechaser': 7.0,
 'beancounter': 6.3,
 'loanshark': 8.9,
 'movershaker': 7.1,
 'pencilpusher': 5.2,
 'telemarketer': 5.6,
 'backstabber': 7,
 'bigcheese': 9.8,
 'bigwig': 9.2,
 'headhunter': 7.9,
 'legaleagle': 8.75,
 'numbercruncher': 7.8,
 'pennypincher': 5.6,
 'yesman': 5.6,
 'twoface': 7.3,
 'bottomfeeder': 5.1,
 'corporateraider': 9.0,
 'mrhollywood': 9.4,
 'robberbaron': 9.4,
 'shortchange': 4.9,
 'downsizer': 6.3,
 'bloodsucker': 6.5,
 'spindoctor': 8.3,
 'namedropper': 6.3,
 'mingler': 8.0,
 'doubletalker': 6.0,
 'vp': 14.0}
SuitScales = {'tightwad': 4.5,
 'moneybags': 5.3,
 'micromanager': 2.5,
 'gladhander': 4.75,
 'flunky': 4.0,
 'coldcaller': 3.5,
 'ambulancechaser': 4.35,
 'beancounter': 4.4,
 'loanshark': 6.5,
 'movershaker': 4.75,
 'pencilpusher': 3.35,
 'telemarketer': 3.75,
 'backstabber': 4.5,
 'bigcheese': 7.0,
 'bigwig': 7.0,
 'headhunter': 6.5,
 'legaleagle': 7.125,
 'numbercruncher': 5.25,
 'pennypincher': 3.55,
 'yesman': 4.125,
 'twoface': 5.25,
 'bottomfeeder': 4.0,
 'corporateraider': 6.75,
 'mrhollywood': 7.0,
 'robberbaron': 7.0,
 'shortchange': 3.6,
 'downsizer': 4.5,
 'bloodsucker': 4.375,
 'spindoctor': 5.65,
 'namedropper': 4.35,
 'mingler': 5.75,
 'doubletalker': 4.25,
 'vp': 10}
SuitScaleFactors = {'A': 6.06,
 'B': 5.29,
 'C': 4.14}
SuitHealthAmounts = {'flunky': 20,
 'bottomfeeder': 20,
 'shortchange': 20,
 'coldcaller': 20,
 'pencilpusher': 30,
 'bloodsucker': 30,
 'pennypincher': 30,
 'telemarketer': 30,
 'yesman': 42,
 'doubletalker': 42,
 'tightwad': 42,
 'namedropper': 42,
 'micromanager': 56,
 'ambulancechaser': 56,
 'beancounter': 56,
 'gladhander': 56,
 'downsizer': 72,
 'backstabber': 72,
 'numbercruncher': 72,
 'movershaker': 72,
 'headhunter': 90,
 'spindoctor': 90,
 'moneybags': 90,
 'twoface': 90,
 'corporateraider': 110,
 'legaleagle': 110,
 'loanshark': 110,
 'mingler': 110,
 'bigcheese': 132,
 'bigwig': 132,
 'robberbaron': 132,
 'mrhollywood': 132,
 'vp': 5000}
SuitHeads = {'tightwad': 'tightwad',
 'moneybags': 'moneybags',
 'micromanager': 'micromanager',
 'gladhander': 'gladhander',
 'flunky': 'flunky',
 'shortchange': 'coldcaller',
 'ambulancechaser': 'ambulancechaser',
 'beancounter': 'beancounter',
 'loanshark': 'loanshark',
 'movershaker': 'movershaker',
 'pencilpusher': 'pencilpusher',
 'telemarketer': 'telemarketer',
 'backstabber': 'backstabber',
 'bigcheese': 'bigcheese',
 'bigwig': 'bigwig',
 'headhunter': 'headhunter',
 'legaleagle': 'legaleagle',
 'numbercruncher': 'numbercruncher',
 'pennypincher': 'pennypincher',
 'yesman': 'yesman',
 'twoface': 'twoface',
 'bottomfeeder': 'tightwad',
 'corporateraider': 'flunky',
 'mrhollywood': 'yesman',
 'robberbaron': 'yesman',
 'coldcaller': 'coldcaller',
 'downsizer': 'beancounter',
 'bloodsucker': 'movershaker',
 'spindoctor': 'telemarketer',
 'namedropper': 'numbercruncher',
 'mingler': 'twoface',
 'doubletalker': 'twoface',
 'vp': None}
toonBodyScales = {'mouse': 0.6,
 'cat': 0.73,
 'duck': 0.66,
 'rabbit': 0.74,
 'horse': 0.85,
 'dog': 0.85,
 'monkey': 0.68,
 'bear': 0.85,
 'pig': 0.77}
toonHeadScales = {'mouse': Point3(1.0),
 'cat': Point3(1.0),
 'duck': Point3(1.0),
 'rabbit': Point3(1.0),
 'horse': Point3(1.0),
 'dog': Point3(1.0),
 'monkey': Point3(1.0),
 'bear': Point3(1.0),
 'pig': Point3(1.0)}
legHeightDict = {'dgs': 1.5,
 'dgm': 2.0,
 'dgl': 2.75}
torsoHeightDict = {'dgs_shorts': 1.5,
 'dgm_shorts': 1.75,
 'dgl_shorts': 2.25,
 'dgs_skirt': 1.5,
 'dgm_skirt': 1.75,
 'dgl_skirt': 2.25}
headHeightDict = {'3': 0.75,
 '1': 0.5,
 '2': 0.5,
 '4': 0.75,
 'dgs_shorts': 0.5,
 'dgl_shorts': 0.75,
 'dgm_shorts': 0.75,
 'dgm_skirt': 0.5}
SuitPathHeights = {ToontownCentralId: 0}
SuitSpawnPoints = [LPoint3f(17, -17, 4.025),
 LPoint3f(17.5, 7.6, 4.025),
 LPoint3f(85, 11.5, 4.025),
 LPoint3f(85, -13, 4.025),
 LPoint3f(-27.5, -5.25, 0.0),
 LPoint3f(-106.15, -4.0, -2.5),
 LPoint3f(-89.5, 93.5, 0.5),
 LPoint3f(-139.95, 1.69, 0.5),
 LPoint3f(-110.95, -68.57, 0.5),
 LPoint3f(70.0001, -1.90735e-06, 4),
 LPoint3f(35.0001, -1.90735e-06, 4),
 LPoint3f(52.5001, 19, 4),
 LPoint3f(52.5001, -19, 4),
 LPoint3f(-9.99991, 50, 2.6226e-06),
 LPoint3f(-9.99991, -50, 2.6226e-06),
 LPoint3f(-40.8999, -87.6, 0.500003),
 LPoint3f(-40.8999, 87.6, 0.500003),
 LPoint3f(-116.86, -50, 0.500003),
 LPoint3f(-116.86, 50, 2.6226e-06),
 LPoint3f(-75.8099, 71.28, 2.6226e-06),
 LPoint3f(-75.8099, -71.28, 2.6226e-06),
 LPoint3f(-40.8999, 61.23, 2.6226e-06),
 LPoint3f(-40.8999, -61.23, 2.6226e-06),
 LPoint3f(-25.2999, 26.5, 2.6226e-06),
 LPoint3f(-25.2999, -26.5, 2.6226e-06)]
SuitPaths = [LPoint3f(17, -17, 0.5),
 LPoint3f(17.5, 7.6, 0.5),
 LPoint3f(85, 11.5, 0.5),
 LPoint3f(85, -13, 0.5),
 LPoint3f(-27.5, -5.25, 0.5),
 LPoint3f(-106.15, -4.0, 0.5),
 LPoint3f(-89.5, 93.5, 0.5),
 LPoint3f(-139.95, 1.69, 0.5),
 LPoint3f(-110.95, -68.57, 0.5),
 LPoint3f(70.0001, -1.90735e-06, 0.5),
 LPoint3f(35.0001, -1.90735e-06, 0.5),
 LPoint3f(52.5001, 19, 0.5),
 LPoint3f(52.5001, -19, 0.5),
 LPoint3f(-9.99991, 50, 0.5),
 LPoint3f(-9.99991, -50, 0.5),
 LPoint3f(-40.8999, -87.6, 0.5),
 LPoint3f(-40.8999, 87.6, 0.5),
 LPoint3f(-116.86, -50, 0.5),
 LPoint3f(-116.86, 50, 0.5),
 LPoint3f(-75.8099, 71.28, 0.5),
 LPoint3f(-75.8099, -71.28, 0.5),
 LPoint3f(-40.8999, 61.23, 0.5),
 LPoint3f(-40.8999, -61.23, 0.5),
 LPoint3f(-25.2999, 26.5, 0.5),
 LPoint3f(-25.2999, -26.5, 0.5)]
SuitNames = {'tightwad': 'Tightwad',
 'moneybags': 'Money Bags',
 'micromanager': 'Micromanager',
 'gladhander': 'Glad Hander',
 'flunky': 'Flunky',
 'coldcaller': 'Cold Caller',
 'ambulancechaser': 'Ambulance Chaser',
 'beancounter': 'Bean Counter',
 'loanshark': 'Loan Shark',
 'movershaker': 'Mover & Shaker',
 'pencilpusher': 'Pencil Pusher',
 'telemarketer': 'Telemarketer',
 'backstabber': 'Back Stabber',
 'bigcheese': 'The Big Cheese',
 'bigwig': 'Big Wig',
 'headhunter': 'Head Hunter',
 'legaleagle': 'Legal Eagle',
 'numbercruncher': 'Number Cruncher',
 'pennypincher': 'Penny Pincher',
 'yesman': 'Yesman',
 'twoface': 'Two-Face',
 'bottomfeeder': 'Bottom Feeder',
 'corporateraider': 'Corporate Raider',
 'mrhollywood': 'Mr. Hollywood',
 'robberbaron': 'Robber Baron',
 'shortchange': 'Short Change',
 'downsizer': 'Downsizer',
 'bloodsucker': 'Bloodsucker',
 'spindoctor': 'Spin Doctor',
 'namedropper': 'Name Dropper',
 'mingler': 'The Mingler',
 'doubletalker': 'Double Talker',
 'vp': 'Senior V.P'}
SuitSharedHeads = ['bottomfeeder',
 'corporateraider',
 'robberbaron',
 'coldcaller',
 'bloodsucker',
 'spindoctor',
 'namedropper',
 'mingler',
 'doubletalker']
SuitAttacks = ['canned',
 'clipontie',
 'sacked',
 'glowerpower',
 'playhardball',
 'marketcrash',
 'pickpocket',
 'fountainpen',
 'hangup']
SuitAttackLengths = {'canned': 4,
 'clipontie': 4,
 'sacked': 4,
 'glowerpower': 2.5,
 'playhardball': 4,
 'marketcrash': 4,
 'pickpocket': 3,
 'fountainpen': 3,
 'hangup': 4}
MickeyPaths = {'a': Point3(17, -17, 4.025),
 'b': Point3(17.5, 7.6, 4.025),
 'c': Point3(85, 11.5, 4.025),
 'd': Point3(85, -13, 4.025),
 'e': Point3(-27.5, -5.25, 0.0),
 'f': Point3(-106.15, -4.0, -2.5),
 'g': Point3(-89.5, 93.5, 0.5),
 'h': Point3(-139.95, 1.69, 0.5),
 'i': Point3(-110.95, -68.57, 0.5)}
GagShopGoodbye = 'See you later!'
GagShopNoMoney = 'Sorry, you need more jellybeans to shop! Pickup jellybeans from fallen ' + Suits + ' or play minigames to get more.'
SharedChatterGreetings = ['Hi, %s!',
 'Yoo-hoo %s, nice to see you.',
 "I'm glad you're here today!",
 'Well, hello there, %s.']
SharedChatterComments = ["That's a great name, %s.",
 'I like your name.',
 'Watch out for the Cogs.',
 'Looks like the trolley is coming!',
 'I need to go to see Goofy to get some pies!',
 'Whew, I just stopped a bunch of Cogs. I need a rest!',
 'Yikes, some of those Cogs are big guys!',
 "You look like you're having fun.",
 "Oh boy, I'm having a good day.",
 "I like what you're wearing.",
 "I think I'll go fishing this afternoon.",
 'Have fun in my neighborhood.',
 'I hope you are enjoying your stay in Toontown!',
 "I heard it's snowing at the Brrrgh.",
 'Have you ridden the trolley today?',
 'I like to meet new people.',
 'Wow, there are lots of Cogs in the Brrrgh.',
 'I love to play tag. Do you?',
 'Trolley games are fun to play.',
 'I like to make people laugh.',
 "It's fun helping my friends.",
 "A-hem, are you lost?  Don't forget your map is in your Shticker Book.",
 'I hear Daisy has planted some new flowers in her garden.',
 'If you press the Ctrl key, you can jump!']
SharedChatterGoodbyes = ['I have to go now, bye!',
 "I think I'll go play a trolley game.",
 "Well, so long. I'll be seeing you, %s!",
 "I'd better hurry and get to work stopping those Cogs.",
 "It's time for me to get going.",
 'Sorry, but I have to go.',
 'Good-bye.',
 'See you later, %s!',
 "I think I'm going to go practice tossing cupcakes.",
 "I'm going to join a group and stop some Cogs.",
 'It was nice to see you today, %s.',
 "I have a lot to do today. I'd better get busy."]
MickeyChatter = ['Welcome to Toontown Central.',
 "Hi, my name is Mickey. What's yours?",
 'Hey, have you seen Donald?',
 "I'm going to go watch the fog roll in at Donald's Dock.",
 'If you see my pal Goofy, say hi to him for me.',
 'I hear Daisy has planted some new flowers in her garden.',
 "I'm going to MelodyLand to see Minnie!",
 "Gosh, I'm late for my date with Minnie!",
 "Looks like it's time for Pluto's dinner!",
 "I think I'll go swimming at Donald's Dock.",
 "It's time for a nap. I'm going to Dreamland."]
MinnieChatter = ['Welcome to Melodyland.',
 "Hi, my name is Minnie. What's yours?",
 'The hills are alive with the sound of music!',
 'You have a cool outfit, %s.',
 'Hey, have you seen Mickey?',
 'If you see my friend Goofy, say hi to him for me.',
 "Wow, there are lots of Cogs near Donald's Dreamland.",
 "I heard it's foggy at the Donald's Dock.",
 "Be sure and try the maze in Daisy Gardens.I think I'll go catch some tunes.",
 'Hey %s, look at that over there.',
 'I love the sound of music.',
 "I bet you didn't know Melodyland is also called TuneTown!  Hee Hee!",
 'I love to play the Matching Game. Do you?',
 'I like to make people giggle.',
 'Boy, trotting around in heels all day is hard on your feet!',
 'Nice shirt, %s.',
 'Is that a Jellybean on the ground?',
 "Gosh, I'm late for my date with Mickey!",
 "Looks like it's time for Pluto's dinner.",
 "It's time for a nap. I'm going to Dreamland."]
GoofySpeedwayChatter = ['Welcome to ' + ToontownCentral + '.',
 'Hi, my name is ' + Goofy + ". What's yours?",
 "Gawrsh, it's nice to see you %s!",
 'Boy, I saw a terrific race earlier.',
 'Watch out for banana peels on the race track!',
 'Have you upgraded your kart lately?',
 'We just got in some new rims at the kart shop.',
 'Hey, have you seen ' + Donald + '?',
 'If you see my friend ' + Mickey + ', say hi to him for me.',
 "D'oh! I forgot to fix " + Mickey + "'s breakfast!",
 'Gawrsh there sure are a lot of ' + Suits + ' near ' + DonaldsDock + '.',
 'At the Brrrgh branch of my Gag Shop, Hypno-Goggles are on sale for only 1 Jellybean!',
 "Goofy's Gag Shops offer the best jokes, tricks, and funnybone-ticklers in all of Toontown!",
 "At Goofy's Gag Shops, every pie in the face is guaranteed to make a laugh or you get your Jellybeans back!",
 "I'm going to Melody Land to see %s!" % Mickey,
 "Gosh, I'm late for my game with %s!" % Donald,
 "I think I'll go swimming at " + DonaldsDock + '.',
 "It's time for a nap. I'm going to Dreamland."]