#!/bin/bash 

TYPE=$1
PaquetNumber=$2
SRC=$3

if [ "$TYPE" == "udp" ]; then 
    type="cbr"
fi

if [ "$TYPE" == "tcp" ]; then 
    type="tcp"
fi

awk "/$type/ && / $PaquetNumber /" $SRC