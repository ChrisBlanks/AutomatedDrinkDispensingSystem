#!/bin/bash
# run i2c communication 

# $1 = how many times to run the script (e.g. 5)

# check to see if any arguments were passed in
if [ $# -eq 0  ]; then
  rep=3 #if no arguments ($1 = nothing), set to 3
else
  rep=$1 #make 1st arg the number of repetitions
fi

# run sequence the "rep" number of times
for i in $(seq $rep)
do
   python3 test.py #2>/dev/NULL 
  sleep 2
  echo $i
done
