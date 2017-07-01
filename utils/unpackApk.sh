#!/bin/bash

cd utils
./aapt dump badging $1 | grep uses-permission | awk -F ':' '{gsub(/\047/, "", $2); print $2}'
cd -
