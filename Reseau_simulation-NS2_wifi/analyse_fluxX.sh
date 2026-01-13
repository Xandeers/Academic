#!/bin/bash     

Flux=$1
Src=$2

awk -v flux="$Flux" ' $8==flux{
print 
}' $Src 