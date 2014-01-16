#!/bin/bash

CONFIG=`ifconfig $1 | grep 'inet addr'`

echo $CONFIG  | sed 's/\s\{2,\}/ /g' | cut -d ':' -f 2 | cut -d ' ' -f 1
echo $CONFIG  | sed 's/\s\{2,\}/ /g' | cut -d ':' -f 4