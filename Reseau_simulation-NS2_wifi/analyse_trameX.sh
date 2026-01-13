#!/bin/bash 

Flux=$1
Nb=$2
Src=$3

awk -v nb="$Nb" -v flux="$Flux" '
$1=="+" && $5=="tcp" && $8==flux && $11==nb {
    print
}' "$Src"


#si on veut les ack on enleve $5 =TCP