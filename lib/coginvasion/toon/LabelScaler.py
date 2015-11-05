# Embedded file name: lib.coginvasion.toon.LabelScaler
"""
  
  Filename: LabelScaler.py
  Created by: blach (9July14)

"""
import math

class LabelScaler:
    SCALING_MINDIST = 1
    SCALING_MAXDIST = 50

    def __init__(self, factor = 0.055):
        self.SCALING_FACTOR = factor

    def resize(self, node):
        self.node = node
        taskMgr.add(self.resizeTask, 'resizeTask')

    def resizeTask(self, task):
        if self.node.isEmpty():
            return task.done
        distance = self.node.getDistance(camera)
        distance = max(min(distance, self.SCALING_MAXDIST), self.SCALING_MINDIST)
        self.node.setScale(math.sqrt(distance) * self.SCALING_FACTOR)
        return task.cont