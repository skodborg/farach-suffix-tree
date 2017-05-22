import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as patches
import math


title = 'alphabet dependence'
xlabel = 'length of input'
ylabel = 'construction time in seconds'
outputimgfile = 'alph_dependence.png'

def plot(filename, label, color, marker='o'):
	global ax
	x  = []
	y = []
	minmax = []
	temp = []
	temp_x = 0
	with open(filename, "rb") as fp:
		for line in fp.readlines():

			tup = line.split(b",")
			x_n = float(tup[0].decode())
			time = float(tup[1].decode())
			if x_n == temp_x:
				temp.append(time)
				
				minmax[-1] = (min(time, minmax[-1][0]),max(time, minmax[-1][1]))
				continue
			if temp_x != 0:
				temp.sort()
				y.append(temp[int(len(temp)/2)])
				temp = []

			temp_x = x_n
			temp.append(time)
			x.append(x_n)
			minmax.append((time,time))
	temp.sort()
	y.append(temp[int(len(temp)/2)])

	plt.plot(x,y, marker=marker, markersize=6, color=color, label=label)
	# plt.plot(x,[y/x for y,x in zip(x,y)], marker='o', markersize=3, label=label)
	l1, l2 = zip(*minmax)
	# ax.fill_between(x, [y/x for x,y in zip(x, l1)], [y/x for x,y in zip(x, l2)], hatch="////", color="#55AA55", linewidth=0.0, alpha=0.5)
	ax.fill_between(x, l1, l2, hatch="////", color=color, linewidth=0.0, alpha=0.2)

# plt.yscale('log')
# plt.grid(True)



fig, ax = plt.subplots()

# ALPHABET DEPENDENCE
markers = ['.', 'x', '|', 'v']
for i, i_pow in enumerate(range(14, 18)):
	plot("testData/alph_dependence_mbp_"+str(i_pow) + "_farach_random_data_varying_alphabet", "farach $|\Sigma|=2^{" + str(i_pow)+'}$', "green", markers[i])
	plot("testData/alph_dependence_mbp_"+str(i_pow) + "_mccreight_random_data_varying_alphabet", "mcc $|\Sigma|=2^{"+str(i_pow)+'}$', "red", markers[i])
	# plot("testData/zoom_alph_dependence_mbp_"+str(i_pow) + "_farach_random_data_varying_alphabet", "farach $|\Sigma|=2^{" + str(i_pow)+'}$', "green", markers[i])
	# plot("testData/zoom_alph_dependence_mbp_"+str(i_pow) + "_mccreight_random_data_varying_alphabet", "mcc $|\Sigma|=2^{"+str(i_pow)+'}$', "red", markers[i])

# ZOOMED EFFECT - DASHED RECTANGLE
ax.add_patch(patches.Rectangle(
        (5000.0, 1.0), 100000.0, 25.6, fill='blue', alpha=0.2))
ax.add_patch(patches.Rectangle(
        (5000.0, 1.0), 100000.0, 25.6, fill=False, linestyle='dashed'))


# # PERIODICITY
# # FARACH
# plot('testData/periodic_abcdefghij_farach_mbp_helper', 'farach 10', 'green')
# plot('testData/periodic_2len1000_mbp_farach_helper', 'farach 1000', 'green')
# plot('testData/periodic_len5000_mbp_farach_helper', 'farach 5000', 'green')
# plot('testData/periodic_len10000_mbp_farach_helper', 'farach 10t', 'green')
# plot('testData/periodic_len25000_mbp_farach_helper', 'farach 25t', 'green')  # CAN WE TRUST THIS? RUN AT A DIFFERENT TIME
# plot('testData/diff_char_50t_mbp_farach_different_char', 'farach different chars', 'orange')
# # MCC
# plot('testData/periodic_abcdefghij_mccreight_mbp_helper', 'mccreight 10', 'red')
# plot('testData/periodic_len5000_mbp_mccreight_helper', 'mccreight 5000', 'red')
# plot('testData/periodic_2len1000_mbp_mccreight_helper', 'mccreight 1000', 'red')
# plot('testData/periodic_len25000_mbp_mccreight_helper', 'mccreight 25t', 'red')  # CAN WE TRUST THIS? RUN AT A DIFFERENT TIME
# # NAIVE
# plot('testData/periodic_abcdefghij_naive_mbp_helper', 'naive 10', 'blue')
# plot('testData/periodic_len1000_naive_mbp_helper', 'naive 1000', 'blue')


# BRCA1
# plot('testData/brca_mbp_farach_dna_prefixes', 'farach', 'blue')
# plot('testData/brca_mbp_mccreight_dna_prefixes', 'mccreight', 'green')
# plot('testData/brca_mbp_naive_dna_prefixes', 'naive', 'orange')

# CHROMOSOME 2
# plot('testData/chromosome2_mbp_farach_dna_prefixes', 'farach', 'blue')
# plot('testData/chromosome2_mbp_mccreight_dna_prefixes', 'mccreight', 'green')
# plot('testData/chromosome2_mbp_naive_dna_prefixes', 'naive', 'orange')


ax.set_title(title)
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
ax.grid(True)
# ax.axis([0.0,110000.0,-2.0,27.0])


# CUSTOM LEGEND
farach_line = mlines.Line2D([], [], color='green', label='Farach')
mcc_line = mlines.Line2D([], [], color='red', label='McCreight')
alph_2_14 = mlines.Line2D([], [], marker=markers[0], label='$|\Sigma|=2^{14}$')
alph_2_15 = mlines.Line2D([], [], marker=markers[1], label='$|\Sigma|=2^{15}$')
alph_2_16 = mlines.Line2D([], [], marker=markers[2], label='$|\Sigma|=2^{16}$')
alph_2_17 = mlines.Line2D([], [], marker=markers[3], label='$|\Sigma|=2^{17}$')
handles = [farach_line, mcc_line, alph_2_14, alph_2_15, alph_2_16, alph_2_17]
legend = ax.legend(loc='upper left', shadow=True, handles=handles)


frame = legend.get_frame()
frame.set_facecolor('0.90')


for label in legend.get_texts():
    label.set_fontsize('large')

for label in legend.get_lines():
     label.set_linewidth(1.5)  # the legend line width


fig.savefig(outputimgfile, bbox_inches='tight')
