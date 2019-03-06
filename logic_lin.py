#	Authored: Max Pfeiffer - 2018
#
#	Converts the .csv output generated from Saleae Logic Lin Analyzer to a more legible 
# 	and data-processing friendly format. 
#
#	Usage: 	python gls_ecu_filt.py "gls_info_cabana_logfile.csv" "0xAA" "0xBB" ...
#		"gls_info_cabana_logfile.csv" = the file to decode 
#		"0xAA" = first id to filter 
#		"0xBB" = second id to filter 
# 		etc.. 
#
#	Output: "lin_ + filename.csv" in format; "Time, ID, Data"
#
#
#!/usr/bin/python
import sys
import csv
import ctypes

filename = sys.argv[1]

input_file = open(sys.argv[1])
og_data = csv.reader(input_file, delimiter = ",")

output_data = open("lin_"+ sys.argv[1], "w+")							
output_writer = csv.writer(output_data, delimiter = ",")
output_writer.writerow(["Time", "ID", "Data"]) 

time = 0
pid = -1
data = ""
header = 1
chk_flag = False



# takes in the first character of a log data line 
# returns true if this is the beginning of a checksum line  
def is_checksum(first_char): 
	# print first_char + " = " + str(ord(first_char))
	if ord(first_char) == 67:
		return True 
	else: 
		return False 


# takes in the first character of a log data line 
# returns true if this is the beginning of a PID line 
def is_pid(first_char):
	return ord(first_char) == 80 


# takes in the first character of a log data line 
# returns true if this is the beginning of a Data line 
def is_data(first_char):
	return ord(first_char) == 68


# returns the hex data portion of the passed as a 2-character string 
def extract_hex(test_list):
	# iterates over the test list until the prev_char is 0 and the cur_char is x
	# then it pops the next two characters as the hex result, with out the 0x prefix. 

	prev_char = test_list.pop(0)
	cur_char = test_list.pop(0)
	prev_ord = ord(prev_char)
	cur_ord = ord(cur_char)
	# print " prev_char = " + str(prev_char) + "prev_ord = " + str(prev_ord)
	# print " cur_char = " + str(cur_char) + "cur_ord = " + str(cur_ord)

	while (cur_ord != 120) or (prev_ord != 48): 
		prev_ord = cur_ord
		cur_ord = ord(test_list.pop(0))
	#	print "cur_ord = " + str(cur_ord)
	#	print "prev_ord = " + str(prev_ord)
	#	print cur_ord != 120
	#	print prev_ord != 48

	# print "stopped the hex search with the list as " + str(test_list)

	# find the 'x' in the 0x00 sequence, then make sure the LIN logs from Logic are converted  
	# cur_char = ord(test_list.pop(0))
	#test_char = test_list.pop(0)
	#cur_char = ord(test_char)
	##not_hex = True 
	#while cur_char != 120 and not_hex:
		# almost also need to look for the 0x combination, not just the x or the 0 combinaton 


		#cur_char = ord(test_list.pop(0))
		#test_char = test_list.pop(0)
		#cur_char = ord(test_char)
		#if cur_char == 48: 
		#	not_hex == False
			# this should help us find that 0 before the x to make sure we're getting the 0x combo 
			# needed to avoid and false positives 

	# extract the next two components as the hex result 
	result = test_list.pop(0)
	result = result + test_list.pop(0)
	# print "restult of extract_hex is " + str(result)

	return result


# saves the present message content 
# resets the message content variables
def save_message(content): 
	output_writer.writerow(content)
	time = 0 


# takes a string of 2 character btyes concatenated with 0 spaces 
# and returns a list with the last byte eliminated 
def strip_last_byte(data_str):
	data_str = list(data_str)
	data_str.pop(len(data)-1)
	str_data = ""
	while(len(data_str) > 1):
		str_data = str_data + data_str.pop(0) 
	return str_data


for row in og_data:
	if header:
		header = 0
	else: 
		# extract the requisite information from the row 
		row_data = list(row.pop(2))				
		first_char = row_data.pop(0)
		# print "first char is " + str(first_char)

		# check to see if we're seeing a checksum flag
		if chk_flag == False:
			chk_flag = is_checksum(first_char)
		
		if(is_pid(first_char)):
			# once past the initial edge case, save the message data collected up util that PID  
			if(pid > -1): 
				# strip is there was no checksum and we have an extra byte 
				if len(data) and chk_flag == False:
					data = strip_last_byte(data)	
					 
				# save the message and reset the checkflag 
				save_message([time,pid,data])
				data = ""
				chk_flag = False

			# Save the PID information 
			pid = extract_hex(row_data)
			pid = int(pid, 16)	
			# print "decimal converted ID is " + str(pid)
			time = row.pop(0)

		elif(is_data(first_char)):
			hex_data = extract_hex(row_data)
			# print "hex_data is " + str(hex_data)
			# print "data before" + str(data)
			data = data + str(hex_data) 
			# print "data after " + str(data)

# for the last frame, save it once we exit the for loop
if len(data) and chk_flag == False:
	data = strip_last_byte(data)

save_message([time, pid, data])


