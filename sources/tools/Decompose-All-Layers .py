#MenuTitle: Decompose All Layers
# -*- coding: utf-8 -*-

__doc__="""
Decompose all layers across all masters
"""

import GlyphsApp

for font in Glyphs.fonts:
    for glyph in font.glyphs:
        for layer in glyph.layers:
            layer.decomposeComponents()