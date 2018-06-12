#MenuTitle: Reinterpolate + Re-key Sidebearings
# -*- coding: utf-8 -*-

__doc__="""
Reinterpolates sidebearings and then updates metrics keys accordingly for selected layers for active master.
References the adjacent master for keys, if none then no layer key is added.
Will reinterpolate and rekey for intermediate masters, but for bookend masters it will only rekey
"""

import GlyphsApp
import re

font = Glyphs.font
masterTotal = len(font.masters)
masterIndex = font.masterIndex

# Sets bolder adjacent master as reference for keys
refIndex = masterIndex + 1

# If boldest master, reference the only adjacent master
if masterIndex == (masterTotal - 1):
    refIndex = masterIndex - 1

layers = font.selectedLayers

leftSide = True
rightSide = False

# Takes a layer and side and returns the nice name for referenced glyph whether keyed for layer or glyph
def checkKey(key, side):
    # Left side
    if side == True:
        # If layer key on adjacent master layer, return reference
        if key.parent.layers[refIndex].leftMetricsKey != None:
            keyA = re.sub('-\d+', '', key.parent.layers[refIndex].leftMetricsKey)
            keyB = re.sub('\.\d+', '', keyA)
            key = re.sub('=*' '\d*' '\+*' '/*', '', keyB)
            return (key, True)
        # If glyph key return reference
        elif key.parent.leftMetricsKey != None:
            keyA = re.sub('-\d+', '', key.parent.leftMetricsKey)
            keyB = re.sub('\.\d+', '', keyA)
            key = re.sub('=*' '\d*' '\+*' '/*', '', keyB) 
            return (key, False)
        # If no keys return none
        else:
            return (None, None)
    # Right side
    else:
        # If layer key on adjacent master layer, return reference
        if key.parent.layers[refIndex].rightMetricsKey != None:
            keyA = re.sub('-\d+', '', key.parent.layers[refIndex].rightMetricsKey)
            keyB = re.sub('\.\d+', '', keyA)
            key = re.sub('=*' '\d*' '\+*' '/*', '', keyB)
            return (key, True)
        # If glyph key return reference
        elif key.parent.rightMetricsKey != None:
            keyA = re.sub('-\d+', '', key.parent.rightMetricsKey)
            keyB = re.sub('\.\d+', '', keyA)
            key = re.sub('=*' '\d*' '\+*' '/*', '', keyB)
            return (key, False)
        # If no keys return none
        else:
            return (None, None)

# Takes two sidebearings and a glyph name and outputs a corresponding metrics key
def genKey(current, key, side, refName):
    flip = False

    # Check if pipe is present and set flip accordingly
    if re.match('\|', refName) != None:
        refName = re.sub('\|', '', refName)
        flip = True
        # If only pipe was used in key, add reference to current glyph
        if refName == '':
            refName = key.parent.name
    else:
        flip = False

    if refName == '':
        return None
    elif re.match('{.*}', key.parent.layers[-1].name) != None:
        # If left
        if side == True:
            if flip == False:
                ref = genBraceRef(refName, key.parent.layers[-1].name, True)
            else:
                ref = genBraceRef(refName, key.parent.layers[-1].name, False)
        # If right
        else:
            if flip == False:
                ref = genBraceRef(refName, key.parent.layers[-1].name, False)
            else:
                ref = genBraceRef(refName, key.parent.layers[-1].name, True)
    else:
        # If left
        if side == True:
            if flip == False:
                ref = font.glyphs[refName].layers[masterIndex].LSB
            else:
                ref = font.glyphs[refName].layers[masterIndex].RSB
        # If right
        else:
            if flip == False:
                ref = font.glyphs[refName].layers[masterIndex].RSB
            else:
                ref = font.glyphs[refName].layers[masterIndex].LSB

    if ref > current:
        difference = int(ref - current)
        if flip == False:
            return '==' + refName + '-' + str(difference)
        else:
            if refName == key.parent.name:
                refName = ''
            return '==|' + refName + '-' + str(difference)
    else:
        difference = int(current - ref)
        if flip == False:
            return '==' + refName + '+' + str(difference)
        else:
            if refName == key.parent.name:
                refName = ''
            return '==|' + refName + '+' + str(difference)


# Takes glyph name as reference by brace layer, generates an intepolation based on same weight
def genBraceRef(braceRefName, braceString, side):
    # Convert brace layer name to integer
    braceValue = int(re.sub('{*}*', '', braceString))
    
    braceRefLayer = font.glyphs[braceRefName].layers[masterIndex]

    # Copies layer on currently active master
    newLayerBrace = braceRefLayer.copy()
    
     # Add new layer as master layer
    font.glyphs[braceRefName].layers.append(newLayerBrace)

    # Set layer name to correct brace name
    newLayerBrace.name = braceString

    # Reinterpolate the temporary brace layer
    newLayerBrace.reinterpolate()

    if side == True:
        braceRefValue = newLayerBrace.LSB
    else:
        braceRefValue = newLayerBrace.RSB

    # Delete inteprolated layer
    del(font.glyphs[braceRefName].layers[newLayerBrace.layerId])
    
    return braceRefValue

# Iterates through selected layers for active master
for layer in layers:
    try:
        name = layer.name

        # Duplicate master layer
        newLayer = layer.copy()

        # Master layer is now "tmp"
        layer.name = "tmp"

        # New layer takes name of master layer
        newLayer.name = name

        # Add new layer as master layer
        layer.parent.layers.append(newLayer)

        # Prevents metrics change on bookend masters
        if masterIndex != 0 and masterIndex != (masterTotal - 1):
            newLayer.reinterpolate()
            
        if re.match('{.*}', newLayer.name) != None:
            newLayer.reinterpolate()

        # Copy updated sidebearings to original layer
        layer.LSB = newLayer.LSB
        layer.RSB = newLayer.RSB

        # If left layer key on adjacent master, generate key for this layer
        if checkKey(layer, leftSide)[1] == True:
            layer.leftMetricsKey = genKey(layer.LSB, layer, leftSide, checkKey(layer, leftSide)[0])
        else:
            layer.leftMetricsKey = None

        # If right layer key on adjacent master, generate key for this layer
        if checkKey(layer, rightSide)[1] == True:
            layer.rightMetricsKey = genKey(layer.RSB, layer, rightSide, checkKey(layer, rightSide)[0])
        else:
            layer.rightMetricsKey = None

        # Make original layer master layer
        layer.name = name

        del(layer.parent.layers[newLayer.layerId])
    except:
        None