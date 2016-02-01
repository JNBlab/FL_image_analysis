#! /usr/bin/python
import numpy as np
import sys
import os
import argparse
from string import split

#------------------------FL_rundirectory.py--------------------
#---------Jennifer S. Sims, Columbia University, 2016----------



#--------- PARSE ARGUMENTS ------------------

parser = argparse.ArgumentParser(description='This parser provides options for running image analysis on a set of fields defined by a list of similarly named samples which are listed together with other sample data in a tab-delimited spreadsheet, "samplefile" which is the only positional argument. Flag -F to concatenate samplefile with a defined list of image data files ~OR~ flag -t to define the (suffix) filetype of all files to be concatenated. Flags -m and -p define the type and range of the maximum value, default is the mean of pixels in the top 5 percent of intensities.', epilog='Minimum information is samplefile, which will return a lovely blank file unless you define some other files with -F or -t.')

parser.add_argument('samplefile',help='A file which contains the samples as Col0. Use tab-delimited text (*.txt, *.tsv).')
parser.add_argument('-m','--maxtype',default='mean',choices=['mean','median'],help='Type of midpoint for the MaxRange of the image pixel intensity. Options are mean and median.')
parser.add_argument('-p','--maxpercent',default=5,help='Percent of top pixel intensities included in MaxRange. Default is 5.')
parser.add_argument('-t','--filetype',help='Flagging -t will run all files corresponding to samples in the samplefile which have the specified filetype suffix.')
parser.add_argument('-F','--filename',action='append',help='Flagging -F will run each file that follows a flag.')

args=parser.parse_args()

samplefile = args.samplefile
maxtype = str(args.maxtype)
maxpercent = int(args.maxpercent)
filetype = args.filetype
if filetype == None:
	try:
		infile = args.filename[0]
	except TypeError:
		sys.exit('No image files. Use [-h] to see help message on flags and inputs.')

# print maxtype,maxpercent,filetype,infile

#------------- PROGRAMS TO USE ------------
#---- accomodates changes to version number
prog1 = 'FL_image'
prog2 = 'FL_biopsy'

for file1 in os.listdir('.'):
	if file1.startswith(prog1):
		if file1.endswith('.py'):
			program1 = file1
		else:
			print 'Image program not found. Ensure that it contains "FL_image*", or alter this code, Line 40.'

for file2 in os.listdir('.'):
	if file2.startswith(prog2):
		if file2.endswith('.py'):
			program2 = file2
		else:
			print 'Biopsy program not found. Ensure that it contains "FL_image*", or alter this code, Line 41.'

#--------- IDENTIFY SAMPLES -----------------

samplelist = []

sampleinput = open(samplefile,'r')
k = 0
for line in sampleinput.readlines():
	llist = split(line)
	if k != 0:
		id = str(llist[0])
		id = str(id.rstrip('-HMargLNxF'))
		samplelist.append(id)
	k = k+1
sampleinput.close()
print k

#----------- RUN PROGRAM1 (IMAGE ANALYSIS) ON FILES ---------------------
# INPUTS FOR FL_image.py ARE AS FOLLOWS:
# infile = sys.argv[1]	# histogram file name (from FIELD)
# image_outfile = sys.argv[2]	# outfile name -- this temp file will contain the columns described above for this single histogram input
# percentmax = int(sys.argv[3])	# size (percentage of 255) of 'MaxRange' described above.  Default input in FL_rundirectory.py is 5, and can be changed in FL_rundirectory.py.
# maxtype = sys.argv[4]

filelist = []

try:
	filelist.append(infile)
#	print infile
except NameError:
	pass
except ValueError:
	pass

d_ID = {}

for file in os.listdir('.'):
	for id in samplelist:
		if file.startswith(id):
			if file.endswith(str(filetype)):
				filelist.append(file)
				print file
filelist=list(set(filelist))
print len(filelist),'files'

for fileitem in filelist:
	for id in samplelist:
		if fileitem.startswith(id):
			d_ID[fileitem] = id

for x in range(0,len(filelist)):
	file1 = filelist[x]
	sample = d_ID[file1]
	outname = str(sample) + '_max' + str(maxtype) + str(maxpercent) + '_pixels.out'
	cmd1 = 'python %(program1)s %(file1)s %(outname)s %(maxpercent)i %(maxtype)s' % vars()
	print 'IMAGE',cmd1
	os.system(cmd1)

#--------- RUN PROGRAM2 (BIOPSY ANALYSIS) ON ALL IMAGE ANALYSIS OUTPUT FILES IN DIRECTORY ------------
# samplefile = sys.argv[1]	# The master biopsy file which contains: Col0 = all sample names, Col1: = all other data, adjust code as needed.  Row0 = headers, and these will be directly copied to the output file.
# outfile = sys.argv[2] 	# to be named
# filetype = sys.argv[3]	# This is the suffix of the image_output file from FL_image.py.  Here, we automatically fill based on type of maxrange.

outfile = str(samplefile.rstrip('.txt''.tsv')) + '_max' + str(maxtype) + str(maxpercent) + '_biopsyanalysis.txt'
suffix = '_max' + str(maxtype) + str(maxpercent) + '_pixels.out'
		
cmd2 = 'python %(program2)s %(samplefile)s %(outfile)s %(suffix)s' % vars()
print 'BIOPSY',cmd2
os.system(cmd2)

print 'BOOM'
