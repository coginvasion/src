# Embedded file name: lib.coginvasion.cog.SuitHabitualBehavior
"""

  Filename: SuitHabitualBehavior.py
  Created by: DecodedLogic (03Sep15)

"""
from lib.coginvasion.cog.SuitBehaviorBase import SuitBehaviorBase

class SuitHabitualBehavior(SuitBehaviorBase):

    def __init__(self, suit, doneEvent = None):
        if doneEvent == None:
            doneEvent = 'suit%s-behaviorDone' % suit.doId
        SuitBehaviorBase.__init__(self, suit, doneEvent)
        self.isEntered = 0
        return