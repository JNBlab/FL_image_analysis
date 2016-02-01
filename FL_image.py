#! /usr/bin/python
import sys
from string import split
import numpy as np

#------------------------FL_image.py--------------------
#------Jennifer S. Sims, Columbia University, 2016------

# This program can be run on any histogram exported from Photoshop and transposed such that Col0=numerals 0-255 representing pixel intensities and Col1=numbers of pixels at each intensity.
# It is intended for use on the "FIELD" histogram describing the entire illuminated surgical field, in order that an ROI within that field be compared to its contextual pixel intensity.,
# Keep this program in the same directory as FL_rundirectory.py in order to run it using FL_rundirectory.py.

#-------------- NOTES ON PARAMETERS OF ANALYSIS-------
# Background Threshold = median of all pixels, unless this median is greated than 26. A pixel intensity of 26 is 10% of the possible intensity range. This can be adjusted (Line 103-104).
# MaxRange = a specified percentage of pixel intensities.  For example, if the maximum intensity in the field is 250, MaxRange is set at 5%, and MaxType is set at 'mean', the "maximum" used for calculating fractional fluorescence intensity would be the mean intensity of all pixels 237.5 < x < 250.

#------------- NOTES ON OUTPUT COLUMNS---------------(SE=self explanatory)
# 'TotalPixels' -- SE
# 'ZeroPixels' -- Number of pixels of intensity 0
# 'NonZeroPixels' -- Number of pixels of intensity > 0
# Maximum (size and type) -- percent of intensities included, maximum calculated as their 'mean' or 'median'. By default 'mean.'
# 'MaxRange' -- based on above parameters, the range of pixel intensities included to calculate a maximum for the field
# 'MeanIntensity' -- mean intesnity value of all non-zero pixels; defines low vs. medium threshold
# 'MedianIntensity' -- median intensity value of all non-zero pixels; defines background vs. low threshold
# 'MidPoint' -- midpoint value between the maximum and background values; defines medium vs. high threshold
# 'Background' -- same as MedianIntensity
# 'BgPixels' -- Number of pixels in background bin
# 'LowRange' -- Numerical intensity values of Low Intensity bin
# 'LowPixels' -- Number of pixels in Low Intensity bin
# 'MidRange' -- Numerical intensity values of Medium Intensity bin
# 'MidPixels' -- Number of pixels in Medium Intensity bin
# 'HighRange' -- Numerical intensity values of Medium Intensity bin
# 'HighPixels' -- Number of pixels in High Intensity bin

# This is intended to provide rudimentary image analysis for use in conjunction with more sophisticated commercial software, for the convenience of garnering quantitative information from screenshots taken on various cameras, and employs no novel algorithms. For your convenience adjusting this code to your own needs, I have included print lines throughout, generally after the declaration of key variables, which can be uncommented as needed (#).


#------------------ INPUT --------------------------

infile = sys.argv[1]	# histogram file name (from FIELD) *** NO HEADER ***
image_outfile = sys.argv[2]	# outfile name -- this temp file will contain the columns described above for this single histogram input
percentmax = int(sys.argv[3])	# size (percentage of 255) of 'MaxRange' described above.  Default input in FL_rundirectory.py is 5, and can be changed in FL_rundirectory.py.
maxtype = sys.argv[4]	# for pixels in 'MaxRange' described above, choose 'mean' or 'median'.  Default input in FL_rundirectory.py is 'mean', and can be changed in FL_rundirectory.py.

instrip = infile.rstrip('.tsv')
insplit = instrip.rsplit('_',1)

#---------- read histogram of pixels by intensity (0-255) into a dictionary
dINT = {}
input = open(infile,'r')
for line in input.readlines():
	llist = split(line)
	val = int(llist[0])
	try:
		num = int(llist[1])
		if num > 0:
			dINT[val] = num
		else:
			pass
	except IndexError:
		pass
input.close()
# print len(dINT.keys())
total = sum(dINT.values())
# print 'total pixels',total

#--------- make the synthetic subpopulation pixels that are greater than zero and sort them
totlist = []
for val in dINT.keys():
	if val != 0:
		num = dINT[val]
		for x in range(0,num):
			totlist.append(val)

#--------- sort the population
totlist.sort(reverse=True)
# print 'nonzero pixels',len(totlist)

