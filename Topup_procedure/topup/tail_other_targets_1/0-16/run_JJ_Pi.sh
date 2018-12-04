#! /bin/bash

for JJ in $(seq 0 2 16)
do
	for Pi in 0 1
	do
		cd create_mesh_1
		rm bound_levels_0
		ln -s ../bound_levels_0/${JJ}_${Pi}_neg bound_levels_0
		./run.sh
		python creat_fine_mesh_5.py ${JJ} ${Pi}

		cd ../generate_PI_2/
		python fe18_n4.py
		
		if [ -d xsectn_${JJ}_${Pi} ]
		then
			rm -rf xsectn_${JJ}_${Pi}
		fi

		mv xsectn xsectn_${JJ}_${Pi}/
		
		cd ..
	done
done

