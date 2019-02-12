import sys
import os
import re
from glyphsLib import GSFont
from glyphsLib import GSGlyph

filename = sys.argv[-1]

font = GSFont(filename)

nonExportGlyphs = []
baseIndex = 0
for glyph in font.glyphs:
    for layer in glyph.layers:
    	if re.match('.*\}.*', layer.name) != None:
    		layer.name = 'Brace Off'
    	elif re.match('.*\].*', layer.name) != None:
    		layer.name = 'Bracket Off'

font.familyName = "Hepta Slab Hairline"

font.instances[0].active = True

del font.instances[1:]

font.save(filename)