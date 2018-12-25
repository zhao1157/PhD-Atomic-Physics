#! /bin/bash

for JJ in $(seq 0 2 16)
do
        for Pi in 0 1
        do
                cd create_mesh_1
                rm bound_levels_0
                ln -s ../bound_levels_0/${JJ}_${Pi}_neg bound_levels_0
                ./run.sh

                cd ../generate_PI_2/
		if [ -d xsectn_${JJ}_${Pi} ]
                then
                        rm -rf xsectn_${JJ}_${Pi}
                fi
                python fe18_n3.py
                mv xsectn xsectn_${JJ}_${Pi}/

                cd ..
        done
done

