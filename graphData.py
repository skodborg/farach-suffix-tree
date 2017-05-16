import numpy as np
import matplotlib.pyplot as plt


testData = "mbp_only_ones"
title = "Alphabet size 1"

# testData = "random_data"
# title = "Alphabet size 10"

# testData = "random10_timings"
# title = "Alphabet size 10"



x_mccreight  = []
y_mccreight = []
mccreight_minmax = []
temp = []
temp_x = 0
with open("testData/mccreight_" + testData, "rb") as fp:
	for line in fp.readlines():
		(n,t,_) = line.split(b", ")
		x = float(n.decode())
		time = float(t.decode())
		if x == temp_x:
			temp.append(time)
			
			mccreight_minmax[-1] = (min(time, mccreight_minmax[-1][0]),max(time, mccreight_minmax[-1][1]))
			continue
		if temp_x != 0:
			temp.sort()
			y_mccreight.append(temp[2])
			temp = []

		temp_x = x
		temp.append(time)
		x_mccreight.append(x)
		mccreight_minmax.append((time,time))
temp.sort()
y_mccreight.append(temp[2])


x_naive  = []
y_naive = []
naive_minmax = []
temp = []
temp_x = 0
with open("testData/naive_" + testData, "rb") as fp:
	for line in fp.readlines():
		(n,t,_) = line.split(b", ")
		x = float(n.decode())
		time = float(t.decode())
		if x == temp_x:
			temp.append(time)
			
			naive_minmax[-1] = (min(time, naive_minmax[-1][0]),max(time, naive_minmax[-1][1]))
			continue
		if temp_x != 0:
			temp.sort()

			y_naive.append(temp[2])

		temp_x = x
		temp = []
		temp.append(time)
		x_naive.append(x)
		naive_minmax.append((time,time))
temp.sort()
y_naive.append(temp[2])


x_farach  = []
y_farach = []
farach_minmax = []
temp = []
temp_x = 0
with open("testData/farach_" + testData, "rb") as fp:
	for line in fp.readlines():
		(n,t,_) = line.split(b", ")
		x = float(n.decode())
		time = float(t.decode())
		if x == temp_x:
			temp.append(time)
			
			farach_minmax[-1] = (min(time, farach_minmax[-1][0]),max(time, farach_minmax[-1][1]))
			continue
		if temp_x != 0:
			temp.sort()
			y_farach.append(temp[2])

		temp_x = x
		temp = []
		temp.append(time)
		x_farach.append(x)
		farach_minmax.append((time,time))
temp.sort()
y_farach.append(temp[2])

		
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
# y_farach = y_farach[1:]
# x_farach = x_farach[1:]
# y_naive = y_naive[1:]
# x_naive = x_naive[1:]
# y_mccreight = y_mccreight[1:]
# x_mccreight = x_mccreight[1:]

# ax.farach = plt.plot(x_farach,[x/y for x, y in zip(y_farach, x_farach)], label="farach")
# ax.naive = plt.plot(x_naive,[y/(x**2) for y, x in zip(y_naive, x_naive)], label="naive")
# ax.mccreight = plt.plot(x_mccreight,[x/y for x, y in zip(y_mccreight, x_mccreight)], label="mccreight")


# ax.mccreight = plt.plot(x_mccreight,y_mccreight, label="mccreight")

ax.farach = plt.plot(x_farach,y_farach, marker='o', markersize=3, label="farach")
ax.naive = plt.plot(x_naive,y_naive, marker='o', markersize=3, label="naive")
ax.mccreight = plt.plot(x_mccreight,y_mccreight, marker='o', markersize=3, label="mccreight")

# for x in range(len(x_mccreight)):

# 	plt.plot((x_mccreight[x], x_mccreight[x]), (mccreight_minmax[x][0], mccreight_minmax[x][1]), 'k-')

# 	plt.plot((x_mccreight[x], x_mccreight[x]), (mccreight_minmax[x][0]/x_mccreight[x], mccreight_minmax[x][1]/x_mccreight[x]), 'k-')

#FILL


l1, l2 = zip(*farach_minmax)
ax.fill_between(x_farach, l1, l2, hatch="////", color="#4A6B8A", linewidth=0.0, alpha=0.5)
# ax.fill_between(x_farach, [y/x for x,y in zip(x_farach, l1)], [y/x for x,y in zip(x_farach, l2)], hatch="////", color="#4A6B8A", linewidth=0.0, alpha=0.5)

l1, l2 = zip(*naive_minmax)
ax.fill_between(x_naive, l1, l2, hatch="////", color="orange", linewidth=0.0, alpha=0.5)
# ax.fill_between(x_naive, [y/x**2 for x,y in zip(x_naive, l1)], [y/x**2 for x,y in zip(x_naive, l2)], hatch="////", color="orange", linewidth=0.0, alpha=0.5)

l1, l2 = zip(*mccreight_minmax)
# ax.fill_between(x_mccreight, [y/x for x,y in zip(x_mccreight, l1)], [y/x for x,y in zip(x_mccreight, l2)], hatch="////", color="#55AA55", linewidth=0.0, alpha=0.5)


ax.fill_between(x_mccreight, l1, l2, hatch="////", color="#55AA55", linewidth=0.0, alpha=0.5)

# for x in range(len(x_farach)):
# 	# plt.plot((x_farach[x], x_farach[x]), (farach_minmax[x][0], farach_minmax[x][1]), 'k-')

# 	plt.plot((x_farach[x], x_farach[x]), (farach_minmax[x][0]/float(x_farach[x]), farach_minmax[x][1]/float(x_farach[x])), 'k-')
# for x in range(len(x_naive)):
# 	# plt.plot((x_naive[x], x_naive[x]), (naive_minmax[x][0], naive_minmax[x][1]), 'k-')
# 	# plt.plot((x_naive[x], x_naive[x]), (naive_minmax[x][0]/x_naive[x], naive_minmax[x][1]/x_naive[x]), 'k-')
# plt.plot((x_naive[x], x_naive[x]), (naive_minmax[x][0]/(x_naive[x]**2), naive_minmax[x][1]/(x_naive[x]**2)), 'k-')


#ax.set_title('Vert. symmetric')


legend = ax.legend(loc='upper left', shadow=True)

frame = legend.get_frame()
frame.set_facecolor('0.90')


for label in legend.get_texts():
    label.set_fontsize('large')

for label in legend.get_lines():
     label.set_linewidth(1.5)  # the legend line width

fig.savefig('fig1.png', bbox_inches='tight')
