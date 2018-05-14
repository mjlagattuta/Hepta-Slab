#MenuTitle: Reinterpolate + Re-key Sidebearings
# -*- coding: utf-8 -*-

__doc__="""
Reinterpolate and update keys on sidebearings of selected layers for active master
"""

import GlyphsApp
import re

font = Glyphs.font
masterIndex = font.masterIndex
layers = font.selectedLayers

leftSide = True
rightSide = False

# Takes a layer and side and returns the nice name for referenced glyph whether keyed for layer or glyph
def checkKey(key, side):
    if side == True:
        if key.leftMetricsKey != None:
            keyA = re.sub('-\d+', '', key.leftMetricsKey)
            keyB = re.sub('\.\d+', '', keyA)
            key = re.sub('=*' '\d*' '\+*' '/*', '', keyB)
            return (key, True)
        elif key.parent.leftMetricsKey != None:
            keyA = re.sub('-\d+', '', key.parent.leftMetricsKey)
            keyB = re.sub('\.\d+', '', keyA)
            key = re.sub('=*' '\d*' '\+*' '/*', '', keyB) 
            return (key, False)
        else:
            return (None, None)
    else:
        if key.rightMetricsKey != None:
            keyA = re.sub('-\d+', '', key.rightMetricsKey)
            keyB = re.sub('\.\d+', '', keyA)
            key = re.sub('=*' '\d*' '\+*' '/*', '', keyB)
            return (key, True)
        elif key.parent.rightMetricsKey != None:
            keyA = re.sub('-\d+', '', key.parent.rightMetricsKey)
            keyB = re.sub('\.\d+', '', keyA)
            key = re.sub('=*' '\d*' '\+*' '/*', '', keyB)
            return (key, False)
        else:
            return (None, None)

# Takes two sidebearings and a glyph name and outputs a corresponding metrics key
def genKey(current, key, side, refName):
    if refName == None:
        return None
    else:
        if side == True and refName != '|':
            ref = font.glyphs[refName].layers[masterIndex].LSB
        elif side == True and refName == '|':
            ref = key.RSB
        elif side == False and refName != '|':
            ref = font.glyphs[refName].layers[masterIndex].RSB
        elif side == False and refName == '|':
            ref = key.LSB

    if ref > current:
        difference = int(ref-current)
        return '==' + refName + '-' + str(difference)
    else:
        difference = int(current-ref)
        return '==' + refName + '+' + str(difference)

# Iterates through selected glyphs for active master
for layer in layers:

        name = layer.name

        newLayer = layer.copy()
        layer.name = "tmp"
        newLayer.name = name

        layer.parent.layers.append(newLayer)

        newLayer.reinterpolate()

        layer.LSB = newLayer.LSB
        layer.RSB = newLayer.RSB

        if checkKey(layer, leftSide)[1] == True:
            layer.leftMetricsKey = genKey(layer.LSB, layer, leftSide, checkKey(layer, leftSide)[0])
        else:
            layer.leftMetricsKey = None
        if checkKey(layer, rightSide)[1] == True:
            layer.rightMetricsKey = genKey(layer.RSB, layer, rightSide, checkKey(layer, rightSide)[0])
        else:
            layer.rightMetricsKey = None

        layer.name = name

        del(layer.parent.layers[newLayer.layerId])