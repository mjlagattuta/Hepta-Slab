#MenuTitle: Add VF Bracket Layers
# -*- coding: utf-8 -*-

__doc__="""
For use in prepping for a variable font export
It is recommended to run this script on a duplicate of your source file only before exporting a variable font
Matches the setup of bracket layers for all glyphs with components whose root glyph has bracket layers
"""

import GlyphsApp
import re

import time
start = time.time()

getBrackets = []
# Make writeBrackets non-zero to start while loop in main()
writeBrackets = [1, 2, 3]
missingBrackets = []

font = Glyphs.font

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

# Checks if current glyph already has bracket layers
def hasBracket(glyphName):
    for i in range(len(getBrackets)):
        if re.match('^%s$' % glyphName, getBrackets[i][0]) != None:
            return True
    return False

# Checks all components in a glyph until it matches to a glyph.name from getBrackets list. Appends name and index in getBrackets
def checkComponents(glyph):
    for layer in glyph.layers:
        for component in layer.components:
            for i in range(len(getBrackets)):
                if re.match('^%s$' % component.name, getBrackets[i][0]) != None:
                    # List used to track when script is done adding layers
                    writeBrackets.append([glyph.name, i])
                    genBrackets(glyph, i)
                    return

def genBrackets(glyph, i):
    # Runs through master layers
    for j in range(len(font.masters)):
        # Copies master layer (and layer.associatedMasterId)
        newLayer = glyph.layers[j].copy()
        # Runs through getBrackets list
        for k in range(len(font.masters)):
            if re.match(newLayer.associatedMasterId, getBrackets[i + k][2]) != None:
                # Nw layer takes name of bracket with corresponding master id
                newLayer.name = getBrackets[i + k][1]
                # Add new bracket layer
                glyph.layers.append(newLayer)
                break
    print "Added bracket layers for glyph '%s'" % glyph.name

def main():
    wrongSetup = False
    # Check all glyphs for proper bracket setup and populate getBrackets list
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

    # If wrong setup print list of glyphs, else check all components against existing bracket glyphs
    if wrongSetup == True:
        print "No changes were made due to missing bracket layers on the following glyphs:"
        for i in range(len(missingBrackets)):
            print missingBrackets[i]
        end = time.time()
        print end - start
    else:
        # Populate writeBrackets list
        for glyph in font.glyphs:
            # If glyph already has bracket layers, or is not exporting, no need to run through its layers and components
            if hasBracket(glyph.name) == True or glyph.export == False:
                pass
            else:
                checkComponents(glyph)
    print len(writeBrackets)

# Main function runs until there are no more glyphs in need of bracket layers
while len(writeBrackets) > 0:
    writeBrackets = []
    main()

end = time.time()
print "Total time: %ds" % (end - start)





