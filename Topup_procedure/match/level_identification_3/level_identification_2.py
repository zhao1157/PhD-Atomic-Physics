#This script is to output the level idenfication after being corrected.

#Set the directories of assorted levels, correct_match and FAC output file
bound_level_dir = '../bound_levels_0'
correct_match_dir = '../correct_match_n3'
fac_out_en = '../outfile/fe18a.en'
#Set the number of electrons of bound configuration
n_e_bound = 10
#Set the number of levels of each symmetry
level_JJ_Pi = {'0_0':18, '0_1':17, '2_0':40, '2_1':41, '4_0':45, '4_1': 45, '6_0': 39, '6_1': 40,
               '8_0': 32, '8_1': 33, '10_0': 21, '10_1': 26, '12_0': 15, '12_1': 16, '14_0': 9,
                '14_1': 9, '16_0': 4, '16_1': 4}
#level_JJ_Pi = {'0_0': 18, '0_1': 17, '2_0': 40, '2_1': 41, '4_0': 45, '4_1': 45, '6_0': 39, '6_1': 40, '8_0': 32,
#             '8_1': 33, '10_0': 24, '10_1': 26, '12_0': 16, '12_1': 17, '14_0': 10, '14_1': 10, '16_0': 7, '16_1': 4}

level = {}
#First read the fac energy file and store the bound levels
f_en = open(fac_out_en, 'r')
for i in range(6): f_en.readline()
n_blocks = int(f_en.readline().split()[2])
f_en.readline()
for block in range(n_blocks):
        f_en.readline()
        n_ele = int(f_en.readline().split()[2])
        n_lev = int(f_en.readline().split()[2])
        f_en.readline()
        if n_ele == n_e_bound:
                for i in range(n_lev):
                        line = f_en.readline()
                        level[line.split()[0]] = line
        else:
                for i in range(n_lev):
                        f_en.readline()

#end of readling fac energy file.

#Ready to process each symmetry
for JJ in range(0, 17, 2):
        for Pi in range(2):
                #read the levels before being corrected.
                raw_order = ['hold']
                for line in open(bound_level_dir+'/'+str(JJ)+'_'+str(Pi)+'_neg'):
                        raw_order.append(line.split()[0])
                #read the correct_match
                correct_match = {}
                for line in open(correct_match_dir+'/'+str(JJ)+'_'+str(Pi)):
                        correct_match[line.split()[0]] = int(line.split()[1]) #for index purpose.
                #correct raw_order and output
                f_write = open(str(JJ)+'_'+str(Pi)+'_line', 'w')
                for line_index in range(1, level_JJ_Pi[str(JJ)+'_'+str(Pi)]+1):
                        if str(line_index) in correct_match:
                                f_write.write(level[raw_order[correct_match[str(line_index)]]])
                        else:
                                f_write.write(level[raw_order[line_index]])
