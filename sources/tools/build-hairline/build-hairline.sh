cp HeptaSlab.glyphs HeptaSlabHairline.glyphs

python2 $(dirname ${BASH_SOURCE[0]})/delNonExp.py HeptaSlabHairline.glyphs
# python2 $(dirname ${BASH_SOURCE[0]})/fixBrackets.py HeptaSlabHairline.glyphs
python2 $(dirname ${BASH_SOURCE[0]})/prepHairline.py HeptaSlabHairline.glyphs

rm -rf addFeatureVars.py

fontmake -o ttf -g HeptaSlabHairline.glyphs -i

rm -rf HeptaSlabHairline.glyphs
rm -rf instance_ufo
rm -rf master_ufo
mv instance_ttf/HeptaSlabHairline-Regular.ttf HeptaSlabHairline-Regular.ttf
rm -rf instance_ttf

gftools fix-nonhinting HeptaSlabHairline-Regular.ttf HeptaSlabHairline-Regular.ttf
gftools fix-dsig --autofix HeptaSlabHairline-Regular.ttf
gftools fix-gasp HeptaSlabHairline-Regular.ttf
rm -rf HeptaSlabHairline-Regular-backup-fonttools-prep-gasp.ttf