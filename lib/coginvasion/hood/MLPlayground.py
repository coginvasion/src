# Embedded file name: lib.coginvasion.hood.MLPlayground
from direct.directnotify.DirectNotifyGlobal import directNotify
from Playground import Playground

class MLPlayground(Playground):
    notify = directNotify.newCategory('MLPlayground')