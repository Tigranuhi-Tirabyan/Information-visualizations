import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import matplotlib.gridspec as gridspec
import sqlite3
from scipy import stats


connection = sqlite3.connect('data_db.db')
c = connection.cursor()



# Setup figure and subplots
with plt.xkcd():
	fig = plt.figure(figsize=(12, 5))
	gs =  gridspec.GridSpec(nrows=2, ncols=4)
	ax1 = fig.add_subplot(gs[0, 0])
	ax2 = fig.add_subplot(gs[1, 0])
	ax3 = fig.add_subplot(gs[0, 1])
	ax4 = fig.add_subplot(gs[1, 1])
	ax5 = fig.add_subplot(gs[0:, 2:])
ax = [ax1, ax2, ax3, ax4, ax5]




def animate(i):
	query = ('SELECT * FROM dice_results')
	data = pd.read_sql_query(query, connection)
	data['dice_means'] = data[['value1', 'value2', 'value3', 'value4', 'value5', 'value6', 'value7']].mean(axis=1)
	for j in range(0, len(ax)):
		ax[j].cla()

		# Changing fontsize of labels and ticks
		for item in ([ax[j].xaxis.label, ax[j].yaxis.label] +ax[j].get_xticklabels() + ax[j].get_yticklabels()):item.set_fontsize(7)	

	# Set titles of subplots
	ax1.set_title("Distribution of means", size = 10, pad = 2)
	ax2.set_title("Normality test p-value",size = 10,pad = 2)
	ax4.set_title("Historical p-values",size = 10, pad = 2)
	ax5.set_title("Distribution of outputs",size = 10,pad = 2)

	# The histogram of means
	ax1.hist(data.dice_means, color ='darkblue', bins = 10, rwidth=0.9)
	trials = ax1.text(0.5,0.8, "",transform=ax1.transAxes, ha="center", color = "darkgray")
	trials.set_text("Number of trials = {}".format(str(data.Id.iloc[-1])))


	# QQ plot
	stats.probplot(data.dice_means, dist = "norm", plot=ax3)
	ax3.set_title("Probability Plot",size = 10,pad = 2)
	ax3.get_lines()[0].set_markersize(4.0)
	ax3.get_lines()[0].set_color('darkblue')
	ax3.get_lines()[1].set_color('darkred')
	ax3.xaxis.labelpad = 0.2
	ax3.yaxis.labelpad = 0.2



	# The results of the Shapiro-Wilk test
	shapiro_test_pvalue = stats.shapiro(data.dice_means).pvalue
	ax2.axis('off')
	txt = ax2.text(0.5,0.5, "",transform=ax2.transAxes, ha="center")
	txt.set_text("p-value: {}".format(str(round(shapiro_test_pvalue,4))))


	# Historical p-values
	for i in range(0,data.shape[0]-2):
		data.loc[data.index[i+2],'p_values'] = stats.shapiro(data.dice_means[:i+3]).pvalue
	ax4.plot(data.Id, data.p_values, color='darkblue')
	
	# The original distribution
	df = data[data.columns[1:8]].apply(pd.value_counts).sum(axis = 1)
	ax5.bar(df.index,df, color='darkblue', width = 0.98)



plt.tight_layout()
ani = FuncAnimation(plt.gcf(), animate, interval = 500, repeat = False)


plt.show()

