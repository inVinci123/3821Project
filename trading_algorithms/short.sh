#!/bin/bash
cat bullish5y | sed -n "/# $1/,/^\$/p" | grep TWorth | awk '{print $5 / $2}' | awk 'BEGIN {a=0} {a += $1} END {print a / NR}'
cat bullish5y | sed -n "/# $1/,/^\$/p" | grep Sharpe | cut -d' ' -f4 | awk 'BEGIN {a=0} {a += $1} END {print a / NR}'
cat bullish5y | sed -n "/# $1/,/^\$/p" | grep Calmar | cut -d' ' -f3 | awk 'BEGIN {a=0} {a += $1} END {print a / NR}'
cat bullish5y | sed -n "/# $1/,/^\$/p" | grep Trade | cut -d' ' -f3 | awk 'BEGIN {a=0} {a += $1} END {print a / NR}'
