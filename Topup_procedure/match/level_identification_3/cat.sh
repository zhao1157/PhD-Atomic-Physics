#! /bin/bash

if [ -f total_line ]
then
        rm -rf total_line
fi

for JJ in $(seq 0 2 16)
do
	for Pi in 0 1
	do
		cat ${JJ}_${Pi}_line >> total_line 

	done

done
