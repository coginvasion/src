# Embedded file name: lib.coginvasion.gags.FruitPieSlice
"""

  Filename: FruitPieSlice.py
  Created by: DecodedLogic (15Jul15)

"""
from lib.coginvasion.gags.ThrowGag import ThrowGag
from lib.coginvasion.gags import GagGlobals
from lib.coginvasion.globals import CIGlobals

class FruitPieSlice(ThrowGag):

    def __init__(self):
        ThrowGag.__init__(self, CIGlobals.FruitPieSlice, 'phase_5/models/props/fruit-pie-slice.bam', 10, GagGlobals.SLICE_SPLAT_SFX, GagGlobals.TART_SPLAT_COLOR)
        self.setHealth(GagGlobals.FRUIT_PIE_SLICE_HEAL)
        self.setImage('phase_3.5/maps/fruit_pie_slice.png')