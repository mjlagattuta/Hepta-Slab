cp HeptaSlab.glyphs HeptaSlabBuild.glyphs

python2 $(dirname ${BASH_SOURCE[0]})/delNonExp.py HeptaSlabBuild.glyphs
python2 $(dirname ${BASH_SOURCE[0]})/fixBrackets.py HeptaSlabBuild.glyphs

fontmake -o variable -g HeptaSlabBuild.glyphs

mv variable_ttf/HeptaSlab-VF.ttf HeptaSlab-VF.ttf
rm -rf master_ufo
rm -rf variable_ttf
rm -rf instance_ufo
rm -rf HeptaSlabBuild.glyphs

python2 addFeatureVars.py HeptaSlab-VF.ttf

rm -rf addFeatureVars.py


gftools fix-nonhinting HeptaSlab-VF.ttf HeptaSlab-VF.ttf
gftools fix-dsig --autofix HeptaSlab-VF.ttf
gftools fix-gasp HeptaSlab-VF.ttf

ttx -x 'MVAR' HeptaSlab-VF.ttf

rm -rf HeptaSlab-VF.ttf
rm -rf HeptaSlab-VF-backup-fonttools-prep-gasp.ttf


cat HeptaSlab-VF.ttx | tr '\n' '\r' | sed -e "s,<STAT>.*<\/STAT>,$(cat $(dirname ${BASH_SOURCE[0]})/patch-STAT.xml | tr '\n' '\r')," | tr '\r' '\n' > HeptaSlab-VF-STAT.ttx

ttx HeptaSlab-VF-STAT.ttx

rm -rf HeptaSlab-VF.ttx
rm -rf HeptaSlab-VF-STAT.ttx

mv HeptaSlab-VF-STAT.ttf HeptaSlab-VF.ttf