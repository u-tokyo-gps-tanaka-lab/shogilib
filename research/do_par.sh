#!/bin/bash

for f in x*;
do
    pypy3 check_reach.py -p --file $f 2>&1 > logs/${f}.log &
done
