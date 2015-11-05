# Embedded file name: lib.coginvasion.toon.ToonHead
"""

  Filename: ToonHead.py
  Created by: blach (??July14)
  Remade: (28Oct14)
  
"""
from panda3d.core import *
from lib.coginvasion.globals import CIGlobals
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
import random

class ToonHead(Actor.Actor):
    EyesOpen = loader.loadTexture('phase_3/maps/eyes.jpg', 'phase_3/maps/eyes_a.rgb')
    EyesOpen.setMinfilter(Texture.FTLinear)
    EyesOpen.setMagfilter(Texture.FTLinear)
    EyesClosed = loader.loadTexture('phase_3/maps/eyesClosed.jpg', 'phase_3/maps/eyesClosed_a.rgb')
    EyesClosed.setMinfilter(Texture.FTLinear)
    EyesClosed.setMagfilter(Texture.FTLinear)
    EyesOpenSad = loader.loadTexture('phase_3/maps/eyesSad.jpg', 'phase_3/maps/eyesSad_a.rgb')
    EyesOpenSad.setMinfilter(Texture.FTLinear)
    EyesOpenSad.setMagfilter(Texture.FTLinear)
    EyesClosedSad = loader.loadTexture('phase_3/maps/eyesSadClosed.jpg', 'phase_3/maps/eyesSadClosed_a.rgb')
    EyesClosedSad.setMinfilter(Texture.FTLinear)
    EyesClosedSad.setMagfilter(Texture.FTLinear)

    def __init__(self, cr):
        try:
            self.ToonHead_initialized
            return
        except:
            self.ToonHead_initialized = 1

        Actor.Actor.__init__(self)
        self.cr = cr
        self.head = None
        self.headtype = None
        self.gender = None
        self.__eyelashOpened = None
        self.__eyelashClosed = None
        self.pupils = []
        return

    def generateHead(self, gender, head, headtype):

        def stashMuzzles(length, stashNeutral = 0):
            if stashNeutral:
                if length == 'short':
                    self.findAllMatches('**/muzzle-long-neutral').hide()
                elif length == 'long':
                    self.findAllMatches('**/muzzle-short-neutral').hide()
            elif length == 'short':
                if self.find('**/muzzle-long-neutral').isHidden():
                    self.find('**/muzzle-long-neutral').show()
            elif length == 'long':
                if self.find('**/muzzle-short-neutral').isHidden():
                    self.find('**/muzzle-short-neutral').show()
            self.findAllMatches('**/muzzle-' + length + '-s*').hide()
            self.findAllMatches('**/muzzle-' + length + '-laugh').hide()
            self.findAllMatches('**/muzzle-' + length + '-angry').hide()

        def stashParts(length):
            for part in self.findAllMatches('**/*' + length + '*'):
                part.hide()

        self.gender = gender
        self.animal = head
        self.head = headtype
        _modelDetail = str(CIGlobals.getModelDetail(CIGlobals.Toon))
        if head != 'dog':
            self.loadModel('phase_3/models/char/%s-heads-%s.bam' % (head, _modelDetail), 'head')
        else:
            self.loadModel('phase_3/models/char/tt_a_chr_%s_head_%s.bam' % (headtype, _modelDetail), 'head')
            self.loadAnims({'neutral': 'phase_3/models/char/tt_a_chr_' + headtype + '_head_neutral.bam',
             'run': 'phase_3/models/char/tt_a_chr_' + headtype + '_head_run.bam',
             'walk': 'phase_3.5/models/char/tt_a_chr_' + headtype + '_head_walk.bam',
             'pie': 'phase_3.5/models/char/tt_a_chr_' + headtype + '_head_pie-throw.bam',
             'fallb': 'phase_4/models/char/tt_a_chr_' + headtype + '_head_slip-backward.bam',
             'fallf': 'phase_4/models/char/tt_a_chr_' + headtype + '_head_slip-forward.bam',
             'lose': 'phase_5/models/char/tt_a_chr_' + headtype + '_head_lose.bam',
             'win': 'phase_3.5/models/char/tt_a_chr_' + headtype + '_head_victory-dance.bam',
             'squirt': 'phase_5/models/char/tt_a_chr_' + headtype + '_head_water-gun.bam',
             'zend': 'phase_3.5/models/char/tt_a_chr_' + headtype + '_head_jump-zend.bam',
             'tele': 'phase_3.5/models/char/tt_a_chr_' + headtype + '_head_teleport.bam',
             'book': 'phase_3.5/models/char/tt_a_chr_' + headtype + '_head_book.bam',
             'leap': 'phase_3.5/models/char/tt_a_chr_' + headtype + '_head_leap_zhang.bam',
             'jump': 'phase_3.5/models/char/tt_a_chr_' + headtype + '_head_jump-zhang.bam',
             'happy': 'phase_3.5/models/char/tt_a_chr_' + headtype + '_head_jump.bam',
             'shrug': 'phase_3.5/models/char/tt_a_chr_' + headtype + '_head_shrug.bam',
             'hdance': 'phase_5/models/char/tt_a_chr_' + headtype + '_head_happy-dance.bam',
             'wave': 'phase_3.5/models/char/tt_a_chr_' + headtype + '_head_wave.bam',
             'swim': 'phase_4/models/char/tt_a_chr_' + headtype + '_head_swim.bam',
             'toss': 'phase_5/models/char/tt_a_chr_' + headtype + '_head_toss.bam',
             'cringe': 'phase_3.5/models/char/tt_a_chr_' + headtype + '_head_cringe.bam',
             'conked': 'phase_3.5/models/char/tt_a_chr_' + headtype + '_head_conked.bam'}, 'head')
            _pupilL = self.findAllMatches('**/def_left_pupil')
            _pupilR = self.findAllMatches('**/def_right_pupil')
        if headtype == '1':
            stashParts('long')
            stashMuzzles('long', stashNeutral=0)
            stashMuzzles('short', stashNeutral=1)
            _pupilL = self.findAllMatches('**/joint_pupilL_short')
            _pupilR = self.findAllMatches('**/joint_pupilR_short')
        elif headtype == '2':
            if head == 'mouse':
                stashParts('short')
                stashMuzzles('short', stashNeutral=1)
                stashMuzzles('long', stashNeutral=0)
                _pupilL = self.findAllMatches('**/joint_pupilL_long')
                _pupilR = self.findAllMatches('**/joint_pupilR_long')
            else:
                stashParts('long')
                stashMuzzles('short', stashNeutral=0)
                stashMuzzles('long', stashNeutral=1)
                _pupilL = self.findAllMatches('**/joint_pupilL_short')
                _pupilR = self.findAllMatches('**/joint_pupilR_short')
            if head == 'rabbit':
                self.findAllMatches('**/head-long').show()
                self.findAllMatches('**/head-front-long').show()
                self.findAllMatches('**/head-front-short').hide()
                self.findAllMatches('**/head-short').hide()
        elif headtype == '3':
            stashParts('short')
            stashMuzzles('long', stashNeutral=0)
            stashMuzzles('short', stashNeutral=1)
            _pupilL = self.findAllMatches('**/joint_pupilL_long')
            _pupilR = self.findAllMatches('**/joint_pupilR_long')
            if head == 'rabbit':
                self.findAllMatches('**/head-long').hide()
                self.findAllMatches('**/head-front-long').hide()
                self.findAllMatches('**/head-front-short').show()
                self.findAllMatches('**/head-short').show()
        elif headtype == '4':
            stashParts('short')
            stashMuzzles('short', stashNeutral=0)
            stashMuzzles('long', stashNeutral=1)
            _pupilL = self.findAllMatches('**/joint_pupilL_long')
            _pupilR = self.findAllMatches('**/joint_pupilR_long')
        self.pupils.append(_pupilL)
        self.pupils.append(_pupilR)
        if self.gender == 'girl':
            self.setupEyelashes()

    def guiFix(self):
        self.drawInFront('eyes*', 'head-front*', -2)
        if not self.find('joint_pupil*').isEmpty():
            self.drawInFront('joint_pupil*', 'eyes*', -1)
        else:
            self.drawInFront('def_*_pupil', 'eyes*', -1)

    def setupEyelashes(self):
        head = self.getPart('head')
        lashes = loader.loadModel('phase_3/models/char/%s-lashes.bam' % self.animal)
        openString = 'open-short'
        closedString = 'closed-short'
        if self.head == 'mouse':
            if self.head == '1':
                openString = 'open-short'
                closedString = 'closed-short'
            elif self.head == '2':
                openString = 'open-long'
                closedString = 'closed-long'
        elif self.head == '1':
            openString = 'open-short'
            closedString = 'closed-short'
        elif self.head == '2':
            openString = 'open-short'
            closedString = 'closed-short'
        elif self.head == '3':
            openString = 'open-long'
            closedString = 'closed-long'
        elif self.head == '4':
            openString = 'open-long'
            closedString = 'closed-long'
        self.__eyelashOpened = lashes.find('**/' + openString).copyTo(head)
        self.__eyelashClosed = lashes.find('**/' + closedString).copyTo(head)
        self.__eyelashClosed.hide()

    def startBlink(self):
        randomStart = random.uniform(0.5, 7)
        taskMgr.doMethodLater(randomStart, self.blinkTask, self.cr.uniqueName('blinkTask'))

    def stopBlink(self):
        taskMgr.remove(self.cr.uniqueName('blinkTask'))
        taskMgr.remove(self.cr.uniqueName('doBlink'))
        taskMgr.remove(self.cr.uniqueName('openEyes'))

    def blinkTask(self, task):
        taskMgr.add(self.doBlink, self.cr.uniqueName('doBlink'))
        delay = random.uniform(0.5, 7)
        task.delayTime = delay
        return task.again

    def doBlink(self, task):
        self.closeEyes()
        taskMgr.doMethodLater(0.2, self.doOpenEyes, self.cr.uniqueName('openEyes'))
        return task.done

    def doOpenEyes(self, task):
        self.openEyes()
        return task.done

    def closeEyes(self):
        if self.gender == 'girl':
            self.__eyelashOpened.hide()
            self.__eyelashClosed.show()
        for pupil in self.pupils:
            pupil.hide()

        if hasattr(self, 'getHealth'):
            if self.getHealth() > 1:
                try:
                    self.findAllMatches('**/eyes*').setTexture(self.EyesClosed, 1)
                except:
                    pass

            else:
                try:
                    self.findAllMatches('**/eyes*').setTexture(self.EyesClosedSad, 1)
                except:
                    pass

        else:
            try:
                self.findAllMatches('**/eyes*').setTexture(self.EyesClosed, 1)
            except:
                pass

    def openEyes(self):
        if self.gender == 'girl':
            self.__eyelashOpened.show()
            self.__eyelashClosed.hide()
        for pupil in self.pupils:
            pupil.show()

        if hasattr(self, 'getHealth'):
            if self.getHealth() > 1:
                try:
                    self.findAllMatches('**/eyes*').setTexture(self.EyesOpen, 1)
                except:
                    pass

            else:
                try:
                    self.findAllMatches('**/eyes*').setTexture(self.EyesOpenSad, 1)
                except:
                    pass

        else:
            try:
                self.findAllMatches('**/eyes*').setTexture(self.EyesOpen, 1)
            except:
                pass

    def startLookAround(self):
        delay = random.randint(3, 15)
        taskMgr.doMethodLater(delay, self.lookAroundTask, self.cr.uniqueName('lookAroundTask'))

    def stopLookAround(self):
        taskMgr.remove(self.cr.uniqueName('lookAroundTask'))
        taskMgr.remove(self.cr.uniqueName('doLookAround'))

    def lookAroundTask(self, task):
        taskMgr.add(self.doLookAround, self.cr.uniqueName('doLookAround'))
        delay = random.uniform(3, 10)
        task.delayTime = delay
        return task.again

    def doLookAround(self, task):
        hpr = self.findSomethingToLookAt()
        h, p, r = hpr
        if not hpr:
            return task.done
        messenger.send('gotLookSpot', [hpr])
        self.lerpLookAt(self.getPart('head'), hpr)
        return task.done

    def findSomethingToLookAt(self):
        toons = []
        if hasattr(base, 'localAvatar'):
            for key in self.cr.doId2do.keys():
                val = self.cr.doId2do[key]
                if not val.doId == base.localAvatar.doId:
                    if val.__class__.__name__ in ('DistributedToon', 'DistributedSuit'):
                        if base.camNode.isInView(val.getPos(camera)):
                            if val.__class__.__name__ == 'DistributedToon':
                                toons.append(val.getPart('head'))
                            elif val.__class__.__name__ == 'DistributedSuit':
                                toons.append(val.headModel)

        decision = random.randint(0, 3)
        if toons == [] or decision == 3:
            return self.randomLookSpot()
        else:
            startH = self.getPart('head').getH()
            startP = self.getPart('head').getP()
            startR = self.getPart('head').getR()
            toon = random.randint(0, len(toons) - 1)
            self.getPart('head').lookAt(toons[toon], 0, 0, -0.75)
            endH = self.getPart('head').getH()
            endP = self.getPart('head').getP()
            endR = self.getPart('head').getR()
            self.getPart('head').setHpr(startH, startP, startR)
            return tuple((endH, endP, endR))

    def randomLookSpot(self):
        spots = [(0, 0, 0),
         (35, 0, 0),
         (-35, 0, 0),
         (35, -20, 0),
         (-35, -20, 0),
         (35, 20, 0),
         (-35, 20, 0),
         (0, 20, 0),
         (0, -20, 0)]
        spot = random.randint(0, len(spots) - 1)
        h, p, r = spots[spot]
        return tuple((h, p, r))

    def lerpLookAt(self, head, hpr, time = 1.0):
        self.lookAtTrack = Parallel(Sequence(LerpHprInterval(head, time, hpr, blendType='easeInOut')))
        self.lookAtTrack.start()
        return 1

    def setHeadColor(self, color = None):
        if color == None:
            color = self.headcolor
        self.findAllMatches('**/head*').setColor(color)
        if self.animal == 'rabbit' or self.animal == 'cat' or self.animal == 'bear' or self.animal == 'pig' or self.animal == 'mouse':
            self.findAllMatches('**/ears*').setColor(color)
        return

    def delete(self):
        try:
            self.ToonHead_deleted
        except:
            self.ToonHead_deleted = 1
            self.stopBlink()
            self.stopLookAround()
            Actor.Actor.cleanup(self)
            Actor.Actor.delete(self)
            self.gender = None
            self.head = None
            self.headtype = None

        return