#!/bin/bash
def=$2
file="${def:-bullish5y}"
cat $file | sed -n "/# $1/,/^\$/p" | grep TWorth | awk '{print $5 / $2}' | awk 'BEGIN {a=0} {a += $1} END {print a / NR}'
cat $file | sed -n "/# $1/,/^\$/p" | grep Sharpe | cut -d' ' -f4 | awk 'BEGIN {a=0} {a += $1} END {print a / NR}'
cat $file | sed -n "/# $1/,/^\$/p" | grep Calmar | cut -d' ' -f3 | awk 'BEGIN {a=0} {a += $1} END {print a / NR}'
# cat $file | sed -n "/# $1/,/^\$/p" | grep Trade | cut -d' ' -f3 | awk 'BEGIN {a=0} {a += $1} END {print a / NR}'
