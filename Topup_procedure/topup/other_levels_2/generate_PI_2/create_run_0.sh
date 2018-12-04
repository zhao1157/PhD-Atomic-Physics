#! /bin/bash

section=level
sub_section=$(ls ../create_mesh_1/fine_mesh_bf_* | wc -w)

for i in $(seq 1 ${sub_section})
do
        if [ -d run_${i} ]
        then
                rm -rf run_${i}/*
        else
                mkdir run_${i}
        fi

        cd run_${i}

        cat << eof > my_pbs
#PBS -l walltime=1:00:00
#PBS -l nodes=1:ppn=1:skylake,mem=4GB
#PBS -N fe17_run_${section}_${i}
#PBS -S /bin/bash
#PBS -j oe

cd \${PBS_O_WORKDIR}

#This is set the environment variable which is required by FAC.
PYTHONPATH=/home/zhao.1157/fac-master/lib64/python2.7/site-packages
export PYTHONPATH

mkdir \${TMPDIR}
cp ../../create_mesh_1/fine_mesh_bf_${i} \${TMPDIR}/fine_mesh_bf
cp ../{add_awk.sh,fe18_n4.py} \${TMPDIR}
cp -rf ../../outfile \${TMPDIR}

cd \${TMPDIR}
python fe18_n4.py $((1+1000*(i-1)))

mv xsectn \${PBS_O_WORKDIR}
eof
        qsub my_pbs
        sleep 0.5
        cd ..
done

