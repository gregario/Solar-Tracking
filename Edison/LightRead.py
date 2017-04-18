# Script to read values from the trad tracking arduino
# Assumes a /home/static/ folder
# Greg Jackson 24/03/2017 AESE Labs, Imperial College London
# Needs MRAA installed

import mraa
import time 
import serial
import simplejson
import os

debug = True # Determines if prints work
SLEEP_TIME = 5 # Interval between measurements 
BAUDRATE = 9600
BYTESIZE = serial.EIGHTBITS
PARITY = serial.PARITY_NONE
STOPBITS = serial.STOPBITS_ONE
XONOFF = False
TIMEOUT = 3
DELAY = 0.2  # communication delay

def openSerial():
	directory = "/dev/"
	files = []
	for (dirpath, dirnames, filenames) in os.walk(directory): 
	        files.extend(filenames)
	output = [s for s in files if "ACM" in s]
	PORT = '/dev/{}'.format(max(output)) # This one is the min of the coms, the other will be max
	if debug: print PORT 

	try:
		TI = serial.Serial(PORT, BAUDRATE, BYTESIZE, PARITY, STOPBITS, TIMEOUT, XONOFF)
	except Exception,e:
		print "error open serial port: " + str(e)
	return TI

def bufferList(TI):
	i = TI.inWaiting() # number of chars waiting in the RX buffer
	if i == 0:
		if debug: print "Nothing in Buffer"
	else:
		x = TI.readline() # read i chars from RX buffer
		if debug: print x
		writeToFile(x)

def writeToFile(x):
	output_jsons = [] # output file
	epoch_time = int(time.time())
	output_jsons.append({'source': 'realTesting', 'test': 'upperCOM', 'DOF': '1DOF', 'packet': x})
	try:	
		resultFile = open("light/data_ucom_{}.json".format(epoch_time),'wb')
		simplejson.dump(output_jsons, resultFile)
	except:
		pass
	finally:
		resultFile.close()

def main():
	TI = openSerial()
	while True:
		if debug: print("beginning serial read")
		bufferList(TI)
		if debug: print("file write finished")
		time.sleep(SLEEP_TIME)

main()
