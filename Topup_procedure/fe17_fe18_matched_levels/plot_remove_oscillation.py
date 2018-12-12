#This script is used to plot the photoionization cross section data without the oscillation at the right end

import os

#============ INPUT ============
#set the number of points to be removed (oscillation at the right end)
points_reduce = 1000

num_levels = 112	#number of levels for this initial symmetry

#276 CC BPRM (n4)
num_head_line_60 = 57 
num_cc_60 = 276     #NUMBER OF TARGET STATES.
file_xsectn_60 = "XSECTN_n4"	#file containing the xsectn data


#===============================================================================
#================================ BLACK BOX ====================================
#===============================================================================
#Correct match
cort_match = {}
for line in open('correct_match_n4', 'r'):
	match = line.split()
	cort_match[match[0]] = match[1]

f_60 = open(file_xsectn_60, 'r')

os.popen('if [ -f total.ps ]; then rm -rf total.ps; fi')

for level in range(1, 1+num_levels):
	#process 60 CC BPRM file
	for line in range(num_head_line_60):
		f_60.readline()
	
	symmetry_level = f_60.readline().split()
	title_plot = symmetry_level[1]+"\_"+symmetry_level[2]+"\_"+symmetry_level[3]
	
	num_points = int(f_60.readline().split()[1])
	f_60.readline()
	
	f_data = open("rm_data_60", 'w')
	for line in range(num_points-points_reduce):
		f_data.write(f_60.readline())
		
	f_data.close()
	for line in range(points_reduce):
		f_60.readline()
	#set the corrected fac data file.
	fac_data = str(level) if not str(level) in cort_match else cort_match[str(level)]
	
	#Now data is extracted for this level, time to plot it
	gnuplot_content = "\
set terminal postscript color enhanced\n\
set out 'tem.ps'\n\
set title \'"+title_plot+"\'\n\
set logscale y\n\
set format y \"%T\"\n\
set ylabel 'log10(PI)'\n\
set xlabel 'Photon Energy (Ry)'\n\
plot 'rm_data_60' u 1:2 title '200 CC BPRM' with lines lc rgb 'black',\\\n\
     'fac_background/"+fac_data+"' u 1:2 title 'FAC' with points lc rgb 'red' pt 3 ps 0.5 \n\
"
	f_gnuplot = open('plot.plt', 'w')
	f_gnuplot.write(gnuplot_content)
	f_gnuplot.close()
	
	
	os.popen('gnuplot plot.plt && cat tem.ps >> total.ps')
	
os.popen('sleep 5 && open total.ps')	
