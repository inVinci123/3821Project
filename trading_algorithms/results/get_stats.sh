#!/bin/bash
# $1: data file

for alg in 'GREEDY$' 'RAN' 'BEST' 'SIMP' 'EXP' 'RSI'
do
  ./get_algo_stats.sh $alg $1 > "$(echo $alg | grep -o '^..')"
done

./get_algo_stats.sh 'GREEDY (ALT)' $1 > ga
./get_algo_stats.sh 'BOLLINGER 1' $1 > b1
./get_algo_stats.sh 'BOLLINGER 2' $1 > b2
