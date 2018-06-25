#MenuTitle: Check VF Bracket Layer Setup
# -*- coding: utf-8 -*-

__doc__="""
For use in prepping for a variable font export
Checks if glyphs with bracket layers are properly set up for a VF export
Does not change anything
"""

import GlyphsApp
import re

missingBrackets = []

font = Glyphs.font

wrongSetup = False

# Checks if all master layers have a corresponding bracket layer
def checkBracketSetup(glyph):
    count = 0
    for layer in glyph.layers:
        if re.match('.*\d\]$', layer.name) != None:
            count = count + 1
    if count == len(font.masters):
        return True
    elif count == 0:
        return None
    else:
        return False

# Check all glyphs for proper bracket setup
for glyph in font.glyphs:
    # If setup is good
    if checkBracketSetup(glyph) == True:
        for layer in glyph.layers:
            if re.match('.*\d\]$', layer.name) != None:
                # print layer.parent.name, layer.name, re.match('.\d*\]$', layer.name)
                getBrackets.append([glyph.name, layer.name, layer.associatedMasterId])
    # If no brackets
    elif checkBracketSetup(glyph) == None:
        pass
    # If setup is bad
    else:
        missingBrackets.append(glyph.name)
        wrongSetup = True

# If wrong setup print list of glyphs
if wrongSetup == True:
    print "There are missing bracket layers on the following glyphs:"
    for i in range(len(missingBrackets)):
        print missingBrackets[i]
else:
    print "All glyphs with bracket layers are ready for export. Duplicate file before running 'Add-VF-Bracket-Layers.py'"





