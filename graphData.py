import numpy as np
import matplotlib.pyplot as plt


testData = "only_ones"
title = "Alphabet size 1"

# testData = "random10_timings"
# title = "Alphabet size 10"



x_mccreight  = []
y_mccreight = []
mccreight_minmax = []
with open("testData/mccreight_" + testData, "rb") as fp:
	for line in fp.readlines():
		(n,t,_) = line.split(b", ")

		time = float(t.decode())
		if len(x_mccreight) > 0 and x_mccreight[-1] == float(n.decode()):
			y_mccreight[-1] = (y_mccreight[-1] + time)/2

			mccreight_minmax[-1] = (min(time, mccreight_minmax[-1][0]),max(time, mccreight_minmax[-1][1]))
			continue
		x_mccreight.append(float(n.decode()))
		y_mccreight.append(time)

		mccreight_minmax.append((time,time))

x_naive  = []	
y_naive = []
naive_minmax = []
with open("testData/naive_" + testData, "rb") as fp:
	for line in fp.readlines():
		(n,t,_) = line.split(b", ")
		time = float(t.decode())
		if len(x_naive) > 0 and  x_naive[-1] == float(n.decode()):
			y_naive[-1] = (y_naive[-1] + time)/2

			naive_minmax[-1] = (min(time, naive_minmax[-1][0]),max(time, naive_minmax[-1][1]))
			continue

		x_naive.append(float(n.decode()))
		y_naive.append(time)
		naive_minmax.append((time,time))


x_farach  = []	
y_farach = []
farach_minmax = []
with open("testData/farach_" + testData, "rb") as fp:
	for line in fp.readlines():
		(n,t,_) = line.split(b", ")
		time = float(t.decode())
		if len(x_farach) > 0 and  x_farach[-1] == float(n.decode()):
			y_farach[-1] = (y_farach[-1] + time)/2
			farach_minmax[-1] = (min(time, farach_minmax[-1][0]),max(time, farach_minmax[-1][1]))
			continue
		x_farach.append(float(n.decode()))
		y_farach.append(time)
		farach_minmax.append((time,time))

		
# fig = plt.figure(figsize=(9, 6))
# plt.scatter(x, y)
# plt.xlabel('length of string')
# plt.ylabel('time taken')
# # plt.yscale('log')
# plt.grid(True)

# fig.savefig('graphs/one_char/farach_different_char.png', bbox_inches='tight')


fig, ax = plt.subplots()
ax.set_title(title)
ax.set_xlabel("length of input")
ax.set_ylabel("construction time in seconds")
# plt.axis([500, 15000, 0, 0.002])
# ax.mccreight = plt.plot(x_mccreight,[x/y for x, y in zip(y_mccreight, x_mccreight)], label="mccreight")
# ax.naive = plt.plot(x_naive,[x/(y**2) for x, y in zip(y_naive, x_naive)], label="naive")
# ax.farach = plt.plot(x_farach,[x/y for x, y in zip(y_farach, x_farach)], label="farach")
# ax.mccreight = plt.plot(x_mccreight,y_mccreight, label="mccreight")

ax.farach = plt.plot(x_farach,y_farach, label="farach")
# ax.naive = plt.plot(x_naive,y_naive, label="naive")

# for x in range(len(x_mccreight)):

# 	plt.plot((x_mccreight[x], x_mccreight[x]), (mccreight_minmax[x][0], mccreight_minmax[x][1]), 'k-')

# 	plt.plot((x_mccreight[x], x_mccreight[x]), (mccreight_minmax[x][0]/x_mccreight[x], mccreight_minmax[x][1]/x_mccreight[x]), 'k-')

#FILL
# l1, l2 = zip(*farach_minmax)
# ax.fill_between(x_farach, l1, l2, hatch="******", color="orange", linewidth=0.0, alpha=0.5)

# for x in range(len(x_farach)):
# 	# plt.plot((x_farach[x], x_farach[x]), (farach_minmax[x][0], farach_minmax[x][1]), 'k-')

# 	plt.plot((x_farach[x], x_farach[x]), (farach_minmax[x][0]/float(x_farach[x]), farach_minmax[x][1]/float(x_farach[x])), 'k-')
# for x in range(len(x_naive)):
# 	# plt.plot((x_naive[x], x_naive[x]), (naive_minmax[x][0], naive_minmax[x][1]), 'k-')
# 	# plt.plot((x_naive[x], x_naive[x]), (naive_minmax[x][0]/x_naive[x], naive_minmax[x][1]/x_naive[x]), 'k-')
# 	plt.plot((x_naive[x], x_naive[x]), (naive_minmax[x][0]/(x_naive[x]**2), naive_minmax[x][1]/(x_naive[x]**2)), 'k-')


#ax.set_title('Vert. symmetric')


legend = ax.legend(loc='upper left', shadow=True)

frame = legend.get_frame()
frame.set_facecolor('0.90')


for label in legend.get_texts():
    label.set_fontsize('large')

for label in legend.get_lines():
     label.set_linewidth(1.5)  # the legend line width


plt.show()
