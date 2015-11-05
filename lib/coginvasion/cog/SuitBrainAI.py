# Embedded file name: lib.coginvasion.cog.SuitBrainAI
"""

  Filename: SuitBrainAI.py
  Created by: DecodedLogic (03Sep15)

"""
from direct.showbase.DirectObject import DirectObject
from lib.coginvasion.cog.SuitHabitualBehavior import SuitHabitualBehavior
from lib.coginvasion.cog.SuitPathBehavior import SuitPathBehavior
from direct.task.Task import Task
import operator

class SuitBrain(DirectObject):

    def __init__(self, suit):
        self.suit = suit
        self.behaviors = {}
        self.currentBehavior = None
        self.thinkTaskName = self.suit.uniqueName('think')
        self.isThinking = False
        return

    def addBehavior(self, behavior, priority):
        self.behaviors.update({behavior: priority})
        behavior.load()
        self.organizeBehaviors()

    def removeBehavior(self, behavior):
        for iBehavior in self.behaviors.keys():
            if iBehavior == behavior:
                self.behaviors.remove(iBehavior)
                if self.currentBehavior == behavior:
                    self.exitCurrentBehavior()

        self.organizeBehaviors()

    def getBehavior(self, behaviorType):
        for behavior in self.behaviors.keys():
            if behavior.__class__ == behaviorType:
                return behavior

    def exitCurrentBehavior(self):
        if self.currentBehavior:
            self.currentBehavior.exit()
            if isinstance(self.currentBehavior, SuitPathBehavior):
                self.currentBehavior.clearWalkTrack()
            if isinstance(self.currentBehavior, SuitHabitualBehavior) and self.currentBehavior.isActive():
                self.ignore(self.currentBehavior.getDoneEvent())
                if self.isThinking and not taskMgr.hasTaskNamed(self.thinkTaskName):
                    taskMgr.add(self.__think, self.thinkTaskName)
            self.currentBehavior = None
        return

    def organizeBehaviors(self):
        behaviors = {}
        for behavior, priority in self.behaviors.items():
            behaviors[behavior] = priority

        sorted_behaviors = sorted(behaviors.items(), key=operator.itemgetter(1))
        self.behaviors = {}
        for behaviorEntry in sorted_behaviors:
            behavior = behaviorEntry[0]
            priority = behaviorEntry[1]
            self.behaviors.update({behavior: priority})

    def startThinking(self, task = None):
        if not self.isThinking and not taskMgr.hasTaskNamed(self.thinkTaskName):
            self.isThinking = True
            taskMgr.add(self.__think, self.thinkTaskName)
            if task:
                return Task.done

    def stopThinking(self):
        if self.isThinking:
            self.isThinking = False
            taskMgr.remove(self.thinkTaskName)
            self.exitCurrentBehavior()

    def unloadBehaviors(self):
        for behavior in self.behaviors.keys():
            behavior.unload()
            del self.behaviors[behavior]

        if self.suit:
            self.suit = None
        del self.suit
        del self.behaviors
        del self.thinkTaskName
        del self.isThinking
        return

    def isThinking(self):
        return self.isThinking

    def __think(self, task = None):
        if task and self.currentBehavior:
            task.delayTime = 1
        if not hasattr(self, 'suit'):
            return Task.done
        if self.suit.isDead() or not self.isThinking:
            self.exitCurrentBehavior()
            self.isThinking = False
            return Task.done
        for behavior in self.behaviors.keys():
            if behavior.shouldStart():
                if behavior.isEntered == 1:
                    continue
                self.exitCurrentBehavior()
                behavior.enter()
                self.currentBehavior = behavior
                break

        if task:
            if isinstance(self.currentBehavior, SuitHabitualBehavior) and self.currentBehavior.isActive():
                self.acceptOnce(self.currentBehavior.getDoneEvent(), self.startThinking)
                self.isThinking = False
                return Task.done
            return Task.again