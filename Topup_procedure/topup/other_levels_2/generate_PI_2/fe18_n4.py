from pfac import fac
import sys
import os

outfile_lev_b = 'outfile/fe18b.en'
outfile_lev_a = outfile_lev_b[:-4]+'a.en'

outfile_rr_b = 'outfile/fe18b.rr'
outfile_rr_a = outfile_rr_b[:-4]+'a.rr'

fac.MemENTable(outfile_lev_b)

#****************************generate_PI_2************************************
os.system('if [ -d out ]; then rm -rf out; fi; mkdir out')
#This is to create the directory where the PI data are stored.
os.system('if [ -d xsectn ]; then rm -rf xsectn; fi; mkdir xsectn')

num_line = int(os.popen('wc -l fine_mesh_bf').read().split()[0])

print ('num_line=', num_line)

f = open('fine_mesh_bf', 'r')

for i in range(int(sys.argv[1]), num_line+int(sys.argv[1])) :
        line = f.readline()

        line_split = line.split()
        print line_split[0]

        for j in range(1, len(line_split)):
                line_split[j] = float(line_split[j])

        fac.InterpCross(outfile_rr_b, 'out/'+str(i)+'_temp', int(line_split[0]), -1, line_split[1:], 0)

        #run add algorithm to obtain the total PI cross section, and delete the temp file.
        inde = i - int(sys.argv[1]) + 1  #inde is the line number the mesh file.
        add_command = ('os.system(' + '\'./add_awk.sh -v ind=' + str(inde) + ' ' +
                        'time_read=1 ' + 'out/'+str(i)+'_temp ' +
                        'time_read=3 ' + 'out/'+str(i)+'_temp ' +
                        'time_read=4 ' +'fine_mesh_bf\'' + ')')
        #print (add_command)
        eval(add_command)

        rm_command = ('os.system(' +    '\'rm ' +  'out/'+str(i)+'_temp\''    + ')')
        eval (rm_command)
        os.system('mv xsectn/'+str(inde)+' xsectn/'+str(i))
