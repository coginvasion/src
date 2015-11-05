# Embedded file name: lib.coginvasion.base.SectionedSound
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *

class AudioClip(DirectObject):
    notify = directNotify.newCategory('SectionedMusic')

    def __init__(self, chunks):
        DirectObject.__init__(self)
        self.ival = None
        self.chunks = chunks
        return

    def playAllParts(self):
        self.ival = Sequence()
        for chunk in self.chunks:
            self.ival.append(SoundInterval(chunk, volume=0.5))
            self.ival.append(Func(messenger.send, 'AudioClip_partDone'))

        self.ival.append(Func(messenger.send, 'AudioClip_clipDone'))
        self.ival.append(Func(self.cleanup))
        self.ival.start()

    def stop(self):
        if self.ival:
            self.ival.pause()
            self.ival = None
        return

    def cleanup(self):
        self.stop()
        self.chunks = None
        return