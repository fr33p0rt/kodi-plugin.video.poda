#!/bin/bash

SRC="https://images.pexels.com/photos/3768898/pexels-photo-3768898.jpeg?crop=entropy&cs=srgb&dl=pexels-andrea-piacquadio-3768898.jpg&fit=crop&fm=jpg&h=3990&w=5985"

BRO="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"

#WID=1920
#SIZ=${WID}x1080

WID=1280
SIZ=${WID}x720

wget -U "${BRO}" "${SRC}" -O fanart-src.jpg

convert fanart-src.jpg -quality 70 -resize ${WID}x -thumbnail ${WID}x -gravity South -crop ${SIZ}+0+0 ../plugin.video.poda/fanart.jpg

rm fanart-src.jpg
