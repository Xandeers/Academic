#!/bin/bash 

Flux=$1
Src=$2

if [ "$Flux" == "0" ]; then 
    
    awk ' $6=="40" {
    print
    }' "$Src" | head -30
else

    awk -v flux="$Flux" ' $6=="40" && $8==flux{
    print
    }' "$Src" | head -30

fi 

#pour le flux soit 1 ou 2 ou 0 pour les deux 