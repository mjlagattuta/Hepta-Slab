mv HeptaSlab-2x.glyphs HeptaSlabBuild.glyphs

mkdir brace-sources
mkdir brace-ttfs

# Remove nonexporting glyphs + slice file
python2 $(dirname ${BASH_SOURCE[0]})/fixBraces.py HeptaSlabBuild.glyphs

for path in brace-sources/*.glyphs; do
	filename=${path##*/}
	thisFolder="${path%/*}"
	ttfname="${filename%.*}-VF.ttf"
	
	fontmake -o variable -g $path --no-production-names

	mv variable_ttf/$ttfname brace-ttfs/$ttfname
	rm -rf master_ufo
	rm -rf variable_ttf
done

rm -rf brace-sources

python2 $(dirname ${BASH_SOURCE[0]})/fixBrackets.py HeptaSlabBuild.glyphs

fontmake -o variable -g HeptaSlabBuild.glyphs

mv variable_ttf/HeptaSlab-VF.ttf HeptaSlab-VF.ttf
rm -rf master_ufo
rm -rf variable_ttf
rm -rf HeptaSlabBuild.glyphs

python2 addFeatureVars.py HeptaSlab-VF.ttf

rm -rf addFeatureVars.py

for path in brace-ttfs/*.ttf; do
	filename=${path##*/}
	thisFolder="${path%/*}"
	
	ttx $path
	rm -rf $path
done

gftools fix-nonhinting HeptaSlab-VF.ttf HeptaSlab-VF.ttf
gftools fix-dsig --autofix HeptaSlab-VF.ttf
gftools fix-gasp HeptaSlab-VF.ttf

ttx HeptaSlab-VF.ttf

rm -rf HeptaSlab-VF.ttf
rm -rf HeptaSlab-VF-backup-fonttools-prep-gasp.ttf

# cp HeptaSlab-VF.ttx HeptaSlabBase-VF.ttx

for path in brace-ttfs/*.ttx; do
	filename=${path##*/}
	thisFolder="${path%/*}"
    glyphName="$(echo $filename | sed -e 's,-source.*,,')"
    gvar="$(cat $path | tr '\n' '\r' | sed -n "s,.*\(<glyphVariations glyph=\"$glyphName\".*<\/glyphVariations>\).*,\1,p")"
    glyf="$(cat $path | tr '\n' '\r' | sed -n "s,.*\(<TTGlyph name=\"$glyphName\".*<\/TTGlyph>\).*,\1,p")"

    echo $filename
    echo $glyphName
    echo "Adding $glyphName glyf data..."
	cat HeptaSlab-VF.ttx | tr '\n' '\r' | sed -e "s,<TTGlyph name=\"$glyphName\"[^T]*TTGlyph>,$glyf," | tr '\r' '\n' > HeptaSlabGlyf-VF.ttx
	echo "Adding $glyphName gvar data..."
	cat HeptaSlabGlyf-VF.ttx | tr '\n' '\r' | sed -e "s,<glyphVariations glyph=\"$glyphName\"[^V]*Variations>,$gvar," | tr '\r' '\n' > HeptaSlab-VF.ttx

	rm -rf HeptaSlabGlyf-VF.ttx
done

rm -rf brace-ttfs

cat HeptaSlab-VF.ttx | tr '\n' '\r' | sed -e "s,<STAT>.*<\/STAT>,$(cat $(dirname ${BASH_SOURCE[0]})/patch-STAT.xml | tr '\n' '\r')," | tr '\r' '\n' > HeptaSlab-VF-STAT.ttx

rm -rf HeptaSlab-VF.ttx

ttx HeptaSlab-VF-STAT.ttx

rm -rf HeptaSlab-VF-STAT.ttx

mv HeptaSlab-VF-STAT.ttf HeptaSlab-VF.ttf