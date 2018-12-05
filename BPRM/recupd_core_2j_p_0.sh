#!/bin/bash

#First let's specify the parity for each configuration
#**Notice, the first element is just a space-holder so that the useful data start with
#index of 1 (CF starts with 1)
parity_core=('SPACE_HOLDER' 1 0 0 1 0 1 0 1 0 1 0 0 1 0 1 0 1)

#Then let's specify the ssout file and the starting and ending line of the energy table,
#where we will read the SLP terms of the core
ssout=fs.en
#recupd_org=recupd.inp.org
line_begin=1
line_end=218

#specify the output file name, make sure it does not pre-exist.
outfile=recupd.inp
if [ -f ${outfile} ]
then
	rm ${outfile}
fi

#Now it's time to loop over the lines, read 2*j and CF
for i in $(seq ${line_begin} ${line_end})
do
	line=( $(sed -n ${i}p ${ssout}) )
	
	TWOJ_CORE[${i}]=${line[5]}
	P_CORE[${i}]=${parity_core[${line[6]}]}
done

for i in $(seq ${line_begin} ${line_end})
do
	printf "%3d" ${TWOJ_CORE[${i}]} >> ${outfile}
done 

printf '\n' >> ${outfile}

for i in $(seq ${line_begin} ${line_end})
do
	printf "%3d" ${P_CORE[${i}]} >> ${outfile}
done 

printf '\n' >> ${outfile}
