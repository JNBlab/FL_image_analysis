#! /usr/bin/python
import sys
from string import split
import numpy as np
import os

#------------------------FL_biopsy.py--------------------
#------Jennifer S. Sims, Columbia University, 2016------

# This program is used to:
# --- 1) compare the biopsy intensity to the pixel intensity distribution of the field as analyzed by FL_image.py
# --------- 1a) assign the biopsy to an objective bin
# --------- 1b) calculate the fractional intensity between the background level and the maximum intensity of the field 
# --- 2) append any other data about the biopsy, e.g. pathology diagnosis, radiographic location, cell count, time stamp
# Keep this program in the same directory as FL_rundirectory.py in order to run it using FL_rundirectory.py.

# This is intended to provide rudimentary image analysis for use in conjunction with more sophisticated commercial software, for the convenience of garnering quantitative information from screenshots taken on various cameras, and employs no novel algorithms. For your convenience adjusting this code to your own needs, I have included print lines throughout, generally after the declaration of key variables, which can be uncommented as needed (#).

#------------------ INPUT --------------------------

samplefile = sys.argv[1]	# A file which contains: Col0 = all sample names, Col1: = all other data, adjust code as needed.  Row0 = headers, and these will be directly copied to the output file.
outfile = sys.argv[2]		# to be named
filetype = sys.argv[3]		# This is the suffix of the image_output file from FL_image.py.  When running FL_biopsy.py from FL_rundirectory.py, it will be automatically filled based on type of maxrange.

samplelist = []
dSAMPLE = {}
sampleheader = []
filestrip = samplefile.rstrip('.tsv' '.txt')	# Your filetypes here.

sampleinput = open(samplefile,'r')
k = 0
for line in sampleinput.readlines():
	llist = split(line)
	if k == 0:
		sampleheader = llist
	elif k != 0:
		id = str(llist[0])
		id = str(id.rstrip('-HMargLNxF'))	# This is currently set to strip the "subjective call" classification off the end of our sample names.
		features = []
		for x in range(1,len(llist)):
			feat = str(llist[x])	# This is the biopsy intensity value. We have historically done this by hand in excel or other spreadsheet program, but a future pipeline version will remove this as input to FL_biopsy.py and include its automated extraction via FL_image.py.
			features.append(feat)
		dSAMPLE[id] = features
		samplelist.append(id)
	k = k+1
sampleinput.close()
print k

filenames = []
samplecall = []
fileheaders = []
filedata = []

dHIST = {}

l = 0
for id in dSAMPLE.keys():
	biopsydata = dSAMPLE[id]
	intensity = float(biopsydata[0])
	for file in os.listdir('.'):
		if file.endswith(filetype):
			if file.startswith(id):
				insplit = file.rsplit('_')		#adjust to suit your file naming system
#				print insplit
				input = open(file,'r')
				l = 0
				for line in input.readlines():
					llist = split(line)
					if l == 0:
						fileheaders = llist
					elif l > 0:
						filedata = llist
					l = l+1
#--------- FIND THE BIN RANGES ------------
				bg = int(filedata[fileheaders.index('Background')])
				lo = int(filedata[fileheaders.index('LowRange')].split('-')[1])
				mid = int(filedata[fileheaders.index('MidRange')].split('-')[1])
				hi = int(filedata[fileheaders.index('HighRange')].split('-')[1])
				if intensity <= bg:
					call = 'none'
				elif intensity <= lo:
					call = 'low'
				elif intensity <= mid:
					call = 'med'
				elif intensity > mid:
					call = 'high'
#--------- assign a fraction between max and background to the biopsy -------
				midpt = float(filedata[fileheaders.index('MidPoint')])
				hirange = hi - midpt
				lorange = midpt - bg
				if intensity > midpt:
					intval = intensity - midpt
					intfract = 0.5+0.5*(intval/hirange)
				elif bg < intensity <= midpt:
					intval = midpt - intensity
					intfract = 0.5-0.5*(intval/lorange)
				elif bg > intensity:
					intval = 0
					intfract = 0
				filenames.append(insplit[0])
				path = str(biopsydata[sampleheader.index('Pathology_dx')+1])		# Change this to whatever your pathology column is named
				print insplit[0],'Raw:',intensity,' SubjCall:',call,' Path:',path
				dHIST[id] = call,intfract,filedata
				if l == 3:
					print dHIST.values()
				input.close()

#------------- WRITE THE OUTPUT FILE ----------------
output = open(outfile,'w')

h1 = sampleheader[0]
h2 = 'ObjectiveCall'
h3 = 'FractionalIntensity'
output.write('%(h1)s\t%(h2)s\t%(h3)s' %vars())
for x in range(1,len(sampleheader)):
	h4 = sampleheader[x]
	output.write('\t%(h4)s' %vars())
for head2 in fileheaders:
	h5 = head2
	output.write('\t%(h5)s' %vars())
output.write('\n' %vars())

for id in dSAMPLE.keys():
	try:
		sampledata = dHIST[id]
		pt1 = id
		pt2 = dHIST[id][0]
		pt3 = dHIST[id][1]
		output.write('%(pt1)s\t%(pt2)s\t%(pt3)s' %vars())
		data = dSAMPLE[id]
		#print data
		for x in range(0,len(data)):
			pt4 = data[x]
			output.write('\t%(pt4)s' %vars())
		filedata = dHIST[id][2]
		for y in range(0,len(filedata)):
			pt3 = filedata[y]
			output.write('\t%(pt3)s' %vars())
		output.write('\n' %vars())
	except KeyError:
		print id, 'data not found'	
output.close()

print outfile,'...biopsy analysis complete!!'