#--------- to calculate the maximum, based on the percentage you inputted, first import the intensities as a numpy array
pxlints = np.array(totlist).astype(float)
maxval = int(np.amax(pxlints))
maxrange1 = percentmax*maxval/100
maxpxlints = pxlints[np.where(pxlints > maxval-maxrange1)]
# print 'new pixels', maxpxlints
if maxtype == 'median':
        maxmid = np.median(maxpxlints)
elif maxtype == 'mean':
        maxmid = np.mean(maxpxlints)

# print 'maxvalues',maxval,'-',maxrange1
# print 'MAX',maxtype,maxmid

#---------- calculate the other statistics on the non-zero pixel population

intmean = np.mean(pxlints)
intmed = np.median(pxlints)
intstd = np.std(pxlints)
# print 'mean intensity :',intmean
# print 'median intensity :',intmed
# print 'stdev intensity :',intstd

#------------------- DEFINE THE OBJECTIVE INTENSITY BINS ----------------------
# 'maxmid' is the mean or median of the 'MaxRange'
# The median of the non-zero pixels defines the background vs. low threshold.
# The mean of the non-zero pixels defines the low vs. medium threshold.
# The midpoint between 'maxmid' and background (non-zero median) defines the medium vs. high threshold.

valrange = maxmid - intmed
midval = int(intmed+0.5*valrange) 

if intmed > 26:
	bgval = 26
else:
	bgval = int(intmed)
	
lowrange = intmean - intmed
lowval = int(intmean)
	
bglist = []
lolist = []
midlist = []
hilist = []
bg = 0
l = 0
m = 0
h = 0
for val in dINT.keys():
	num = dINT[val]
	if val <= bgval:
		for x in range(0,num):
			bglist.append(val)
			bg = bg + 1
	elif val <= lowval:
		for x in range(0,num):
			lolist.append(val)
			l = l + 1
	elif val <= midval:
		for x in range(0,num):
			midlist.append(val)
			m = m + 1
	elif val > midval:
		for x in range(0,num):
			hilist.append(val)
			h = h + 1


# print 'Bkgd','0 :',bgval,bg
# print 'Low',bgval,':',lowval,l
# print 'Med',lowval,':',midval,m
# print 'Hi',midval,':',maxval,h

#-------------------- WRITE THE OUTPUT ---------------------

# outfile is one the inputs

output = open(image_outfile,'w')

h1 = 'TotalPixels'
h2 = 'ZeroPixels'
h3 = 'NonZeroPixels'
h4 = 'Max' + str(maxtype)
h5 = 'MaxRange'
h6 = 'MeanIntensity'
h7 = 'MedianIntensity'
h8 = 'MidPoint'
h9 = 'Background'
h10 = 'BgPixels'
h11 = 'LowRange'
h12 = 'LowPixels'
h13 = 'MidRange'
h14 = 'MidPixels'
h15 = 'HighRange'
h16 = 'HighPixels'
output.write('%(h1)s \t%(h2)s \t%(h3)s \t%(h4)s \t%(h5)s \t%(h6)s \t%(h7)s \t%(h8)s \t%(h9)s \t%(h10)s \t%(h11)s \t%(h12)s \t%(h13)s \t%(h14)s \t%(h15)s \t%(h16)s \n' %vars())

pt1 = total
pt2 = dINT[0]
pt3 = len(totlist)
pt4 = maxmid
pt5 = maxrange1
pt6 = intmean
pt7 = intmed
pt8 = midval
pt9 = bgval
pt10 = bg
pt11 = str(int(bgval)) + '-' + str(int(lowval))
pt12 = l
pt13 = str(int(lowval+1)) + '-' + str(int(midval))
pt14 = m
pt15 = str(int(midval+1)) + '-' + str(int(maxval))
pt16 = h
output.write('%(pt1)s \t%(pt2)s \t%(pt3)s \t%(pt4)s \t%(pt5)s \t%(pt6)s \t%(pt7)s \t%(pt8)s \t%(pt9)s \t%(pt10)s \t%(pt11)s \t%(pt12)s \t%(pt13)s \t%(pt14)s \t%(pt15)s \t%(pt16)s \n' %vars())

output.close()

print str(image_outfile),'PixelRange',len(dINT.keys()),'midval',midval
