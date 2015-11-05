# Embedded file name: lib.coginvasion.gui.PieGui
"""
  
  Filename: PieGui.py
  Created by: blach (6Aug14)
  
"""
from panda3d.core import *
from direct.gui.DirectGui import *
from direct.directnotify.DirectNotify import *
from direct.interval.SoundInterval import SoundInterval
from direct.showbase.DirectObject import *

class PieGui(DirectObject):
    notify = DirectNotify().newCategory('PieGui')

    def __init__(self, pieclass):
        DirectObject.__init__(self)
        self.weapon = 'tart'
        self.pies = pieclass

    def createGui(self):
        self.deleteGui()
        gui = loader.loadModel('phase_3.5/models/gui/weapon_gui.bam')
        self.gui_dict = {1: {'idle': gui.find('**/tart_idle'),
             'selected': gui.find('**/tart_selected'),
             'disabled': gui.find('**/tart_disabled')},
         0: {'idle': gui.find('**/cake_idle'),
             'selected': gui.find('**/cake_selected'),
             'disabled': gui.find('**/cake_disabled')},
         2: {'idle': gui.find('**/slice_idle'),
             'selected': gui.find('**/slice_selected'),
             'disabled': gui.find('**/slice_disabled')},
         3: {'idle': gui.find('**/tnt_idle'),
             'selected': gui.find('**/tnt_selected'),
             'disabled': gui.find('**/tnt_idle')}}
        self.guiPos = {'noTnt': [(0, 0, -0.5), (0, 0, 0), (0, 0, 0.5)],
         'tnt': [(0, 0, -0.15),
                 (0, 0, 0.15),
                 (0, 0, 0.45),
                 (0, 0, -0.45)]}
        self.guiFrame = DirectFrame(parent=base.a2dRightCenter, pos=(-0.2, 0, 0))
        img1 = OnscreenImage(image=gui.find('**/cake_idle'), pos=(0, 0, -0.5), scale=0.3, parent=self.guiFrame)
        img2 = OnscreenImage(image=gui.find('**/tart_selected'), pos=(0, 0, 0.0), scale=0.3, parent=self.guiFrame)
        img3 = OnscreenImage(image=gui.find('**/slice_idle'), pos=(0, 0, 0.5), scale=0.3, parent=self.guiFrame)
        img4 = OnscreenImage(image=gui.find('**/tnt_idle'), pos=(0, 0, -0.75), scale=0.3, parent=self.guiFrame)
        img4.hide()
        self.ammo_lbl = DirectLabel(text='Ammo: %s' % self.pies.getAmmo(), text_fg=(1, 1, 1, 1), relief=None, text_shadow=(0, 0, 0, 1), text_scale=0.08, pos=(0.2, 0, 0.35), parent=base.a2dBottomLeft)
        self.gui_list = [img1,
         img2,
         img3,
         img4]
        self.enableWeaponSwitch()
        gui.remove_node()
        del gui
        return

    def deleteGui(self):
        self.disableWeaponSwitch()
        if hasattr(self, 'gui_list'):
            for gui in self.gui_list:
                gui.destroy()
                gui = None

            del self.gui_list
        if hasattr(self, 'ammo_lbl'):
            self.ammo_lbl.destroy()
            del self.ammo_lbl
        return

    def enableWeaponSwitch(self):
        if self.pies.current_ammo[3] >= 1:
            self.accept('4', self.setWeapon, ['tnt'])
        self.accept('3', self.setWeapon, ['cake'])
        self.accept('2', self.setWeapon, ['tart'])
        self.accept('1', self.setWeapon, ['slice'])
        self.accept('wheel_up', self.setWeapon, ['slice'])
        self.accept('wheel_down', self.setWeapon, ['cake'])

    def disableWeaponSwitch(self):
        self.ignore('1')
        self.ignore('2')
        self.ignore('3')
        self.ignore('4')
        self.ignore('wheel_up')
        self.ignore('wheel_down')

    def setWeapon(self, weapon, playSound = True):
        self.weapon = weapon
        if playSound:
            sfx = base.loadSfx('phase_3/audio/sfx/GUI_balloon_popup.mp3')
            SoundInterval(sfx).start()
        if weapon == 'cake':
            base.localAvatar.b_setPieType(0)
            if self.pies.current_ammo[3] >= 1:
                self.accept('wheel_down', self.setWeapon, ['tnt'])
            else:
                self.accept('wheel_down', self.setWeapon, ['slice'])
            self.accept('wheel_up', self.setWeapon, ['tart'])
        elif weapon == 'tart':
            base.localAvatar.b_setPieType(1)
            self.accept('wheel_up', self.setWeapon, ['slice'])
            self.accept('wheel_down', self.setWeapon, ['cake'])
        elif weapon == 'slice':
            base.localAvatar.b_setPieType(2)
            self.accept('wheel_down', self.setWeapon, ['tart'])
            if self.pies.current_ammo[3] >= 1:
                self.accept('wheel_up', self.setWeapon, ['tnt'])
            else:
                self.accept('wheel_up', self.setWeapon, ['cake'])
        elif weapon == 'tnt':
            base.localAvatar.b_setPieType(3)
            self.accept('wheel_up', self.setWeapon, ['cake'])
            self.accept('wheel_down', self.setWeapon, ['slice'])
        self.resetGui()
        self.gui_list[self.pies.getPieType()]['image'] = self.gui_dict[self.pies.getPieType()]['selected']
        self.update()

    def resetGui(self):
        if hasattr(self, 'gui_list') and hasattr(self, 'gui_dict'):
            for i in range(4):
                self.gui_list[i]['image'] = self.gui_dict[i]['idle']
                if self.pies.current_ammo[i] <= 0:
                    self.gui_list[i]['image'] = self.gui_dict[i]['disabled']
                if self.pies.current_ammo[3] <= 0:
                    for gui_index in range(3):
                        self.gui_list[gui_index].setPos(self.guiPos['noTnt'][gui_index])

                    self.gui_list[3].hide()
                else:
                    for gui_index in range(4):
                        self.gui_list[gui_index].setPos(self.guiPos['tnt'][gui_index])

    def update(self):
        if hasattr(self, 'ammo_lbl') and hasattr(self, 'gui_list'):
            if self.pies.getAmmo() <= 0:
                self.gui_list[self.pies.getPieType()]['image'] = self.gui_dict[self.pies.getPieType()]['disabled']
                self.ammo_lbl['text_fg'] = (0.9, 0, 0, 1)
                if self.pies.getPieType() == 3:
                    self.setWeapon('tart')
                    self.ignore('4')
            else:
                self.ammo_lbl['text_fg'] = (1, 1, 1, 1)
            self.ammo_lbl['text'] = 'Ammo: %s' % self.pies.getAmmo()