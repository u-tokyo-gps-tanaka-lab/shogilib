#!/bin/bash

for f in x*;
do
    python reach_partial.py $f 2>&1 > logs/${f}.log &
done