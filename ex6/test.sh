#!/bin/sh
for i in `seq 1 6`;
do
echo "1
$i
wav Samples\batman_theme_x.wav" | python ./ex6.py
done


echo "1
2
wav Samples\batman_theme_x.wav" | python ./ex6.py
