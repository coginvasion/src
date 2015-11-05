# Embedded file name: lib.coginvasion.hood.DLPlayground
from direct.directnotify.DirectNotifyGlobal import directNotify
from Playground import Playground

class DLPlayground(Playground):
    notify = directNotify.newCategory('DLPlayground')