#use python 2.x
import os

#specify the increment of the z-scaled energy and the number of points in each region
range_energy = "range_1"
start = -0.01 
incremet = (0.01+92.0/18/18)/30000	
#start = -0.01+incremet*500*46
num_pts = 50            #number of points in each region
#num_region = os.popen('ls error').read().split()
num_region = 600
#num_region = 45+260+1   #number of regions to be divided.
#recomp = [68, 69, 70, 71] #SET IN LOOP BELOW
b_symmetry = "0 11 0"    #initial symmetry which is ONLY one.
f_symmetry = "0 9 1\n0 11 1\n0 13 1"              #final symmetries which are at most 3.

#                           *********** BLACK BOX ***********
#                           ***********           ***********
#*************************** Dont' Touch the following code! ***********************************
#                           *********************************

#Extract the J, Pi values
J_PI=b_symmetry.split()

#Set the content of stgbf.inp file, which is the same for all the runs.
content_stgbf = "\
-1 0 0\n\
"+b_symmetry+ " 0 0\n\
"+f_symmetry+"\n\
-1 -1 -1\n\
"

#a directory to collect the error range
os.system('if [ -d error ]; then rm -rf error; fi; mkdir error;')
os.system('if [ -d success ]; then rm -rf success; fi; mkdir success;')
os.system('if [ -d XSECTN_35 ]; then rm -rf XSECTN_35; fi; mkdir XSECTN_35;')

#for i in range(300): 
#for i in range(310, 550):
for i in range(num_region):
#for i in [int(k) for k in num_region]:
	#if not i in recomp: continue
        print i
	BDH_FILE = "/fs/project/pradhan.1/zhao.1157/"+J_PI[1]+"_"+J_PI[2]
	scratch_folder = "/fs/project/pradhan.1/zhao.1157/"+J_PI[1]+"_"+J_PI[2]+"/"+range_energy+"/"+str(i)
	#========= 1 ========
	#Write the content of the PBS file.
	content_pbs = "\
#PBS -l walltime=72:00:00\n\
#PBS -l nodes=1:ppn=1,mem=13GB\n\
#PBS -N "+J_PI[1]+"_"+J_PI[2]+"_"+range_energy+"_"+str(i) + "\n\
#PBS -j oe\n\
#PBS -S /bin/bash\n\
\n\
module load intel/18.0.2 \n\
cd ${PBS_O_WORKDIR}/f_bf_" + str(i) +"\n\
mkdir ${TMPDIR}\n\
cp ../../../*x ${TMPDIR}\n\
cp *.inp ${TMPDIR}\n\
\n\
#cp "+BDH_FILE+"/H ${TMPDIR}; if [ $? != 0 ]; then exit; fi\n\
#for d_file in $(ls "+BDH_FILE+"/D??); do cp ${d_file} ${TMPDIR}; if [ $? != 0 ]; then exit; fi; done\n\
\n\
cd ${TMPDIR}\n\
ln -s "+BDH_FILE+"/H \n\
for d_file in $(ls "+BDH_FILE+"/D??); do ln -s ${d_file}; done\n\
./stgfjjx < stgf.inp \n\
flag1=$?\n\
echo flag1=$flag1;\n\
\n\
if [[ ${flag1} = 0 ]]; then f_file=$(ls F??); else touch ${PBS_O_WORKDIR}/error/" + str(i) + "; fi;\
for b in 1 2 3 4 5\n\
do\n\
for b_file in $(ls "+BDH_FILE+"/run_stgb/B??_${b}); do cp ${b_file} ${b_file:${#b_file}-5:3}; done\n\
if [ -f DVEC ]; then rm -f DVEC; fi; sleep 2;\n\
./prebfx < stgbf.inp; flag2=$?; \n\
echo flag2=$flag2;\n\
if [[ ${flag2} = 0 ]]; then ./rstgbfx < stgbf.inp; flag3=$?; else touch ${PBS_O_WORKDIR}/error/" + str(i) + "; exit; fi;\n\
echo flag3=$flag3;\n\
if [[ ${flag3} != 0 ]]; then touch ${PBS_O_WORKDIR}/error/" + str(i) + "; else \
touch ${PBS_O_WORKDIR}/success/" + str(i)+";\
mv XSECTN ${PBS_O_WORKDIR}/XSECTN_35/XSECTN_"+str(i)+"_${b}; fi; rm -rf B??;  done;\
cd ../; rm -rf ${TMPDIR}; if [[ ${flag3} = 0 ]]; then rm -rf ${PBS_O_WORKDIR}/f_bf_" + str(i) +"; fi;\n\
"

	#========== 2 =======
	#Write the content of stgf.inp file.
	content_stgf = "\
0 2 0 1200\n\
0.0001\n\
1\n\
1\n\
"+str(num_pts)+" "*3 + str(start+incremet*num_pts*(i-0)) +" "*3 + str(incremet) + "\n\
2\n\
"+f_symmetry+"\n\
"

	#========== 3 ==========
	#Create directory
	os.system('if [ -d f_bf_'+str(i)+' ]; then rm -rf f_bf_'+str(i)+'; fi; mkdir f_bf_'\
			+str(i)+';')
	#Write to files
	f = open('f_bf_'+str(i)+'/my_pbs', 'w')
	f.write(content_pbs)
	f.close()
	
	f = open('f_bf_'+str(i)+'/stgf.inp', 'w')
	f.write(content_stgf)
	f.close()
	
	f = open('f_bf_'+str(i)+'/stgbf.inp', 'w')
	f.write(content_stgbf)
	f.close()
	
	#========== 4 ==========
	#Submit the job now
	os.system('qsub f_bf_' + str(i) + '/my_pbs; sleep .3')
	
