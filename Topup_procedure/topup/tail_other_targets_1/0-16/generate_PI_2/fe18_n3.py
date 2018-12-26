from pfac import fac
import os

outfile_lev_b = 'outfile/fe18b.en'
outfile_lev_a = outfile_lev_b[:-4]+'a.en'

outfile_rr_b = 'outfile/fe18b.rr'
outfile_rr_a = outfile_rr_b[:-4]+'a.rr'

fac.MemENTable(outfile_lev_b)

os.system('if [ -d out ]; then rm -rf out; fi; mkdir out')
#This is to create the directory where the PI data are stored.
os.system('if [ -d xsectn ]; then rm -rf xsectn; fi; mkdir xsectn')

#f = open('../create_mesh_1/fine_mesh_bf', 'r')
#content = f.readlines()
#num_line = len(content)
#f.close()
#del(content)

num_line = int(os.popen('wc -l ../create_mesh_1/fine_mesh_bf').read().split()[0])

print ('num_line=', num_line)

f = open('../create_mesh_1/fine_mesh_bf', 'r')

for i in range(1, num_line+1) :
    line = f.readline()

    line_split = line.split()
    print line_split[0]

    for j in range(1, len(line_split)):
        line_split[j] = float(line_split[j])
   
#TotalPICross() consumes too much memory, so abandon it, and use my own summation algorithm. 
#    fac.TotalPICross(outfile_rr_b, 'xsectn/'+str(i)+'_temp', int(line_split[0]), line_split[1:])
#    #process the total xsectn
#    f_write = open('xsectn/'+str(i), 'w')
#    f_xsectn = open('xsectn/'+str(i)+'_temp')
#    f_xsectn.readline()
#    for line_xsectn in f_xsectn:
#        f_write.write('  {0:12.6E} {1:9.3E}\n'.format(float(line_xsectn.split()[0])/13.605693, float(line_xsectn.split()[1])*0.01))

#os.popen('rm -rf xsectn/*_temp')

#InterpCross() does not consume much memory, because it outputs the sub-results in a file and I do the summation myself.
    fac.InterpCross(outfile_rr_b, 'out/'+str(i)+'_temp', int(line_split[0]), -1,
            line_split[1:], 0)

    #run add algorithm to obtain the total PI cross section, and delete the temp file.
    add_command = ('os.system(' + '\'./add_awk.sh -v ind=' + str(i) + ' ' +
                    'time_read=1 ' + 'out/'+str(i)+'_temp ' +
                    'time_read=3 ' + 'out/'+str(i)+'_temp ' +
                    'time_read=4 ' +'../create_mesh_1/fine_mesh_bf\'' + ')')
    #print (add_command)
    eval(add_command)

    rm_command = ('os.system(' +    '\'rm ' +  'out/'+str(i)+'_temp\''    + ')')
    eval (rm_command)
