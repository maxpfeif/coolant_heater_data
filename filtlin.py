#	Authored: Max Pfeiffer - 2018
#
#	Takes a passed .csv file with a LIN log in the "Time, ID, Data" format 
# 	and prints the filtered messages with the filtered id to the console. 
##
#	Usage: 	python filtlin.py example_log.csv ex_id 
#		where example log is the data to be plotted 
#		filtered by ex_id, so only this id is filtered 
#
#!/usr/bin/python
import sys
import csv

filename = sys.argv[1]
filt_id = sys.argv[2]

control = open(filename)
og_data = csv.reader(control, delimiter=",");
header = 1
for row in og_data:
	if header:
		header = 0
		print ("Time, Data")
	else: 
		pid = row.pop(1)
		if(pid == filt_id):
			time = row.pop(0)
			data = row.pop(0)
			print (str(time) + "\t" +  str(data))
control.close()	
