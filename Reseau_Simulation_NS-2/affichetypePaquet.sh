#!/bin/bash 

TYPE=$1
SRC=$2

if [ "$TYPE" == "udp" ]; then 
    type="cbr"
fi

if [ "$TYPE" == "tcp" ]; then 
    type="tcp"
fi

awk "/$type/" $SRC