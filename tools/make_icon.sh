#!/bin/bash

BAS=256

let "FS=BAS/5"
let "FSS=BAS*6/55"
let "TS=BAS/6"
let "SP=BAS/32"
let "OF=BAS/3"

convert -background blue -fill white \
          -font "Roboto-Bold" -pointsize $FS label:"PODA TV" \
          -trim \
          icon-1.png

convert -background blue -fill grey \
          -font "Roboto-Bold" -pointsize $FSS label:'poda.cz' \
          -trim \
          icon-2.png

L1Y=$(( $(identify -format '%h' icon-2.png) / 2 + ${SP} ))
L2X=$(( (${BAS} - $(identify -format '%w' icon-1.png)) / 2 ))
L2Y=$(( $(identify -format '%h' icon-1.png) / 2 + ${SP} ))

convert -size ${BAS}x${BAS} xc:blue -gravity Center \
        icon-1.png -geometry +0-${L1Y} -composite \
        -gravity East \
        icon-2.png -geometry +${L2X}+${L2Y} -composite \
        ../plugin.video.poda/icon.png

rm icon-1.png icon-2.png
