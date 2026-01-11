#!/bin/bash

PaquetX=$1
SRC=$2

sed -n "/ $PaquetX\$/p" < "$SRC"