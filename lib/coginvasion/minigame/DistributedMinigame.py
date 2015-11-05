# Embedded file name: lib.coginvasion.minigame.DistributedMinigame
"""

  Filename: DistributedMinigame.py
  Created by: blach (06Oct14)

"""
from panda3d.core import *
from lib.coginvasion.globals import CIGlobals
from pandac.PandaModules import *
from direct.distributed import DistributedObject
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.Transitions import *
from lib.coginvasion.gui.Dialog import *
from direct.fsm.State import State
from direct.fsm.ClassicFSM import ClassicFSM
import Timer
from lib.coginvasion.hood import ZoneUtil
from HeadPanels import HeadPanels
from FinalScoreGUI import FinalScoreGUI
import random
transitions = Transitions(loader)

class DistributedMinigame(DistributedObject.DistributedObject, Timer.Timer):

    def __init__(self, cr):
        try:
            self.DistributedMinigame_initialized
            return
        except:
            self.DistributedMinigame_initialized = 1

        DistributedObject.DistributedObject.__init__(self, cr)
        Timer.Timer.__init__(self)
        self.headPanels = HeadPanels()
        self.finalScoreUI = FinalScoreGUI()
        self.fsm = ClassicFSM('DistributedMinigame', [State('start', self.enterStart, self.exitStart, ['waitForOthers']),
         State('waitForOthers', self.enterWaitForOthers, self.exitWaitForOthers, ['play']),
         State('play', self.enterPlay, self.exitPlay, ['gameOver']),
         State('gameOver', self.enterGameOver, self.exitGameOver, ['off']),
         State('off', self.enterOff, self.exitOff)], 'off', 'off')
        self.fsm.enterInitialState()
        self.cr = cr
        self.localAv = base.localAvatar
        self.localAvId = self.localAv.doId
        self.musicPath = 'phase_4/audio/bgm/trolley_song.mid'
        self.winSfx = base.loadSfx('phase_4/audio/sfx/MG_win.mp3')
        self.loseSfx = base.loadSfx('phase_4/audio/sfx/MG_lose.mp3')
        self.prizeHigh = base.loadSfx('phase_6/audio/sfx/KART_Applause_1.mp3')
        self.prizeLow = base.loadSfx('phase_6/audio/sfx/KART_Applause_4.mp3')
        self.music = None
        self.description = ''
        self.descDialog = None
        self.winnerPrize = 0
        self.loserPrize = 0
        self.winnerMsg = 'Winner!\nYou have earned: %s'
        self.loserMsg = 'Loser!\nYou have earned: %s'
        self.allWinnerMsgs = ['Nice try!\nYou have earned: %s',
         'Good job!\nYou have earned: %s',
         'Way to go!\nYou have earned: %s',
         'Awesome!\nYou have earned: %s']
        self.timer = None
        self.timeLbl = None
        return

    def enterFinalScores(self):
        self.finalScoreUI.load()
        self.finalScoreUI.showFinalScores()

    def exitFinalScores(self):
        self.finalScoreUI.hideFinalScores()
        self.finalScoreUI.unload()

    def finalScores(self, avIdList, scoreList):
        self.finalScoreUI.handleFinalScores(avIdList, scoreList)

    def generateHeadPanel(self, gender, head, headtype, color, doId, name):
        self.headPanels.generate(gender, head, headtype, color, doId, name)

    def updateHeadPanelValue(self, doId, direction):
        self.headPanels.updateValue(doId, direction)

    def setTimerTime(self, time):
        self.setTime(time)

    def createTimer(self):
        Timer.Timer.load(self)

    def deleteTimer(self):
        Timer.Timer.unload(self)

    def setDescription(self, desc):
        self.description = desc

    def getDescription(self):
        return self.description

    def enterStart(self):
        self.descDialog = GlobalDialog(style=3, message=self.getDescription(), doneEvent='gameDescAck')
        self.acceptOnce('gameDescAck', self.handleDescAck)

    def handleDescAck(self):
        self.d_ready()
        self.fsm.request('waitForOthers')

    def exitStart(self):
        self.ignore('gameDescAck')
        self.descDialog.cleanup()
        del self.descDialog

    def enterWaitForOthers(self):
        self.waitLbl = DirectLabel(text='Waiting for other players...', relief=None, text_fg=(1, 1, 1, 1), text_scale=0.08, text_shadow=(0, 0, 0, 1))
        return

    def exitWaitForOthers(self):
        self.waitLbl.destroy()
        del self.waitLbl

    def setLoserPrize(self, prize):
        self.loserPrize = prize

    def setWinnerPrize(self, prize):
        self.winnerPrize = prize

    def getLoserPrize(self):
        return self.loserPrize

    def getWinnerPrize(self):
        return self.winnerPrize

    def winner(self):
        self.winSfx.play()
        self.localAv.b_setAnimState('happy')
        Sequence(Wait(3.5), Func(self.displayGameOver, 'winner')).start()

    def showPrize(self, amt):
        self.winSfx.play()
        self.localAv.b_setAnimState('happy')
        Sequence(Wait(3.5), Func(self.displayGameOver, 'showPrize', amt)).start()

    def loser(self):
        self.loseSfx.play()
        self.localAv.b_setAnimState('neutral')
        Sequence(Wait(3.5), Func(self.displayGameOver, 'loser')).start()

    def displayGameOver(self, scenario, amt = None):
        if scenario == 'winner':
            msg = self.winnerMsg % self.winnerPrize
            self.prizeHigh.play()
        elif scenario == 'loser':
            msg = self.loserMsg % self.loserPrize
            self.prizeLow.play()
        elif scenario == 'showPrize':
            msg = random.choice(self.allWinnerMsgs) % amt
            self.prizeHigh.play()
        self.gameOverDialog = GlobalDialog(message=msg, style=3, doneEvent='gameOverAck')
        self.acceptOnce('gameOverAck', self.__handleGameOverAck)
        self.gameOverDialog.show()

    def deleteGameOverDialog(self):
        self.ignore('gameOverAck')
        if hasattr(self, 'gameOverDialog'):
            self.gameOverDialog.cleanup()
            del self.gameOverDialog

    def __handleGameOverAck(self):
        self.fsm.requestFinalState()
        Sequence(Func(base.transitions.irisOut, 1.0), Wait(1.2), Func(self.d_leaving), Func(self.headBackToMinigameArea)).start()

    def headBackToMinigameArea(self):
        whereName = ZoneUtil.getWhereName(CIGlobals.MinigameAreaId)
        loaderName = ZoneUtil.getLoaderName(CIGlobals.MinigameAreaId)
        requestStatus = {'zoneId': CIGlobals.MinigameAreaId,
         'hoodId': CIGlobals.MinigameArea,
         'where': whereName,
         'how': 'teleportIn',
         'avId': base.localAvatar.doId,
         'shardId': None,
         'loader': loaderName}
        self.cr.playGame.hood.fsm.request('quietZone', [requestStatus])
        return

    def abort(self):
        self.headBackToMinigameArea()

    def load(self):
        self.fsm.request('start')
        base.transitions.irisIn()

    def d_leaving(self):
        """ Tell the AI that we are leaving. """
        self.sendUpdate('leaving', [])

    def allPlayersReady(self):
        self.fsm.request('play')

    def enterPlay(self):
        self.playMinigameMusic()

    def exitPlay(self):
        self.stopMinigameMusic()

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterGameOver(self, winner, winnerDoId, allPrize):
        if winner:
            if self.localAvId in winnerDoId:
                self.winner()
            else:
                self.loser()
        else:
            self.showPrize(allPrize)

    def exitGameOver(self):
        self.deleteGameOverDialog()

    def gameOver(self, winner = 0, winnerDoId = [], allPrize = 0):
        self.fsm.request('gameOver', [winner, winnerDoId, allPrize])

    def setMinigameMusic(self, path):
        self.musicPath = path

    def getMinigameMusic(self):
        return self.musicPath

    def playMinigameMusic(self):
        self.stopMinigameMusic()
        self.music = base.loadMusic(self.musicPath)
        self.music.setLoop(True)
        self.music.setVolume(0.7)
        self.music.play()

    def stopMinigameMusic(self):
        if self.music:
            self.music.stop()
            self.music = None
        return

    def d_ready(self):
        self.sendUpdate('ready', [])

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        base.localAvatar.setPosHpr(0, 0, 0, 0, 0, 0)
        self.fsm.requestFinalState()
        del self.fsm
        self.winSfx = None
        self.loseSfx = None
        self.prizeHigh = None
        self.prizeLow = None
        self.headPanels.delete()
        self.headPanels = None
        self.finalScoreUI.unload()
        self.finalScoreUI = None
        return