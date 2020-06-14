#!/bin/bash

export PYTHONHASHSEED=0
for py in *.py
do
    python $py || exit 1
done

for m in */Makefile
do
    d=$(dirname $m)
    pushd $d
    make test || exit 1
    make clean
    popd
done
echo "=== all examples OK ==="
