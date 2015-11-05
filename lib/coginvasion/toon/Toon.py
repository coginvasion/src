# Embedded file name: lib.coginvasion.toon.Toon
"""

  Filename: Toon.py
  Created by: blach (??July14)
  
"""
from lib.coginvasion.globals import CIGlobals
from lib.coginvasion.avatar import Avatar
from direct.actor.Actor import Actor
from direct.directnotify.DirectNotify import DirectNotify
from lib.coginvasion.toon.ToonHead import ToonHead
from direct.showbase.ShadowPlacer import ShadowPlacer
from panda3d.core import *
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.showbase import Audio3DManager
from direct.interval.IntervalGlobal import *
from direct.distributed import DelayDelete
from LabelScaler import LabelScaler
from direct.showbase.ShadowDemo import *
import ToonDNA
import random
import Pies
notify = DirectNotify().newCategory('Toon')

class Toon(Avatar.Avatar, ToonHead, ToonDNA.ToonDNA):
    audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], camera)
    audio3d.setDistanceFactor(25)
    audio3d.setDropOffFactor(0.025)

    def __init__(self, cr, mat = 0):
        self.cr = cr
        try:
            self.Toon_initialized
            return
        except:
            self.Toon_initialized = 1

        Avatar.Avatar.__init__(self, mat)
        ToonDNA.ToonDNA.__init__(self)
        ToonHead.__init__(self, cr)
        self.forwardSpeed = 0.0
        self.rotateSpeed = 0.0
        self.avatarType = CIGlobals.Toon
        self.track = None
        self.standWalkRunReverse = None
        self.currentAnim = None
        self.tag = None
        self.money = 0
        self.lookAtTrack = None
        self.portal1 = None
        self.portal2 = None
        self.gunAttached = False
        self.gun = None
        self.tokenIcon = None
        self.tokenIconIval = None
        self.pies = Pies.Pies()
        self.pies.setAvatar(self)
        self.fallSfx = self.audio3d.loadSfx('phase_4/audio/sfx/MG_cannon_hit_dirt.mp3')
        self.audio3d.attachSoundToObject(self.fallSfx, self)
        self.eyes = loader.loadTexture('phase_3/maps/eyes.jpg', 'phase_3/maps/eyes_a.rgb')
        self.myTaskId = random.uniform(0, 1231231232132131231232L)
        self.closedEyes = loader.loadTexture('phase_3/maps/eyesClosed.jpg', 'phase_3/maps/eyesClosed_a.rgb')
        self.soundChatBubble = loader.loadSfx('phase_3/audio/sfx/GUI_balloon_popup.mp3')
        self.shadowCaster = None
        self.chatSoundDict = {}
        self.animFSM = ClassicFSM('Toon', [State('off', self.enterOff, self.exitOff),
         State('neutral', self.enterNeutral, self.exitNeutral),
         State('swim', self.enterSwim, self.exitSwim),
         State('walk', self.enterWalk, self.exitWalk),
         State('run', self.enterRun, self.exitRun),
         State('openBook', self.enterOpenBook, self.exitOpenBook),
         State('readBook', self.enterReadBook, self.exitReadBook),
         State('closeBook', self.enterCloseBook, self.exitCloseBook),
         State('teleportOut', self.enterTeleportOut, self.exitTeleportOut),
         State('teleportIn', self.enterTeleportIn, self.exitTeleportIn),
         State('died', self.enterDied, self.exitDied),
         State('fallFWD', self.enterFallFWD, self.exitFallFWD),
         State('fallBCK', self.enterFallBCK, self.exitFallBCK),
         State('jump', self.enterJump, self.exitJump),
         State('leap', self.enterLeap, self.exitLeap),
         State('laugh', self.enterLaugh, self.exitLaugh),
         State('happy', self.enterHappy, self.exitHappy),
         State('shrug', self.enterShrug, self.exitShrug),
         State('hdance', self.enterHDance, self.exitHDance),
         State('wave', self.enterWave, self.exitWave),
         State('scientistEmcee', self.enterScientistEmcee, self.exitScientistEmcee),
         State('scientistWork', self.enterScientistWork, self.exitScientistWork),
         State('scientistGame', self.enterScientistGame, self.exitScientistGame),
         State('scientistJealous', self.enterScientistJealous, self.exitScientistJealous),
         State('cringe', self.enterCringe, self.exitCringe),
         State('conked', self.enterConked, self.exitConked)], 'off', 'off')
        animStateList = self.animFSM.getStates()
        self.animFSM.enterInitialState()
        Avatar.Avatar.initializeBodyCollisions(self, self.avatarType, 3, 1.5)
        return

    def updateChatSoundDict(self):
        self.chatSoundDict['exclaim'] = self.audio3d.loadSfx(self.getToonAnimalNoise('exclaim'))
        self.chatSoundDict['question'] = self.audio3d.loadSfx(self.getToonAnimalNoise('question'))
        self.chatSoundDict['short'] = self.audio3d.loadSfx(self.getToonAnimalNoise('short'))
        self.chatSoundDict['medium'] = self.audio3d.loadSfx(self.getToonAnimalNoise('med'))
        self.chatSoundDict['long'] = self.audio3d.loadSfx(self.getToonAnimalNoise('long'))
        self.chatSoundDict['howl'] = self.audio3d.loadSfx(self.getToonAnimalNoise('howl'))
        self.audio3d.attachSoundToObject(self.chatSoundDict['exclaim'], self.getPart('head'))
        self.audio3d.attachSoundToObject(self.chatSoundDict['question'], self.getPart('head'))
        self.audio3d.attachSoundToObject(self.chatSoundDict['short'], self.getPart('head'))
        self.audio3d.attachSoundToObject(self.chatSoundDict['medium'], self.getPart('head'))
        self.audio3d.attachSoundToObject(self.chatSoundDict['long'], self.getPart('head'))
        self.audio3d.attachSoundToObject(self.chatSoundDict['howl'], self.getPart('head'))

    def ghostOn(self):
        self.getGeomNode().hide()
        self.getNameTag().hide()
        self.getShadow().hide()
        if self.tokenIcon:
            self.tokenIcon.hide()
        self.stashBodyCollisions()

    def ghostOff(self):
        self.unstashBodyCollisions()
        if self.tokenIcon:
            self.tokenIcon.show()
        self.getShadow().show()
        self.getNameTag().show()
        self.getGeomNode().show()

    def attachGun(self, gunName):
        self.detachGun()
        if gunName == 'pistol':
            self.gun = loader.loadModel('phase_4/models/props/water-gun.bam')
            self.gun.reparentTo(self.find('**/def_joint_right_hold'))
            self.gun.setPos(Point3(0.28, 0.1, 0.08))
            self.gun.setHpr(VBase3(85.6, -4.44, 94.43))
            self.gunAttached = True
        elif gunName == 'shotgun':
            self.gun = loader.loadModel('phase_4/models/props/shotgun.egg')
            self.gun.setScale(0.75)
            self.gun.reparentTo(self.find('**/def_joint_right_hold'))
            self.gun.setPos(Point3(-0.5, -0.2, 0.19))
            self.gun.setHpr(Vec3(350, 272.05, 0))
            color = random.choice([VBase4(1, 0.25, 0.25, 1), VBase4(0.25, 1, 0.25, 1), VBase4(0.25, 0.25, 1, 1)])
            self.gun.setColorScale(color)
            self.gunAttached = True

    def detachGun(self):
        if self.gun and self.gunAttached:
            self.gun.removeNode()
            self.gun = None
            self.gunAttached = False
        return

    def stopAnimations(self):
        if hasattr(self, 'animFSM'):
            if not self.animFSM.isInternalStateInFlux():
                self.animFSM.request('off')
            else:
                notify.warning('animFSM in flux, state=%s, not requesting off' % self.animFSM.getCurrentState().getName())
        else:
            notify.warning('animFSM has been deleted')
        if self.track != None:
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        return

    def disable(self):
        try:
            self.Toon_disabled
        except:
            self.Toon_disabled = 1
            self.pies.delete()
            self.stopAnimations()
            self.removeAdminToken()
            self.deleteCurrentToon()
            self.chatSoundDict = {}

    def delete(self):
        try:
            self.Toon_deleted
        except:
            self.Toon_deleted = 1
            del self.animFSM
            self.forwardSpeed = None
            self.chatSoundDict = None
            self.rotateSpeed = None
            self.avatarType = None
            self.track = None
            self.standWalkRunReverse = None
            self.currentAnim = None
            self.toon_head = None
            self.toon_torso = None
            self.toon_legs = None
            self.gender = None
            self.headtype = None
            self.head = None
            self.legtype = None
            self.torsotype = None
            self.hr = None
            self.hg = None
            self.hb = None
            self.tr = None
            self.tg = None
            self.tb = None
            self.lr = None
            self.lg = None
            self.lb = None
            self.shir = None
            self.shig = None
            self.shib = None
            self.shor = None
            self.shog = None
            self.shob = None
            self.shirt = None
            self.sleeve = None
            self.short = None
            self.tag = None
            self.money = None
            self.lookAtTrack = None
            self.portal1 = None
            self.portal2 = None
            self.pies = None
            self.fallSfx = None
            self.eyes = None
            self.myTaskId = None
            self.closedEyes = None
            self.soundChatBubble = None
            Avatar.Avatar.delete(self)

        return

    def initCollisions(self):
        self.collNodePath.setCollideMask(BitMask32(0))
        self.collNodePath.node().setFromCollideMask(CIGlobals.WallBitmask)
        pusher = CollisionHandlerPusher()
        pusher.setInPattern('%in')
        pusher.addCollider(self.collNodePath, self)
        base.cTrav.addCollider(self.collNodePath, pusher)

    def deleteCurrentToon(self):
        if self.shadowCaster:
            self.shadowCaster.clear()
            self.shadowCaster = None
        self.stopLookAround()
        self.stopBlink()
        self.pupils = []
        if 'head' in self._Actor__commonBundleHandles:
            del self._Actor__commonBundleHandles['head']
        if 'torso' in self._Actor__commonBundleHandles:
            del self._Actor__commonBundleHandles['torso']
        if 'legs' in self._Actor__commonBundleHandles:
            del self._Actor__commonBundleHandles['legs']
        self.deleteShadow()
        self.removePart('head')
        self.removePart('torso')
        self.removePart('legs')
        self.detachGun()
        return

    def enterGagShop(self):
        DirectLabel(text='ENTERED GAG SHOP', relief=None, text_scale=0.08)
        return

    def setAdminToken(self, tokenId):
        tokens = {0: 500,
         1: 1000}
        icons = loader.loadModel('phase_3/models/props/gm_icons.bam')
        self.tokenIcon = icons.find('**/access_level_%s' % tokens[tokenId])
        self.tokenIcon.reparentTo(self)
        self.tokenIcon.setPos(self.tag.getPos() + (0, 0, 0.5))
        self.tokenIcon.setScale(0.4)
        self.tokenIconIval = Sequence(LerpHprInterval(self.tokenIcon, duration=3.0, hpr=Vec3(360, 0, 0), startHpr=Vec3(0, 0, 0)))
        self.tokenIconIval.loop()
        icons.removeNode()

    def removeAdminToken(self):
        if self.tokenIcon != None and self.tokenIconIval != None:
            self.tokenIconIval.finish()
            self.tokenIcon.removeNode()
            self.tokenIconIval = None
            self.tokenIcon = None
        return

    def setChat(self, chatString):
        if not self.isThought(chatString):
            if not self.getGhost() or self.doId == base.localAvatar.doId:
                if 'ooo' in chatString.lower():
                    sfx = self.chatSoundDict['howl']
                elif '!' in chatString.lower():
                    sfx = self.chatSoundDict['exclaim']
                elif '?' in chatString.lower():
                    sfx = self.chatSoundDict['question']
                elif len(chatString) <= 9:
                    sfx = self.chatSoundDict['short']
                elif 10 <= len(chatString) <= 19:
                    sfx = self.chatSoundDict['medium']
                elif len(chatString) >= 20:
                    sfx = self.chatSoundDict['long']
                sfx.play()
        Avatar.Avatar.setChat(self, chatString)

    def setName(self, nameString):
        Avatar.Avatar.setName(self, nameString, avatarType=self.avatarType)

    def setDNAStrand(self, dnaStrand):
        ToonDNA.ToonDNA.setDNAStrand(self, dnaStrand)
        self.deleteCurrentToon()
        self.generateToon()

    def generateToon(self):
        self.generateLegs()
        self.generateTorso()
        self.generateHead()
        self.setToonColor()
        self.setClothes()
        self.setGloves()
        self.parentToonParts()
        self.rescaleToon()
        self.setupNameTag()
        Avatar.Avatar.initShadow(self)
        if self.pies.getPieType() == 3:
            self.attachTNT()
        if self.cr.isShowingPlayerIds:
            self.showAvId()
        self.updateChatSoundDict()

    def attachTNT(self):
        self.pies.attachTNT()
        self.holdTNTAnim()

    def detachTNT(self):
        self.pies.detachTNT()
        self.animFSM.request(self.animFSM.getCurrentState().getName())

    def holdTNTAnim(self):
        self.pose('toss', 22, partName='torso')

    def parentToonParts(self):
        self.attach('head', 'torso', 'def_head')
        self.attach('torso', 'legs', 'joint_hips')

    def unparentToonParts(self):
        self.getPart('head').reparentTo(self.getGeomNode())
        self.getPart('torso').reparentTo(self.getGeomNode())
        self.getPart('legs').reparentTo(self.getGeomNode())

    def rescaleToon(self):
        animal = self.getAnimal()
        bodyScale = CIGlobals.toonBodyScales[animal]
        headScale = CIGlobals.toonHeadScales[animal][2]
        shoulderHeight = CIGlobals.legHeightDict[self.legs] * bodyScale + CIGlobals.torsoHeightDict[self.torso] * bodyScale
        height = shoulderHeight + CIGlobals.headHeightDict[self.head] * headScale
        bodyScale = CIGlobals.toonBodyScales[animal]
        self.setAvatarScale(bodyScale)
        self.setHeight(height)

    def setGloves(self):
        color = self.getGloveColor()
        gloves = self.find('**/hands')
        gloves.setColor(color)

    def setClothes(self):
        shirt, shirtcolor = self.getShirtStyle()
        short, shortcolor = self.getShortStyle()
        sleeve, sleevecolor = self.getSleeveStyle()
        torsot = self.findAllMatches('**/torso-top')
        torsob = self.findAllMatches('**/torso-bot')
        sleeves = self.findAllMatches('**/sleeves')
        torsot.setTexture(loader.loadTexture(shirt), 1)
        torsob.setTexture(loader.loadTexture(short), 1)
        sleeves.setTexture(loader.loadTexture(sleeve), 1)
        torsot.setColor(shirtcolor)
        sleeves.setColor(sleevecolor)
        torsob.setColor(shortcolor)

    def generateLegs(self):
        legtype = self.getLegs()
        self.loadModel('phase_3/models/char/tt_a_chr_' + legtype + '_shorts_legs_' + str(CIGlobals.getModelDetail(self.avatarType)) + '.bam', 'legs')
        self.loadAnims({'neutral': 'phase_3/models/char/tt_a_chr_' + legtype + '_shorts_legs_neutral.bam',
         'run': 'phase_3/models/char/tt_a_chr_' + legtype + '_shorts_legs_run.bam',
         'walk': 'phase_3.5/models/char/tt_a_chr_' + legtype + '_shorts_legs_walk.bam',
         'pie': 'phase_3.5/models/char/tt_a_chr_' + legtype + '_shorts_legs_pie-throw.bam',
         'fallb': 'phase_4/models/char/tt_a_chr_' + legtype + '_shorts_legs_slip-backward.bam',
         'fallf': 'phase_4/models/char/tt_a_chr_' + legtype + '_shorts_legs_slip-forward.bam',
         'lose': 'phase_5/models/char/tt_a_chr_' + legtype + '_shorts_legs_lose.bam',
         'win': 'phase_3.5/models/char/tt_a_chr_' + legtype + '_shorts_legs_victory-dance.bam',
         'squirt': 'phase_5/models/char/tt_a_chr_' + legtype + '_shorts_legs_water-gun.bam',
         'zend': 'phase_3.5/models/char/tt_a_chr_' + legtype + '_shorts_legs_jump-zend.bam',
         'tele': 'phase_3.5/models/char/tt_a_chr_' + legtype + '_shorts_legs_teleport.bam',
         'book': 'phase_3.5/models/char/tt_a_chr_' + legtype + '_shorts_legs_book.bam',
         'leap': 'phase_3.5/models/char/tt_a_chr_' + legtype + '_shorts_legs_leap_zhang.bam',
         'jump': 'phase_3.5/models/char/tt_a_chr_' + legtype + '_shorts_legs_jump-zhang.bam',
         'happy': 'phase_3.5/models/char/tt_a_chr_' + legtype + '_shorts_legs_jump.bam',
         'shrug': 'phase_3.5/models/char/tt_a_chr_' + legtype + '_shorts_legs_shrug.bam',
         'hdance': 'phase_5/models/char/tt_a_chr_' + legtype + '_shorts_legs_happy-dance.bam',
         'wave': 'phase_3.5/models/char/tt_a_chr_' + legtype + '_shorts_legs_wave.bam',
         'scemcee': 'phase_4/models/char/tt_a_chr_dgm_shorts_legs_scientistEmcee.bam',
         'scwork': 'phase_4/models/char/tt_a_chr_' + legtype + '_shorts_legs_scientistWork.bam',
         'scgame': 'phase_4/models/char/tt_a_chr_' + legtype + '_shorts_legs_scientistGame.bam',
         'scjealous': 'phase_4/models/char/tt_a_chr_' + legtype + '_shorts_legs_scientistJealous.bam',
         'swim': 'phase_4/models/char/tt_a_chr_' + legtype + '_shorts_legs_swim.bam',
         'toss': 'phase_5/models/char/tt_a_chr_' + legtype + '_shorts_legs_toss.bam',
         'cringe': 'phase_3.5/models/char/tt_a_chr_' + legtype + '_shorts_legs_cringe.bam',
         'conked': 'phase_3.5/models/char/tt_a_chr_' + legtype + '_shorts_legs_conked.bam'}, 'legs')
        self.findAllMatches('**/boots_long').stash()
        self.findAllMatches('**/boots_short').stash()
        self.findAllMatches('**/shoes').stash()

    def generateTorso(self):
        torsotype = self.getTorso()
        self.loadModel('phase_3/models/char/tt_a_chr_' + torsotype + '_torso_' + str(CIGlobals.getModelDetail(self.avatarType)) + '.bam', 'torso')
        self.loadAnims({'neutral': 'phase_3/models/char/tt_a_chr_' + torsotype + '_torso_neutral.bam',
         'run': 'phase_3/models/char/tt_a_chr_' + torsotype + '_torso_run.bam',
         'walk': 'phase_3.5/models/char/tt_a_chr_' + torsotype + '_torso_walk.bam',
         'pie': 'phase_3.5/models/char/tt_a_chr_' + torsotype + '_torso_pie-throw.bam',
         'fallb': 'phase_4/models/char/tt_a_chr_' + torsotype + '_torso_slip-backward.bam',
         'fallf': 'phase_4/models/char/tt_a_chr_' + torsotype + '_torso_slip-forward.bam',
         'lose': 'phase_5/models/char/tt_a_chr_' + torsotype + '_torso_lose.bam',
         'win': 'phase_3.5/models/char/tt_a_chr_' + torsotype + '_torso_victory-dance.bam',
         'squirt': 'phase_5/models/char/tt_a_chr_' + torsotype + '_torso_water-gun.bam',
         'zend': 'phase_3.5/models/char/tt_a_chr_' + torsotype + '_torso_jump-zend.bam',
         'tele': 'phase_3.5/models/char/tt_a_chr_' + torsotype + '_torso_teleport.bam',
         'book': 'phase_3.5/models/char/tt_a_chr_' + torsotype + '_torso_book.bam',
         'leap': 'phase_3.5/models/char/tt_a_chr_' + torsotype + '_torso_leap_zhang.bam',
         'jump': 'phase_3.5/models/char/tt_a_chr_' + torsotype + '_torso_jump-zhang.bam',
         'happy': 'phase_3.5/models/char/tt_a_chr_' + torsotype + '_torso_jump.bam',
         'shrug': 'phase_3.5/models/char/tt_a_chr_' + torsotype + '_torso_shrug.bam',
         'hdance': 'phase_5/models/char/tt_a_chr_' + torsotype + '_torso_happy-dance.bam',
         'wave': 'phase_3.5/models/char/tt_a_chr_' + torsotype + '_torso_wave.bam',
         'scemcee': 'phase_4/models/char/tt_a_chr_dgm_shorts_torso_scientistEmcee.bam',
         'scwork': 'phase_4/models/char/tt_a_chr_' + torsotype + '_torso_scientistWork.bam',
         'scgame': 'phase_4/models/char/tt_a_chr_' + torsotype + '_torso_scientistGame.bam',
         'scjealous': 'phase_4/models/char/tt_a_chr_' + torsotype + '_torso_scientistJealous.bam',
         'swim': 'phase_4/models/char/tt_a_chr_' + torsotype + '_torso_swim.bam',
         'toss': 'phase_5/models/char/tt_a_chr_' + torsotype + '_torso_toss.bam',
         'cringe': 'phase_3.5/models/char/tt_a_chr_' + torsotype + '_torso_cringe.bam',
         'conked': 'phase_3.5/models/char/tt_a_chr_' + torsotype + '_torso_conked.bam'}, 'torso')

    def generateHead(self, pat = 0):
        gender = self.getGender()
        head = self.getAnimal()
        headtype = self.getHead()
        ToonHead.generateHead(self, gender, head, headtype)

    def setToonColor(self):
        self.setHeadColor()
        self.setTorsoColor()
        self.setLegColor()

    def setLegColor(self):
        legcolor = self.getLegColor()
        self.findAllMatches('**/legs').setColor(legcolor)
        self.findAllMatches('**/feet').setColor(legcolor)

    def setTorsoColor(self):
        torsocolor = self.getTorsoColor()
        self.findAllMatches('**/arms').setColor(torsocolor)
        self.findAllMatches('**/neck').setColor(torsocolor)
        self.findAllMatches('**/hands').setColor(1, 1, 1, 1)

    def enterOff(self, ts = 0, callback = None, extraArgs = []):
        self.currentAnim = None
        return

    def exitOff(self):
        pass

    def enterShrug(self, ts = 0, callback = None, extraArgs = []):
        self.play('shrug')

    def exitShrug(self):
        self.exitGeneral()

    def enterHDance(self, ts = 0, callback = None, extraArgs = []):
        self.play('hdance')

    def exitHDance(self):
        self.exitGeneral()

    def enterScientistWork(self, ts = 0, callback = None, extraArgs = []):
        self.loop('scwork')

    def exitScientistWork(self):
        self.exitGeneral()

    def enterScientistEmcee(self, ts = 0, callback = None, extraArgs = []):
        self.loop('scemcee')

    def exitScientistEmcee(self):
        self.exitGeneral()

    def enterScientistGame(self, ts = 0, callback = None, extraArgs = []):
        self.loop('scgame')

    def exitScientistGame(self):
        self.exitGeneral()

    def enterScientistJealous(self, ts = 0, callback = None, extraArgs = []):
        self.loop('scjealous')

    def exitScientistJealous(self):
        self.exitGeneral()

    def enterWave(self, ts = 0, callback = None, extraArgs = []):
        self.play('wave')

    def exitWave(self):
        self.exitGeneral()

    def enterLaugh(self, ts = 0, callback = None, extraArgs = []):
        self.setPlayRate(5.0, 'neutral')
        self.loop('neutral')

    def exitLaugh(self):
        self.setPlayRate(1.0, 'neutral')
        self.stop()

    def enterNeutral(self, ts = 0, callback = None, extraArgs = []):
        if self.pies.getPieType() == 3 and self.pies.tnt_state == 'ready':
            self.loop('neutral', partName='legs')
            if self.animal == 'dog':
                self.loop('neutral', partName='head')
            self.holdTNTAnim()
        else:
            self.loop('neutral')

    def exitNeutral(self):
        self.exitGeneral()

    def exitGeneral(self):
        self.stop()

    def enterRun(self, ts = 0, callback = None, extraArgs = []):
        if self.pies.getPieType() == 3 and self.pies.tnt_state == 'ready':
            self.loop('run', partName='legs')
            if self.animal == 'dog':
                self.loop('run', partName='head')
            self.holdTNTAnim()
        else:
            self.loop('run')

    def exitRun(self):
        self.exitGeneral()

    def enterWalk(self, ts = 0, callback = None, extraArgs = []):
        if self.pies.getPieType() == 3 and self.pies.tnt_state == 'ready':
            self.loop('walk', partName='legs')
            if self.animal == 'dog':
                self.loop('walk', partName='head')
            self.holdTNTAnim()
        else:
            self.loop('walk')

    def exitWalk(self):
        self.exitGeneral()

    def enterOpenBook(self, ts = 0, callback = None, extraArgs = []):
        self.book1 = Actor('phase_3.5/models/props/book-mod.bam', {'chan': 'phase_3.5/models/props/book-chan.bam'})
        self.book1.reparentTo(self.getPart('torso').find('**/def_joint_right_hold'))
        self.track = ActorInterval(self, 'book', startFrame=CIGlobals.OpenBookFromFrame, endFrame=CIGlobals.OpenBookToFrame, name=self.uniqueName('enterOpenBook'))
        self.track.setDoneEvent(self.track.getName())
        self.acceptOnce(self.track.getDoneEvent(), self.__doCallback, [callback, extraArgs])
        self.track.start(ts)
        self.book1.play('chan', fromFrame=CIGlobals.OpenBookFromFrame, toFrame=CIGlobals.OpenBookToFrame)

    def exitOpenBook(self):
        if self.track:
            self.ignore(self.track.getDoneEvent())
            self.track.finish()
            self.track = None
        if self.book1:
            self.book1.cleanup()
            self.book1 = None
        return

    def enterReadBook(self, ts = 0, callback = None, extraArgs = []):
        self.book2 = Actor('phase_3.5/models/props/book-mod.bam', {'chan': 'phase_3.5/models/props/book-chan.bam'})
        self.book2.reparentTo(self.getPart('torso').find('**/def_joint_right_hold'))
        self.pingpong('book', fromFrame=CIGlobals.ReadBookFromFrame, toFrame=CIGlobals.ReadBookToFrame)
        self.book2.pingpong('chan', fromFrame=CIGlobals.ReadBookFromFrame, toFrame=CIGlobals.ReadBookToFrame)

    def exitReadBook(self):
        if self.book2:
            self.book2.cleanup()
            self.book2 = None
        return

    def enterCloseBook(self, ts = 0, callback = None, extraArgs = []):
        self.book3 = Actor('phase_3.5/models/props/book-mod.bam', {'chan': 'phase_3.5/models/props/book-chan.bam'})
        self.book3.reparentTo(self.getPart('torso').find('**/def_joint_right_hold'))
        self.track = ActorInterval(self, 'book', startFrame=CIGlobals.CloseBookFromFrame, endFrame=CIGlobals.CloseBookToFrame, name=self.uniqueName('enterCloseBook'))
        self.track.setDoneEvent(self.track.getName())
        self.acceptOnce(self.track.getDoneEvent(), self.__doCallback, [callback, extraArgs])
        self.track.start(ts)
        self.book3.play('chan', fromFrame=CIGlobals.CloseBookFromFrame, toFrame=CIGlobals.CloseBookToFrame)

    def exitCloseBook(self):
        if self.track:
            self.ignore(self.track.getDoneEvent())
            self.track.finish()
            self.track = None
        if self.book3:
            self.book3.cleanup()
            self.book3 = None
        return

    def enterTeleportOut(self, ts = 0, callback = None, extraArgs = []):
        self.notify.info(str(self.doId) + '-' + str(self.zoneId) + ': enterTeleportOut')
        self.portal1 = Actor('phase_3.5/models/props/portal-mod.bam', {'chan': 'phase_3.5/models/props/portal-chan.bam'})
        self.portal1.play('chan')
        self.portal1.reparentTo(self.getPart('legs').find('**/def_joint_right_hold'))
        self.play('tele')
        if hasattr(self, 'uniqueName'):
            name = self.uniqueName('enterTeleportOut')
        else:
            name = 'enterTeleportOut'
        self.track = Sequence(Wait(0.4), Func(self.teleportOutSfx), Wait(1.3), Func(self.throwPortal), Wait(3.4), name=name)
        self.track.delayDelete = DelayDelete.DelayDelete(self, name)
        self.track.setDoneEvent(self.track.getName())
        self.acceptOnce(self.track.getName(), self.teleportOutDone, [callback, extraArgs])
        self.track.start(ts)

    def doPortalBins(self, portal):
        portal.setBin('shadow', 0)
        portal.setDepthWrite(0)
        portal.setDepthTest(0)

    def teleportOutDone(self, callback, requestStatus):
        self.notify.info(str(self.doId) + '-' + str(self.zoneId) + ': teleportOutDone')
        self.__doCallback(callback, requestStatus)
        self.exitTeleportOut()

    def teleportOutSfx(self):
        self.outSfx = self.audio3d.loadSfx('phase_3.5/audio/sfx/AV_teleport.mp3')
        self.audio3d.attachSoundToObject(self.outSfx, self.portal1)
        self.outSfx.play()

    def throwPortal(self):
        self.doPortalBins(self.portal1)
        self.portal1.reparentTo(self.getPart('legs').find('**/joint_nameTag'))
        self.portal1.setScale(CIGlobals.PortalScale)
        self.portal1.setY(6.5)
        self.portal1.setH(180)

    def exitTeleportOut(self):
        self.notify.info(str(self.doId) + '-' + str(self.zoneId) + ': exitTeleportOut')
        if self.track != None:
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        if self.portal1:
            self.portal1.cleanup()
            self.portal1 = None
        return

    def getTeleportInTrack(self, portal):
        self.doPortalBins(portal)
        holeTrack = Sequence()
        holeTrack.append(Func(portal.reparentTo, self))
        pos = Point3(0, -2.4, 0)
        holeTrack.append(Func(portal.setPos, pos))
        holeTrack.append(ActorInterval(portal, 'chan', startTime=3.4, endTime=3.1))
        holeTrack.append(Wait(0.6))
        holeTrack.append(ActorInterval(portal, 'chan', startTime=3.1, endTime=3.4))

        def restorePortal(portal):
            portal.setPos(0, 0, 0)
            portal.detachNode()
            portal.clearBin()
            portal.clearDepthTest()
            portal.clearDepthWrite()

        holeTrack.append(Func(restorePortal, portal))
        toonTrack = Sequence(Wait(0.3), Func(self.getGeomNode().show), Func(self.tag.show), ActorInterval(self, 'happy', startTime=0.45))
        if hasattr(self, 'uniqueName'):
            trackName = self.uniqueName('teleportIn')
        else:
            trackName = 'teleportIn'
        return Parallel(toonTrack, holeTrack, name=trackName)

    def enterTeleportIn(self, ts = 0, callback = None, extraArgs = []):
        self.portal2 = Actor('phase_3.5/models/props/portal-mod.bam', {'chan': 'phase_3.5/models/props/portal-chan.bam'})
        self.show()
        self.getGeomNode().hide()
        self.tag.hide()
        self.track = self.getTeleportInTrack(self.portal2)
        self.track.setDoneEvent(self.track.getName())
        self.acceptOnce(self.track.getName(), self.teleportInDone, [callback, extraArgs])
        self.track.delayDelete = DelayDelete.DelayDelete(self, self.track.getName())
        self.track.start(ts)

    def teleportInDone(self, callback, extraArgs):
        self.__doCallback(callback, extraArgs)
        self.exitTeleportIn()

    def exitTeleportIn(self):
        if self.track != None:
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        if self.portal2:
            self.portal2.cleanup()
            self.portal2 = None
        if self.getGeomNode():
            self.getGeomNode().show()
        if self.tag:
            self.tag.show()
        return

    def enterFallFWD(self, ts = 0, callback = None, extraArgs = []):
        self.play('fallf')
        Sequence(Wait(0.5), Func(self.fallSfx.play)).start()

    def exitFallFWD(self):
        self.exitGeneral()

    def enterFallBCK(self, ts = 0, callback = None, extraArgs = []):
        self.play('fallb')
        Sequence(Wait(0.5), Func(self.fallSfx.play)).start()

    def exitFallBCK(self):
        self.exitGeneral()

    def enterHappy(self, ts = 0, callback = None, extraArgs = []):
        self.play('happy')

    def exitHappy(self):
        self.exitGeneral()

    def enterSwim(self, ts = 0, callback = None, extraArgs = []):
        self.loop('swim')
        self.getGeomNode().setP(-89.0)
        self.getGeomNode().setZ(4.0)
        self.getNameTag().setPos(0, -2, 5.0)

    def exitSwim(self):
        self.exitGeneral()
        self.getGeomNode().setP(0.0)
        self.getGeomNode().setZ(0.0)
        self.getNameTag().setPos(0, 0, self.getHeight() + 0.3)

    def enterDied(self, ts = 0, callback = None, extraArgs = []):
        self.isdying = True
        self.play('lose')
        self.track = Sequence(Wait(2.2), Func(self.dieSfx), Wait(2.8), self.getGeomNode().scaleInterval(2, Point3(0.01), startScale=self.getGeomNode().getScale()), Func(self.delToon), name=self.uniqueName('enterDied'))
        self.track.setDoneEvent(self.track.getName())
        self.acceptOnce(self.track.getDoneEvent(), self.diedDone, [callback, extraArgs])
        self.track.delayDelete = DelayDelete.DelayDelete(self, 'enterTeleportOut')
        self.track.start(ts)

    def diedDone(self, callback, extraArgs):
        self.__doCallback(callback, extraArgs)
        self.exitDied()

    def __doCallback(self, callback, extraArgs):
        if callback:
            if extraArgs:
                callback(*extraArgs)
            else:
                callback()

    def dieSfx(self):
        self.Losesfx = self.audio3d.loadSfx('phase_5/audio/sfx/ENC_Lose.mp3')
        self.audio3d.attachSoundToObject(self.Losesfx, self)
        self.Losesfx.play()

    def delToon(self):
        self.isdead = True

    def exitDied(self):
        if self.track != None:
            self.ignore(self.track.getDoneEvent())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        self.rescaleToon()
        return

    def enterJump(self, ts = 0, callback = None, extraArgs = []):
        self.loop('jump')

    def exitJump(self):
        self.exitGeneral()

    def enterLeap(self, ts = 0, callback = None, extraArgs = []):
        self.loop('leap')

    def exitLeap(self):
        self.exitGeneral()

    def enterCringe(self, ts = 0, callback = None, extraArgs = []):
        self.play('cringe')

    def exitCringe(self):
        self.exitGeneral()

    def enterConked(self, ts = 0, callback = None, extraArgs = []):
        self.play('conked')

    def exitConked(self):
        self.exitGeneral()