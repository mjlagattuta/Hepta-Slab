# Script to build brace layers
## This script converts the input .glyphs file into a form with bracket layers converted to suffixed glyphs so that fontmake can generate the VF
## It uses the parsed bracket values to then generate a script to run on the final ttf using fonttools to enable the GSUB feature

# TODO

import sys
import os
import re
import copy
import time
from glyphsLib import GSFont
from glyphsLib import GSGlyph
from glyphsLib import GSLayer
from glyphsLib import GSFontMaster
from glyphsLib import GSInstance

start = time.time()

filename = sys.argv[-1]

font = GSFont(filename)

nonExportGlyphs = []
baseIndex = 0
for glyph in font.glyphs:
    if glyph.export == False:
        nonExportGlyphs.append(baseIndex)
        baseIndex -= 1
    baseIndex += 1

for baseIndex in nonExportGlyphs:
    del font._glyphs[baseIndex]

font.save(filename)
print "Build File Saved"

braceSources = []

def keepOneGlyph(font, glyphName):
    delGlyphs = []
    index = 0
    for glyph in font.glyphs:
        if glyph.name != glyphName:
            delGlyphs.append(index)
            index -= 1
        index += 1

    for glyphIndex in delGlyphs:
        del font._glyphs[glyphIndex]

for glyphIndex, glyph in enumerate(font.glyphs):
    hasBrace = False
    for layer in glyph.layers:
        if re.match('.*\d\}$', layer.name):
            hasBrace = True
            break
    if hasBrace == True:
        braceFont = GSFont(filename)
        braceFilename = glyph.name + "-source" + str(glyphIndex) + ".glyphs"
        print "Created file:" + glyph.name + "-source" + str(glyphIndex) + ".glyphs"
        braceFont.familyName = glyph.name + "-source" + str(glyphIndex)

        braceFont.features = []
        braceFont.classes = ()
        braceFont.kerning = {}

        # for feature in braceFont.features:
        #     braceFont.features.pop()

        # for eachClass in braceFont.classes:
        #     braceFont.classes.pop()

        # for prefix in braceFont.featurePrefixes:
        #     braceFont.featurePrefixes.pop()

        glyphName = glyph.name
        keepOneGlyph(braceFont, glyphName)

        addMasters = []
        for layer in braceFont.glyphs[0].layers:
            if re.match('.*\d\}$', layer.name):
                value = re.sub('.*{|}', '', layer.name)
                newMaster = copy.copy(braceFont.masters[0])
                newMaster.weightValue = int(value)
                newMaster.id = None
                newMaster.name = value
                addMasters.append([newMaster, layer.layerId])

        for master in addMasters:
            braceFont.masters.append(master[0])
            masterId = braceFont.masters[-1].id
            braceFont.glyphs[0].layers[masterId].paths = braceFont.glyphs[0].layers[master[1]].paths
            braceFont.glyphs[0].layers[masterId].components = braceFont.glyphs[0].layers[master[1]].components
            braceFont.glyphs[0].layers[masterId].anchors = braceFont.glyphs[0].layers[master[1]].anchors
            braceFont.glyphs[0].layers[masterId].width = braceFont.glyphs[0].layers[master[1]].width
            del braceFont.glyphs[0].layers[master[1]]

        braceFont.save("brace-sources/" + braceFilename)
        print "Saved file:" + glyph.name + "-source.glyphs"

end = time.time()
print end - start


