#!/bin/bash

python ../perfect_hash.py ../animals.txt | python ./py2dot.py -l | neato -Tps -Gstart=100 -o animals.ps
