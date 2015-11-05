# Embedded file name: lib.coginvasion.book.ShtickerBook
"""
  
  Filename: ShtickerBook.py
  Created by: blach (20June14)
  
"""
from lib.coginvasion.globals import CIGlobals
from panda3d.core import *
from direct.gui.DirectGui import *
from lib.coginvasion.manager.SettingsManager import SettingsManager
from direct.fsm.StateData import StateData
from direct.fsm.State import State
from direct.fsm.ClassicFSM import ClassicFSM
from lib.coginvasion.hood import ZoneUtil
import types
from OptionPage import OptionPage
from AdminPage import AdminPage
qt_btn = loader.loadModel('phase_3/models/gui/quit_button.bam')

class ShtickerBook(StateData):

    def __init__(self, parentFSM, doneEvent):
        self.parentFSM = parentFSM
        StateData.__init__(self, doneEvent)
        self.fsm = ClassicFSM('ShtickerBook', [State('off', self.enterOff, self.exitOff),
         State('optionPage', self.enterOptionPage, self.exitOptionPage, ['zonePage', 'off']),
         State('zonePage', self.enterZonePage, self.exitZonePage, ['releaseNotesPage', 'optionPage', 'off']),
         State('releaseNotesPage', self.enterReleaseNotesPage, self.exitReleaseNotesPage, ['zonePage', 'off']),
         State('adminPage', self.enterAdminPage, self.exitAdminPage, ['releaseNotesPage', 'off'])], 'off', 'off')
        if base.localAvatar.getAdminToken() > -1:
            self.fsm.getStateNamed('releaseNotesPage').addTransition('adminPage')
        self.fsm.enterInitialState()
        self.entered = 0
        self.parentFSM.getStateNamed('shtickerBook').addChild(self.fsm)

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def load(self):
        StateData.load(self)
        self.book_contents = loader.loadModel('phase_3.5/models/gui/stickerbook_gui.bam')
        self.book_texture = self.book_contents.find('**/big_book')
        self.book_open = loader.loadSfx('phase_3.5/audio/sfx/GUI_stickerbook_open.mp3')
        self.book_close = loader.loadSfx('phase_3.5/audio/sfx/GUI_stickerbook_delete.mp3')
        self.book_turn = loader.loadSfx('phase_3.5/audio/sfx/GUI_stickerbook_turn.mp3')

    def unload(self):
        self.book_texture.removeNode()
        del self.book_texture
        self.book_contents.removeNode()
        del self.book_contents
        loader.unloadSfx(self.book_open)
        del self.book_open
        loader.unloadSfx(self.book_close)
        del self.book_close
        loader.unloadSfx(self.book_turn)
        del self.book_turn
        del self.fsm
        del self.parentFSM
        del self.entered
        StateData.unload(self)

    def enter(self):
        if self.entered:
            return
        self.entered = 1
        StateData.enter(self)
        render.hide()
        base.setBackgroundColor(0.05, 0.15, 0.4)
        self.book_img = OnscreenImage(image=self.book_texture, scale=(2, 1, 1.5))
        self.book_open.play()
        if base.localAvatar.getAdminToken() > -1:
            self.fsm.request('adminPage')
        else:
            self.fsm.request('zonePage')

    def exit(self):
        if not self.entered:
            return
        self.entered = 0
        base.setBackgroundColor(CIGlobals.DefaultBackgroundColor)
        render.show()
        self.book_img.destroy()
        del self.book_img
        self.book_close.play()
        self.fsm.request('off')
        StateData.exit(self)

    def enterZonePage(self):
        self.createPageButtons('optionPage', 'releaseNotesPage')
        self.setTitle('Places')
        self.ttc_btn = DirectButton(geom=(qt_btn.find('**/QuitBtn_UP'), qt_btn.find('**/QuitBtn_DN'), qt_btn.find('**/QuitBtn_RLVR')), relief=None, scale=1.2, text_scale=0.045, text=CIGlobals.ToontownCentral, command=self.finished, extraArgs=[CIGlobals.ToontownCentralId], pos=(-0.45, 0.15, 0.5), text_pos=(0, -0.01))
        self.minigame_btn = DirectButton(geom=(qt_btn.find('**/QuitBtn_UP'), qt_btn.find('**/QuitBtn_DN'), qt_btn.find('**/QuitBtn_RLVR')), relief=None, scale=1.2, text_scale=0.055, text=CIGlobals.MinigameArea, command=self.finished, extraArgs=[CIGlobals.MinigameAreaId], pos=(-0.45, 0.35, 0.38), text_pos=(0, -0.01))
        self.populationLbl = OnscreenText(text='', pos=(0.45, 0.1), align=TextNode.ACenter)
        self.popRecordLbl = OnscreenText(text='', pos=(0.45, -0.1), align=TextNode.ACenter, scale=0.05)
        taskMgr.add(self.__updateGamePopulation, 'ShtickerBook-updateGamePopulation')
        return

    def __updateGamePopulation(self, task):
        population = 0
        for district in base.cr.activeDistricts.values():
            population += district.getPopulation()

        self.populationLbl.setText('Game Population:\n' + str(population))
        recordPopulation = base.cr.myDistrict.getPopRecord()
        self.popRecordLbl.setText('Record Population:\n' + str(recordPopulation))
        task.delayTime = 5.0
        return task.again

    def exitZonePage(self):
        taskMgr.remove('ShtickerBook-updateGamePopulation')
        self.popRecordLbl.destroy()
        del self.popRecordLbl
        self.populationLbl.destroy()
        del self.populationLbl
        self.ttc_btn.destroy()
        del self.ttc_btn
        self.minigame_btn.destroy()
        del self.minigame_btn
        self.deletePageButtons(True, True)
        self.clearTitle()

    def createPageButtons(self, back, fwd):
        if back:
            self.btn_prev = DirectButton(geom=(self.book_contents.find('**/arrow_button'), self.book_contents.find('**/arrow_down'), self.book_contents.find('**/arrow_rollover')), relief=None, pos=(-0.838, 0, -0.661), scale=(-0.1, 0.1, 0.1), command=self.pageDone, extraArgs=[back])
        if fwd:
            self.btn_next = DirectButton(geom=(self.book_contents.find('**/arrow_button'), self.book_contents.find('**/arrow_down'), self.book_contents.find('**/arrow_rollover')), relief=None, pos=(0.838, 0, -0.661), scale=(0.1, 0.1, 0.1), command=self.pageDone, extraArgs=[fwd])
        return

    def deletePageButtons(self, back, fwd):
        if back:
            self.btn_prev.destroy()
            del self.btn_prev
        if fwd:
            self.btn_next.destroy()
            del self.btn_next

    def setTitle(self, title):
        self.page_title = OnscreenText(text=title, pos=(0, 0.62, 0), scale=0.12)

    def clearTitle(self):
        self.page_title.destroy()
        del self.page_title

    def enterReleaseNotesPage(self):
        if base.localAvatar.getAdminToken() > -1:
            self.createPageButtons('zonePage', 'adminPage')
        else:
            self.createPageButtons('zonePage', None)
        self.setTitle('Release Notes')
        self.frame = DirectScrolledFrame(canvasSize=(-1, 1, -3, 1), frameSize=(-1, 1, -0.6, 0.6))
        self.frame.setPos(0, 0, 0)
        self.frame.setScale(0.8)
        self.release_notes = DirectLabel(text=open('release_notes.txt', 'r').read(), text_align=TextNode.ALeft, pos=(-0.955, 0, 0.93), relief=None, text_fg=(0, 0, 0, 1), text_wordwrap=37.0, text_scale=0.05, parent=self.frame.getCanvas())
        return

    def exitReleaseNotesPage(self):
        self.frame.destroy()
        del self.frame
        self.release_notes.destroy()
        del self.release_notes
        self.clearTitle()
        if base.localAvatar.getAdminToken() > -1:
            self.deletePageButtons(True, True)
        else:
            self.deletePageButtons(True, False)

    def enterAdminPage(self):
        self.adminPageStateData = AdminPage(self, self.fsm)
        self.adminPageStateData.load()
        self.adminPageStateData.enter()

    def exitAdminPage(self):
        self.adminPageStateData.exit()
        self.adminPageStateData.unload()
        del self.adminPageStateData

    def pageDone(self, nextPage):
        self.fsm.request(nextPage)
        self.book_turn.play()

    def enterOptionPage(self):
        self.optionPageStateData = OptionPage(self, self.fsm)
        self.optionPageStateData.load()
        self.optionPageStateData.enter()

    def exitOptionPage(self):
        self.optionPageStateData.exit()
        self.optionPageStateData.unload()
        del self.optionPageStateData

    def prevPage(self, currentPage):
        self.clearCurrentPage()
        if self.currentPage == 2:
            self.optionPage()
        elif self.currentPage == 3:
            self.zonePage()
        elif self.currentPage == 4:
            self.releaseNotesPage()

    def nextPage(self, currentPage):
        self.clearCurrentPage()
        if self.currentPage == 1:
            self.zonePage()
        elif self.currentPage == 2:
            self.releaseNotesPage()
        elif self.currentPage == 3:
            self.adminPage()

    def clearCurrentPage(self):
        self.book_turn.play()
        for m in base.bookpgnode.getChildren():
            m.removeNode()

    def finished(self, zone):
        if base.localAvatar.getHealth() < 1 and type(zone) == type(1):
            return
        else:
            doneStatus = {}
            if zone in [CIGlobals.ToontownCentralId, CIGlobals.MinigameAreaId]:
                doneStatus['mode'] = 'teleport'
                doneStatus['zoneId'] = zone
                doneStatus['hoodId'] = ZoneUtil.getHoodId(zone)
                doneStatus['where'] = ZoneUtil.getWhereName(zone)
                doneStatus['how'] = 'teleportIn'
                doneStatus['avId'] = base.localAvatar.doId
                doneStatus['shardId'] = None
                doneStatus['loader'] = ZoneUtil.getLoaderName(zone)
            else:
                doneStatus['mode'] = zone
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
            return

    def closeBook(self):
        self.book_close.play()
        base.bookpgnode.removeNode()
        base.booknode.removeNode()