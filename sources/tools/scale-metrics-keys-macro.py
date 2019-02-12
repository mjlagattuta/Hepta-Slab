import re

currentUPM = 1000
newUPM = 2000
scale = newUPM / currentUPM

def scaleValue(metricsKey):
    if re.match('.*\d+', str(metricsKey)) == None or metricsKey == None:
        return False
    else:
        if re.match('.*[+-].*', str(metricsKey)) != None:
            return True
        elif re.match('.*[*/].*', str(metricsKey)) == None and re.match('=.*', str(metricsKey)) != None:
            return True
        else:
            return False

for glyph in Font.glyphs:
    print "\n"
    print glyph.name, glyph.leftMetricsKey, glyph.rightMetricsKey
    if scaleValue(glyph.leftMetricsKey):
        val = int(re.sub('.*[+-]\D*', '', re.sub('=*', '', glyph.leftMetricsKey))) * scale
        before = glyph.leftMetricsKey
        glyph.leftMetricsKey = re.sub('\d*', '', glyph.leftMetricsKey) + str(val)
        print "UPDATE", glyph.name, before, glyph.leftMetricsKey
    if scaleValue(glyph.rightMetricsKey):
        val = int(re.sub('.*[+-]\D*', '', re.sub('=*', '', glyph.rightMetricsKey))) * scale
        before = glyph.rightMetricsKey
        glyph.rightMetricsKey = re.sub('\d*', '', glyph.rightMetricsKey) + str(val)
        print "UPDATE", glyph.name, before, glyph.rightMetricsKey
    for layer in glyph.layers:
        print layer.name, layer.leftMetricsKey, layer.rightMetricsKey
        if scaleValue(layer.leftMetricsKey):
            val = int(re.sub('.*[+-]\D*', '', re.sub('=*', '', layer.leftMetricsKey))) * scale
            before = layer.leftMetricsKey
            layer.leftMetricsKey = re.sub('\d*', '', layer.leftMetricsKey) + str(val)
            print "UPDATE", layer.name, before, layer.leftMetricsKey
        if scaleValue(layer.rightMetricsKey):
            val = int(re.sub('.*[+-]\D*', '', re.sub('=*', '', layer.rightMetricsKey))) * scale
            before = layer.rightMetricsKey
            layer.rightMetricsKey = re.sub('\d*', '', layer.rightMetricsKey) + str(val)
            print "UPDATE", layer.name, before, layer.rightMetricsKey