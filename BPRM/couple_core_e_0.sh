#!/bin/bash

#This script is to find the possible L_2S+1_P terms of an ion when the core and the
#interacting electron are coupled.

#First let's specify the parity for each configuration
#**Notice, the first element is just a space-holder so that the useful data start with
#index of 1 (CF starts with 1)
maxpw=9 #max angular momentum of partial wave
parity_core=('SPACE_HOLDER' 1 0 0 1 0 1 0 1 0 1 0 0 1 0 1 0 1)

#Then let's specify the ssout file and the starting and ending line of the energy table,
#where we will read the SLP terms of the core
ssout=fe18_ss.en
line_begin=1
line_end=99

#Create a directory where we will store the empty files named with the resulted SLP of the
#ion.
out_put=L_2S1_P
if [ -d ${out_put} ]
then
	rm -rf ${out_put}
fi
mkdir ${out_put}

#Now it's time to loop over the lines, read 2*S+1_L_P and coupled to the interacting 
#electron with orbitals ranging from 0 to ${maxpw}
l_max=0	#find out the maximum value of L
s_max=0	#find out the maximum value of S

for i in $(seq ${line_begin} ${line_end})
do
	line=( $(sed -n ${i}p ${ssout}) )
	
	S_CORE=${line[3]}
	S_CORE=${S_CORE/-/}	#remove the negative sign in front of S value
	L_CORE=${line[4]}
	P_CORE=${parity_core[${line[5]}]}

	#Now it's time to couple the core term to the interacting electron which has orbitals
	#of 0-${maxpw}
	for l_e in $(seq 0 ${maxpw})
	do
		#calculate the total parity of the ion
		P_ION=$(( (P_CORE+l_e)%2 ))
		
		#calculate the total spin based on the core spin(1 or >1)
		if [ ${S_CORE} -eq 1 ]
		then
			S_ION=(2)
		elif [ ${S_CORE} -gt 1 ]
		then
			S_ION=( $((S_CORE-1)) $((S_CORE+1)) )
		else
			echo "S_ION is not valid, exiting"
			exit
		fi
		
		if [ ${s_max} -lt ${S_ION[${#S_ION[*]}-1]} ]
		then
			s_max=${S_ION[$(( ${#S_ION[*]}-1 ))]}
		fi
		
		#calculate the total orbital
		L_ION_MIN=$(( L_CORE-l_e ))
		L_ION_MIN=${L_ION_MIN/-/}	#remove the negative sign to get the absolute value
		
		L_ION_MAX=$(( L_CORE+l_e ))	#get the maximum value of the orbital
		
		if [ ${l_max} -lt ${L_ION_MAX} ]
		then
			l_max=${L_ION_MAX}
		fi
		
		#now it's time to record the possible SLP terms.
		for S in ${S_ION[*]}
		do
			for L in $(seq ${L_ION_MIN} ${L_ION_MAX})
			do
				if [ ! -f ${out_put}/${L}_${S}_${P_ION} ]
				then	
					touch ${out_put}/${L}_${S}_${P_ION}	#Now this LSP term is "written" in
														#in the directory.
				fi
			
			done
		done
		
		
	done
done

#So far we have finished calculating all the possible LSP terms, not it's ready to collect
#these terms by using ls command
outfile=core_e_lsp

if [ -f ${outfile} ]
then
	rm -f ${outfile}
fi
for s in $(seq ${s_max} -1 1)
do
	for l in $(seq 0 ${l_max})
	do
		if [ -f ${out_put}/${l}_${s}_0 ]
		then
			printf "%5s%5s%5s\n" ${l} ${s} 0 >> ${outfile}
		fi
		
		if [ -f ${out_put}/${l}_${s}_1 ]
		then
			printf "%5s%5s%5s\n" ${l} ${s} 1 >> ${outfile}
		fi
	done
done




