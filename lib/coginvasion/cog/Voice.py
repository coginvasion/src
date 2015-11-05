# Embedded file name: lib.coginvasion.cog.Voice
"""

  Filename: Voice.py
  Created by: DecodedLogic (31July14)

"""

class Voice:

    def __init__(self, filePath):
        self.filePath = filePath

    def getSoundFile(self, expression):
        return self.filePath % expression


NORMAL = Voice('phase_3.5/audio/dial/COG_VO_%s.mp3')
SKELETON = Voice('phase_5/audio/sfx/Skel_COG_VO_%s.mp3')
BOSS = Voice('phase_9/audio/sfx/Boss_COG_VO_%s.mp3')

def getVoiceById(self, index):
    voices = [NORMAL, SKELETON, BOSS]
    return voices[index]