#!/bin/bash 

PaquetX=$1
SRC=$2

awk "/^+/ && / $PaquetX\$/" $SRC

