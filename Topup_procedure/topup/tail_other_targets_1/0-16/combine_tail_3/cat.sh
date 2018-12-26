#! /bin/bash

if [ -f ratio ]
then
	rm -rf ratio
fi

for JJ in $(seq 0 2 16)
do
	for Pi in 0 1
	do
		cat ${JJ}_${Pi}_ratio >> ratio

	done

done
