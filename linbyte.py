#	Authored: Max Pfeiffer - 2018
#
#	Takes a passed .csv file with a CAN or LIN log in the "Time, ID, Data" format 
# 	and prints the output in a .csv format of a given id and a given byte from that id. 
# 	
#	Usage: 	python linbyte.py example_log.csv ex_id 1 
#		where example log is the data
#		filtered by ex_id, so only this id is filtered 
#		the following numbers indicate byte fields we wish to print 
#
#!/usr/bin/python
import sys
import csv


filename = sys.argv[1]
filt_id = sys.argv[2]
filt_bytes = []
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
			outlist = []
			if(pid == filt_id):
				num_bytes = 0 
				time = row.pop(0)
				data = row.pop(0)

				# split the data into a list
				list_data = list(data)

				# get the length of that list, otherwise 0 
				num_bytes = len(list_data) if len(list_data) > num_bytes else num_bytes

				# split up the bytes 
				for i in range(0,int(num_bytes/2)):
					first = list_data.pop(0)
					second = list_data.pop(0)
					outval = int(str(first + second), 16)
					outlist.append(outval)

				printout = str(time) + ", "
				for val in filt_bytes:
					printout = printout + str(outlist[int(val)])  
					if (len(filt_bytes) > 1): 
						printout = printout + ", "
				print(printout)

						

	control.close()	

filter_by_id(filt_id, filename, plot_data)


