# FL_image_analysis
Tools for processing still images from videos taken through the internal camera of a surgical microscope, recording full-spectrum (non-filter) images illuminated dually by white light and fluorescence excitation in which the monochrome intensity of particular region of interest is to be quantified in the context of the intensity of the whole image.  We have used this pipeline specifically for the analysis of images of intraoperative fluorescein perfusion of brain tumors from the HD camera (1080p) on an OPMI PENTERO 900 (Zeiss) with a yellow 560 filter, and quantification of biopsies within those illuminated fields.

###The process consists of the following steps:###

1.	Extraction of monochrome pixel intensities.  The included instructions are for Adobe Photoshop (CC 2015), which is the only program we have used for this purpose.  Other pixel-based image software (e.g. ImageJ) could be used equivalently.

	•	Rendering of the image (*.tif, *.jpg, *.gif, *.bmp, etc. input) in RGB
	
	•	Monochrome masking of the image
	
	•	Determination of region of interest
	
	•	Export of pixel intensity histograms
	
2.	Integration of pixel intensity data with other available data about biopsy.  Radiographic localization, subjective fluorescence, pathology diagnosis, timestamp, and other features tabulated in *.txt files of specified format.

3.	Calculation of objective fluorescence intensity bin and fractional fluorescence intensity based on biopsy ROI and field histograms, and export of integrated data file.

