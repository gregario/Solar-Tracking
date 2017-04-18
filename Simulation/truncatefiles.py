import sys,os,shutil
import simplejson,uuid,time



#test_loop = ['0A1']
test_loop = ['0A1','0A2','0A3','0A4','0A5','0A6','0A7','0B1','0B2','0B3','0B4','0B5','0B6','0B7','0C1','0C2','0C3','0C4','0C5','0C6','0C7','0D1','0D2','0D3','0D4','0D5','0D6','0D7']
#test_loop = ['0B1','0B2','0B3','0B4','0B5','0B6','0B7']
#test_loop = ['0C1','0C2','0C3','0C4','0C5','0C6','0C7']
#test_loop = ['0D1','0D2','0D3','0D4','0D5','0D6','0D7']

def fileoperation(test):
		resultFile = open("results/{}_solartracking_results.json".format(test),'r')
		x = simplejson.load(resultFile)
		resultFile.close()
		return x

def main():
	print "day,static,1DOF,2DOF,bruteforce,lightweight"
	for test in test_loop:
		x = fileoperation(test)
		for key in x: 
			if ((key['test'] == 'tradTrack') and (key['DOF'] == 'static')):
				print "{0},{1},".format(key['source'],key['current_gen']),
			if ((key['test'] == 'tradTrack') and (key['DOF'] == '1DOF')):
				print ',',
				print key['current_gen'],
			if ((key['test'] == 'tradTrack') and (key['DOF'] == '2DOF')):
				print ',',
				print key['current_gen'],
			if (key['test'] == 'bruteOptimisation'):
				print ',',
				print key['cur_gen_max'],
			if (key['test'] == 'lightOptimisation'):
				print ',',
				print key['current_gen']



main()

