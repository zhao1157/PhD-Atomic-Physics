#! /bin/bash

num_line=$(wc -l fine_mesh_bf)
num_line=${num_line//\ fine_mesh_bf}
for i in $(seq 1 $((num_line/1000)))
do
        sed -n $((1+(i-1)*1000)),$((1000*i))p fine_mesh_bf > fine_mesh_bf_${i}
done

sed -n $((1000*i+1)),${num_line}p fine_mesh_bf > fine_mesh_bf_$((i+1))
