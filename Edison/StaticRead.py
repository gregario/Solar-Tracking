# Script to read values from the trad tracking arduino
# Assumes a /home/static/ folder
# Greg Jackson 24/03/2017 AESE Labs, Imperial College London
# Needs MRAA installed
# Copyright (c) 2017, greg jackson
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import mraa
import time 
import serial
import simplejson
import os

debug = True # Determines if prints work
SLEEP_TIME = 60 # Interval between measurements 
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
	PORT = '/dev/{}'.format(output[1]) # This one is the min of the coms, the other will be max
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
	output_jsons.append({'source': 'realTesting', 'test': 'midCom', 'DOF': '1DOF', 'packet': x})
	try:	
		resultFile = open("static/data_mcom_{}.json".format(epoch_time),'wb')
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
