# FL_image_analysis
Tools for processing still images from videos taken through the internal camera of a surgical microscope, recording full-spectrum (non-filter) images illuminated dually by white light and fluorescence excitation in which the monochrome intensity of particular region of interest is to be quantified in the context of the intensity of the whole image.  We have used this pipeline specifically for the analysis of images of intraoperative fluorescein perfusion of brain tumors from the HD camera (1080p) on an OPMI PENTERO 900 (Zeiss) with a yellow 560 filter, and quantification of biopsies within those illuminated fields.

###The process consists of the following steps:###

1.	Extraction of monochrome pixel intensities.  The included instructions are for Adobe Photoshop (CC 2015), which is the only program we have used for this purpose.  Other pixel-based image software (e.g. ImageJ) could be used equivalently.

	•	Rendering of the image (*.tif, *.jpg, *.gif, *.bmp, etc. input) in RGB
	
	•	Monochrome masking of the image
	
	•	Determination of region of interest (ROI)
	
	•	Export of pixel intensity histograms
	
2.	Integration of pixel intensity data with other available data about biopsy.  Radiographic localization, subjective fluorescence, pathology diagnosis, timestamp, and other features tabulated in *.txt files of specified format.

3.	Calculation of objective fluorescence intensity bin and fractional fluorescence intensity based on biopsy ROI and field histograms, and export of integrated data file.

###Extraction of monochrome pixel intensities###
We perform these operations using commercial software (Adobe Photoshop).  No additional setup required. Other programs or home-written software may be substituted if they provide monochrome masking, in order that the green channel be isolated, and export of pixel intensities in user-defined ROIs. We provide a detailed protocol (/FL_ImageExport_PROTOCOL.pdf), two example image files, and two directories of example output data from this process (/ExampleFiles/).

###Calculation of quantitative fluorescence intensity value of biopsy ROI based on biopsy FIELD###

FL_rundirectory.py, FL_biopsy.py, and FL_image.py are programs written by J. Sims in Python2.7.5.  They require the following modules (standard installation):  sys, string, numpy, os, argparse.

In addition to these programs, the following files are expected as input:

Biopsy Data -- a tab-delimited text file with biopsy sample names in Col0, Raw fluorescence intesnity values (mean or median intensity of ROI histogram) in Col1, and other non-imaging data in other columns (variable number accomodated, headers required).  See example file "BiopsyData.txt"

FIELD histogram files -- a tab-delimited text file containing Col0 = [0:255], Col1 = number of pixels of intensity value. This can be manually or automatically generated from the "FIELD.csv" histograms output during step 1.  See example files:
```	FL16-T1-MF.tsv
	FL16-T2-HF.tsv
	FL16-T3-NF.tsv
	FL19-T2-MF.tsv
	FL20-T1-HF.tsv
	FL23-T2-NF.tsv
	FL23-T4-MF.tsv
	FL27-T1-NF.tsv
	FL27-T2-LF.tsv
	FL45-T1-HF.tsv
	FL45-T2-NF.tsv
	FL45-T3-NF.tsv
	FL67-T2-NF.tsv
```
These filenames must begin with the same patient/timepoint identifier as the biopsy names listed in the Biopsy Data file.

To run the image and biopsy analysis pipeline on all these files, run the following command from a directory which contains 1) the three python programs, 2) the *.tsv files (above) and 3) BiopsyData.txt:
```
python FL_rundirectory.py BiopsyData.txt -t tsv
```
This compares biopsies listed in Col0 of BiopsyData.txt to their corresponding files in the present directory.  For more details on usage, file specification, and analysis options, see the help documentation:
```
python FL_rundirectory.py -h
```
