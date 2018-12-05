#This script is to plot the tail and other targets contributions.

import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, AutoMinorLocator

from numpy import log10

def setup(ax, indx, num_cc, point_boundary):
	data_tail = [[], []]
	data_tail_targets = [[], []]
	data_targets = [[], []]
	
	for line in open(indx + '_tail'):
		data = line.split()
		data_tail[0].append(float(data[0]))
		data_tail[1].append(float(data[1]))
		
	for line in open(indx + '_tail_other_targets'):
		data = line.split()
		data_tail_targets[0].append(float(data[0]))
		data_tail_targets[1].append(float(data[1]))
	
	for line in open(indx + '_other_targets'):
		data = line.split()
		data_targets[0].append(float(data[0]))
		data_targets[1].append(float(data[1]))
	
	ax.semilogy(data_tail[0][:point_boundary], data_tail[1][:point_boundary], 'b', label = str(num_cc)+'CC BPRM')
	ax.semilogy(data_tail[0][point_boundary:], data_tail[1][point_boundary:], '-.g', label = 'Tail')
	
	ax.semilogy(data_targets[0], data_targets[1], 'k', label = 'Other cores')
	
	ax.semilogy(data_tail_targets[0], data_tail_targets[1], 'r', label = 'Total (including other cores)')
	
	ax.legend(prop = {'size':8})
	ax.set_xlim(0, 530)
	
	ax.yaxis.set_major_locator(LogLocator(base = 10, numticks = 6))
	ax.set_yticklabels(ax.get_yticks())
	labels = [str(int(log10(float(label.get_text())))) for label in ax.get_yticklabels()]
	ax.set_yticklabels(labels)
	ax.yaxis.set_minor_locator(LogLocator(base = 10, subs = (0.2, 0,4, 0.6, 0.8), numticks = 24))
	ax.xaxis.set_minor_locator(AutoMinorLocator(5))
	

#======= MAIN =========
if __name__ == '__main__':
	#================== Fe XVII ================
	fig_1, axes_1 = plt.subplots(2, 1, sharex = True)
	setup(axes_1[0], '4_1_10', 218, 36100)
	setup(axes_1[1], '6_1_10', 218, 36100)
	
	fig_1.text(.40, .88, '$2s^22p^5 4d\,(J=2)$', ha = 'left', va = 'top')
	fig_1.text(.40, .48, '$2s^22p^5 5g\,(J=3)$', ha = 'left', va = 'top')
	
	fig_1.text(0.07, 0.5, '$log_{10}^{\sigma_{PI}}\,(Mb)$', ha='center', va = 'center', rotation = 90)
	fig_1.text(0.5, 0.02, 'Photon Energy ($Ry$)', ha = 'center', va = 'center')
	
	fig_1.subplots_adjust(hspace = 0.00)
	
	#================= Fe XVIII ===============
	fig_2, axes_2 = plt.subplots(2, 1, sharex = True)
	
	setup(axes_2[0], '5_0_20', 276, 30100)
	setup(axes_2[1], '7_1_44', 276, 30100)
	
	fig_2.text(.40, .88, '$2s^22p^4 4d\,(J=5/2)$', ha = 'left', va = 'top')
	fig_2.text(.40, .48, '$2s^22p^4 6h\,(J=7/2)$', ha = 'left', va = 'top')
	
	fig_2.text(0.07, 0.5, '$log_{10}^{\sigma_{PI}}\,(Mb)$', ha='center', va = 'center', rotation = 90)
	fig_2.text(0.5, 0.02, 'Photon Energy ($Ry$)', ha = 'center', va = 'center')
	
	fig_2.subplots_adjust(hspace = 0.00)
	
	#======= correction ========
	#reset the yticklabels for the last plot because of the overlap between the labels.
	axes_2[1].set_yticks([1e-11, 1e-8, 1e-5, 1e-2, 1e1])
	axes_2[1].set_yticklabels(['-11', '-8', '-5', '-2', '1', '1'])
	#plt.tight_layout()
	#plt.show()
	
	fig_1.savefig('fe17_tail_other_targets.eps')
	fig_2.savefig('fe18_tail_other_targets.eps')

