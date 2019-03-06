#	Authored: Max Pfeiffer - 2018
#
#	Takes a passed .csv file with a CAN or LIN log in the "Time, ID, Data" format 
# 	and plots the data for the target ID over time. Entering specific byte indexes
# 	splits the data up into specific bytes, otherwise entering no additional argument
#	simly plots the entire message packet.  
#	
#	plotlin takes the data for the target ID and produces plots of each byte, with the 
#	byte number on the y-axis label.
#
#	Usage: 	python plotlin.py example_log.csv ex_id 1 2 3
#		where example log is the data to be plotted 
#		filtered by ex_id, so only this id is filtered 
#		the following numbers indicate byte fields we wish to preserve or plot. 
#
#!/usr/bin/python
import sys
import csv
import matplotlib.pyplot as plt 


filename = sys.argv[1]
filt_id = sys.argv[2]
filt_bytes =[]
for i in range(3, len(sys.argv)):
	filt_bytes.append(sys.argv[i])
plot_data = []
plot_x = []
plot_y = [[],[],[],[],[],[],[],[]]				# the y-plots for up to 8 data bytes 
bytes_present = 0 								# max number of bytes in the message set, used for plotting 

# takes a filter id and a filename, extracts the data for 
# that target ID into the plot_data structure 
def filter_by_id(filt_id, filename, plot_data):
	control = open(filename)
	og_data = csv.reader(control, delimiter=",");
	header = 1
	for row in og_data:
		if header:
			header = 0
		else: 
			pid = row.pop(1)
			if(pid == filt_id):
				time = row.pop(0)
				data = row.pop(0)
				print( "data = " + str(data))
				plot_data.append([time , data])
	control.close()	



# separates the byte data from ploy_data to plot_y, fills plot_x  
def filter_bytes(filt_bytes, plot_data, plot_y, plot_x, bytes_present):
	if(len(filt_bytes) > 0):
		for row in plot_data:
			row = list(row)							# for each row in the plot_y, extract and separate 
			plot_x.append(row.pop(0))				# get rid of the time 
			row = list(row.pop(0))			
			bytes_present = len(row) if len(row) > bytes_present else bytes_present 
			for i in range(0, len(plot_y)):	 				
				concat = row.pop(0) + row.pop(0) if len(row) > 0 else "00"
				plot_y[i].append(int(concat, 16)) 


# plots the passed x and y data if its in the filt_bytes list 
def plotlin(plot_x, plot_y, plot_data, filt_bytes):
	num_bytes = len(filt_bytes)
	plt.figure(1)

	if(num_bytes == 0):								# print from plot data 
		x_vals = []
		y_vals = []
		for row in plot_data:
			x_vals.append(row.pop(0))
			y_vals.append(int(row.pop(0), 16))
		plt.plot(x_vals, y_vals)
		plt.ylabel("Cumulative Data Bytes as A Value")
		plt.xlabel("Time") 
		plt.title(str(filename) + "  PID " + str(filt_id))
		plt.savefig(str(filename) + " PID " + str(filt_id) + ".png")


	# the challeng her is how to print the shit.. well fuck lets just print all the data from plot_data 

	else: 
		for i in range(0,num_bytes):
			plt.subplot(num_bytes, 1, i+1) 
			plt.title(str(filename) + "  PID " + str(filt_id) + " Byte " + str(filt_bytes[i]))
			# print (int(filt_bytes[i]))
			# print (len(plot_y[int(filt_bytes[i])]))
			
			if(len(plot_x) != len(plot_y[int(filt_bytes[i])])):
				plt.plot(plot_y[int(filt_bytes[i])]) 
			else: 	
				plt.plot(plot_y[int(filt_bytes[i])]) 
				plt.ylabel("Byte" + str(filt_bytes[i])) # otherwise we should just print all the bytes 
		
		plt.xlabel("Time") 
		plt.savefig(str(filename) + " PID " + str(filt_id) + " Bytes " + ".png")



filter_by_id(filt_id, filename, plot_data)
filter_bytes(filt_bytes, plot_data, plot_y, plot_x, bytes_present)
plotlin(plot_x, plot_y, plot_data, filt_bytes)

