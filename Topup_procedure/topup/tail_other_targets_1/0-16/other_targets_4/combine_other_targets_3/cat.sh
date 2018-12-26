#! /bin/bash

if [ -f BPRM_bprm_tail_other_targets ]
then
	rm -rf BPRM_bprm_tail_other_targets
fi

for JJ in $(seq 0 2 16)
do
	for Pi in 0 1
	do
		echo ${JJ}_${Pi}
		cat ${JJ}_${Pi}_bprm_tail_other_targets >> BPRM_bprm_tail_other_targets
	done

done
