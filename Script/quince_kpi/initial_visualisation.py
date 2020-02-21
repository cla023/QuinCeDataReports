###############################################################################
###                                                                         ###
###############################################################################

### Description:
#

#------------------------------------------------------------------------------
#import pandas as pd
import matplotlib.pyplot as plt
import os
import string


# Function plots parameter(s) vs time and saves plot(s) in output directory
def plot_data(colnames, df, output_dir, cleaned=False):

	# Get number of columns to plot
	ncol=len(colnames)

	if ncol==1:

		# Remove rows with NaNs
		df = df.dropna(subset=[colnames[0]])

		# Identify the parameters QC flag columns
		color_column = colnames[0] + ' QC Flag'

		# Set up the plot
		fig, ax = plt.subplots(figsize= (9,3*ncol))

		# If cleaned is false, plot all data. Else, plot data with QC flag 2.
		if cleaned is False:
			# Set plot color for the QC flags, and add to plot in a loop
			color_code = {2:'green',3:'orange',4:'red'}
			for flag, col in color_code.items():
				limited_df = df[df[color_column]==flag]
				ax.scatter(x=limited_df['Date/Time'], y=limited_df[colnames[0]],
					c=col, label=flag, alpha=0.7, edgecolors='none', marker='.')
				ax.legend(fontsize=9, bbox_to_anchor=(1, 1))
		else:
			limited_df = df[df[color_column]==2]
			ax.scatter(x=limited_df['Date/Time'], y=limited_df[colnames[0]],
				c='green', alpha=0.7, edgecolors='none', marker='.')

		# Add axis labels and grid
		plt.ylabel(colnames[0], fontsize=10)
		fig.autofmt_xdate()
		ax.grid(True)

	else:
		# List of letters used for labelling the plots
		letters=list(string.ascii_lowercase[0:ncol])

		# Setup the plot, and make subplots in a loop
		fig, ax = plt.subplots(len(colnames), sharex=True, figsize= (9,3*ncol))
		count = 0
		for colname in colnames:

			# Remove rows with NaNs
			df = df.dropna(subset=[colname])

			# Identify the parameters QC flag columns and set the color code
			color_column = colname + ' QC Flag'

			# If cleaned is false, plot all data. Else, plot data with QC flag 2.
			if cleaned is False:
				# Set plot color for the QC flags, and add to plot in a loop
				color_code = {2:'green',3:'orange',4:'red'}
				for flag, col in color_code.items():
					limited_df = df[df[color_column]==flag]
					ax[count].scatter(x=limited_df['Date/Time'], y=limited_df[colname],
						c=col, label=flag, alpha=0.7, edgecolors='none', marker='.')
				if count == 0:
					ax[count].legend(fontsize=9, bbox_to_anchor=(1, 1))
			else:
				limited_df = df[df[color_column]==2]
				ax[count].scatter(x=limited_df['Date/Time'], y=limited_df[colname],
					c='green', alpha=0.7, edgecolors='none', marker='.')

			# Add y-axis label, grid and lettering
			ax[count].set_ylabel(colname, fontsize=10)
			ax[count].grid(True)
			if len(colnames) > 1:
				ax[count].set_title(letters[count] + ')', loc='left', fontsize=10,
					fontweight="bold")

			count += 1

		# Add x-axis sideways
		fig.autofmt_xdate()


	#----------------------
	# Save plot to file
	if cleaned is True:
		filename = 'kpi_plot_data_cleaned.png'
	else:
		filename = 'kpi_plot_data.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')

	return filename