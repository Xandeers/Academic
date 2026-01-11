#!/bin/bash 

Noeud=$1
TYPE=$2
FICHIER=$3


if [ "$TYPE" = "udp" ]; then 
    type="cbr"
fi

if [ "$TYPE" = "tcp" ]; then 
    type="tcp"
fi 

awk -v node="$Noeud" -v type="$type" '
    $1 == "+" && $3 == node && $5 == type {
        print
    }
' "$FICHIER"