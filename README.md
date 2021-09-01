# Hepta Slab

## Description
Hepta Slab is a slab-serif revival based on specimens of antique genre types from Bruce and Co., primarily Antique 307. The family consists of 9 weights with the extremes intended for display use and the middle weights for setting text.

<br/>

![Character Set](docs/images/v0.008-waterfall.svg)


![Hepta Slab Waterfall](docs/images/v0.008-charSet.svg)

## Features
Features include lining numerals, oldstyle numerals, case sensitive punctuation, fractions, superior and inferior numerals as well as multiple stylistic alternates.

## Notes
*Glyphs marked in a color are indicated on the labelkey.txt file in the sources folder. The list can be viewed in Glyphs App with the LabelKey plugin via the Glyphs Plugin Manager.*

## Building

Fonts are built automatically by GitHub Actions - take a look in the "Actions" tab for the latest build.

If you particularly want to build fonts manually on your own computer, you will need to install the [`yq` utility](https://github.com/mikefarah/yq). On OS X with Homebrew, type `brew install yq`; on Linux, try `snap install yq`; if all else fails, try the instructions on the linked page.

Then:

* `make build` will produce font files.
* `make test` will run [FontBakery](https://github.com/googlefonts/fontbakery)'s quality assurance tests.
* `make proof` will generate HTML proof files.

## License

This Font Software is licensed under the SIL Open Font License, Version 1.1.
This license is copied below, and is also available with a FAQ at
http://scripts.sil.org/OFL

## Repository Layout

This font repository structure is inspired by [Unified Font Repository v0.3](https://github.com/unified-font-repository/Unified-Font-Repository), modified for the Google Fonts workflow.


<br/>

---

## ChangeLog
When you make modifications, be sure to add a description of your changes, following the format of the other entries, to the start of this section.

**23 May 2018 (Mike LaGattuta) ‘Hepta Slab’ v0.016**
* Added more kerning pairs

**14 May 2018 (Mike LaGattuta) ‘Hepta Slab’ v0.014**
* Added T_h c_h c_t and s_t  discretionary ligatures
* Wrote script to fix metrics keys on 2nd Master. (Sidebearings are currently wrong based on non-interpolated metrics keys)

**9 May 2018 (Mike LaGattuta) ‘Hepta Slab’ v0.013**
* Converted 3rd instance (ExtraLight) to Master for necessary corrections
* Pinching corrections

**4 May 2018 (Mike LaGattuta) ‘Hepta Slab’ v0.009**
* Added stylistic alternates for 1, 2, and 7
* Revised instance weights

**19 April 2018 (Mike LaGattuta) ‘Hepta Slab’ v0.007**
* Updated smallcaps height
* Changed oldstyle figures to half-ranging figures

**27 March 2018 (Mike LaGattuta) ‘Hepta Slab’ v0.006**
* Fixed @ symbol proportions
* Fixed ampersand counters
* General spacing improvements

## Acknowledgements
If you make modifications, be sure to add your name (N), 
email (E), web-address (if you have one) (W) and 
description (D). This list is in alphabetical order according to last names.

N: Mike LaGattuta
E: mjlagattuta@gmail.com
W: https://michaellagattuta.com/
D: Designer

