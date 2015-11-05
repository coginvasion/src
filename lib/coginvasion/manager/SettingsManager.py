# Embedded file name: lib.coginvasion.manager.SettingsManager
"""

  Filename: SettingsManager.py
  Created by: blach (??July14)
  
"""
from panda3d.core import *
from pandac.PandaModules import *
from direct.directnotify.DirectNotify import DirectNotify
import json
notify = DirectNotify().newCategory('SettingsManager')

class SettingsManager:

    def applySettings(self, jsonfile):
        if not jsonfile:
            raise StandardError('no file specified!')
        info = open(jsonfile)
        jsonInfo = json.load(info)
        settings = jsonInfo['settings']
        width, height = settings['resolution']
        fs = settings['fullscreen']
        music = settings['music']
        sfx = settings['sfx']
        tex_detail = settings['texture-detail']
        model_detail = settings['model-detail']
        aa = settings['aa']
        af = settings.get('af', None)
        if af == None:
            self.writeSettingToFile('af', 'off', 'settings.json')
        base.enableMusic(music)
        base.enableSoundEffects(sfx)
        if aa == 'on':
            render.set_antialias(AntialiasAttrib.MMultisample)
            aspect2d.set_antialias(AntialiasAttrib.MMultisample)
        else:
            loadPrcFileData('', 'framebuffer-multisample 0')
            loadPrcFileData('', 'multisamples 0')
            render.clear_antialias()
        ts = TextureStage('ts')
        if tex_detail == 'high':
            pass
        elif tex_detail == 'low':
            loadPrcFileData('', 'compressed-textures 1')
        wp = WindowProperties()
        wp.setSize(width, height)
        wp.setFullscreen(fs)
        base.win.requestProperties(wp)
        info.close()
        return

    def getSettings(self, jsonfile):
        if jsonfile:
            info = open(jsonfile)
            jsonInfo = json.load(info)
            settings = jsonInfo['settings']
            width, height = settings['resolution']
            fs = settings['fullscreen']
            music = settings['music']
            sfx = settings['sfx']
            tex_detail = settings['texture-detail']
            model_detail = settings['model-detail']
            aa = settings['aa']
            af = settings['af']
            return tuple((width,
             height,
             fs,
             music,
             sfx,
             tex_detail,
             model_detail,
             aa,
             af))
        raise StandardError('no file specified!')

    def writeSettingToFile(self, setting, value, jsonfile, apply = 0):
        info = open(jsonfile)
        jsonInfo = json.load(info)
        if setting == 'fullscreen':
            jsonInfo['settings'][setting] = value[0]
        else:
            jsonInfo['settings'][setting] = value
        jsonFile = open(jsonfile, 'w+')
        jsonFile.write(json.dumps(jsonInfo))
        jsonFile.close()
        if apply:
            if setting == 'resolution':
                width, height = value
                wp = WindowProperties()
                wp.setSize(width, height)
                base.win.requestProperties(wp)
            elif setting == 'fullscreen':
                wp = WindowProperties()
                wp.setFullscreen(value[0])
                base.win.requestProperties(wp)
        info.close()