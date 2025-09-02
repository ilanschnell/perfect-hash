#!/bin/bash

python ../perfect_hash.py ../animals.txt --hft=2 | python ./py2dot.py -l | neato -Tpng -Gstart=100 -o animals.png
