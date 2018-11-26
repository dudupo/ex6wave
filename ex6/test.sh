#!/bin/sh
# for i in `seq 1 6`;
# do
# echo "1
# $i
# wav Samples\batman_theme_x.wav" | python ./ex6.py
# done

echo "1
4
wav Samples\batman_theme_x.wav
1
test.wav
1
4
test.wav
1
test2.wav
4" | python ./ex6.py

echo "1
4
wav Samples\batman_theme_x.wav
2
1
4
1
test.wav
4" | python ./ex6.py
