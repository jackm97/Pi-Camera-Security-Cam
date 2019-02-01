#!/usr/bin/env python3
#
# record.py - motion tracking software for Raspberry Pi Camera (Raspbian Stretch)
#
# 25May18 Jack Myers
# 6June18 Added time tracking
#



# import the necessary packages
#from picamera.array import PiRGBArray
#from picamera import PiCamera
import numpy as np
import imutils
from imutils.video import VideoStream
import time
import os
import cv2

 
####################################################################################

def get_save_file(filetype):
	""" 
	
	input:
		filetype - string with type of file to save (e.g. ".avi")
	returns:
		filename -  name of file that the recorded video or time stamps will save to
	"""

	filedate = time.strftime("%m-%d-%Y")
	filename = None
	filenum = 1
	while True:
		filename = filedate + '_%s'%filenum + filetype
		if not os.access(filename, os.F_OK):
			return filename
		else:
			filenum+=1
			
	

#####################################################################################

def process(frame, fgbg, kernel, debug, ttrack):
	"""
	Process frame to determine objects that are moving in the frame
	
	Parameters:
		frame - the raw frame from camera.capture_continuous to be processed
		fgbg - the background extraction object
		kernel - the kernel used for noise cancellation
		debug - boolean for debugging
		ttrack - boolean for time tracking

	Returns:
		image - processed image with bounding rectangles around detected objects
		fgmask - binary image from which the contours are found
		ismotion - boolean indicating if motion is detected in teh frame
	"""
	# Rotate the image
	image = frame
	image = imutils.rotate(image, angle = 180)
		
	# Apply background subtraction and clean up noise
	fgmask = fgbg.apply(image)
	fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
	fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
	ret, fgmask = cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
		
	# Find the contours from the fgmask binary image
	img, contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	
	# Eliminate contours that are too small that likely come from noise and various
	# scene shifts. Also apply rectangles to the original image around contours if debug
	goodcont = 0
	for c in contours:
		if cv2.contourArea(c) > 600:	
			(x, y, w, h) = cv2.boundingRect(c)
			if debug:
				cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
			goodcont += 1
	
	# Checks for motion in the frame
	if goodcont > 0:
		ismotion = True
	else:
		ismotion = False
	
	# time stamp the frame
	font = cv2.FONT_HERSHEY_SIMPLEX
	ctime = time.strftime("%H:%M:%S")
	if not ttrack:
		cv2.putText(image, ctime, (10, 450), font, 1.3,(255,255,255),3,cv2.LINE_AA) 
	else:
		cv2.putText(image, ctime, (10, 450), font, 1.3,(0,255,0),3,cv2.LINE_AA)        
	return image, fgmask, ismotion

######################################################################################

def capture(debug=False):
	"""
	Capture, display, and save live stream from pi camera

	Parameters:
		debug - boolean for debugging

	***NOTE***
	If debugging is enabled when recording, the output video
	file will contain bounding boxes

	"""
	
	# defines a frame buffer, and opencv video writer for saving video
	frame_buf = []
	frames = []
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	
	# variable for time counting
	t0 = time.perf_counter()
	

	# booleans for debugging, saving video, and time tracking
	isrecord = False
	debug = debug
	ttrack = False
	wasmotion = False

	# set up background subtractor and kernel for noise removal
	fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold = 25, detectShadows = True)
	kernel = np.ones((5,5),np.uint8)

	# initialize camera
	vs = VideoStream(src=0, usePiCamera=True, resolution=(640,480),
		framerate=8).start() 	
	time.sleep(2.0)
	
	# capture frames from the camera
	while True:
		frame = vs.read()
        # process frame
		image, fgmask, ismotion = process(frame, fgbg, kernel, debug, ttrack)
		dimage = image.copy() #display image for live feed

		# when recording is enabled, frames are written to the .h264 file
		# when motion is detected and a recording indicator is put to the live feed
		if isrecord:
			if ismotion:
				if len(frame_buf) > 0:
					for frame in frame_buf:
						out.write(frame)
					frame_buf = []
				out.write(image)
					
			else:
				if len(frame_buf) < 8:
					frame_buf.append(image.copy())
				else:
					frame_buf.append(image.copy())
					del frame_buf[0]
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(dimage, 'Recording',(10, 25), font, 1,(0,0,255),2,cv2.LINE_AA)
	 
		
		# records time stamp and durations of detected motion
		if ttrack:
			if ismotion and ismotion!=wasmotion:
				t0 = time.perf_counter()
				date = time.strftime("%m-%d-%Y")
				ctime = time.strftime("%H:%M:%S")
			
			if not ismotion and ismotion!=wasmotion:
				dt = time.perf_counter() - t0
				outline = date + " " + ctime + ", " + "%.10f\n"%dt
				textfile.write(outline)
				

		# show the frame
		# if debug = True also show bounding rectangles and fgmask
		# and debugging indicator is applied
		if debug:
			cv2.imshow("Mask", fgmask)
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(dimage, 'Debugging',(450, 25), font, 1,(255,255,255),2,cv2.LINE_AA)
		
		cv2.imshow("Live Feed", dimage)
		key = cv2.waitKey(1) & 0xFF
 
		
 
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			if ttrack and ismotion:
				dt = time.perf_counter() - t0
				outline = time.strftime("%m-%d-%Y") + " " + time.strftime("%H:%M:%S") + ", " + "%.10f\n"%dt
				textfile.write(outline) 
			break
		
		# if the 'r' key is pressed, recording is stopped or started
		elif key == ord("r"):
			if not isrecord:
				#get the filename that the next recorded video will save to
				filename = get_save_file('.avi')
				out = cv2.VideoWriter(filename,fourcc, 8.0, (640,480))
			else:
				#release the previous output file
				out.release()
			isrecord = not isrecord
		
		# if the 't' key is pressed time tracking is enabled
		elif key == ord("t"):
			if not ttrack:
				filename = get_save_file('.txt')
				textfile = open(filename, 'w')
			else:
				textfile.close()
			ttrack = not ttrack
				

		# if the 'd' key is pressed, debugging is toggled on and off
		elif key == ord("d"):
			if debug:
				cv2.destroyWindow('Mask')
			debug = not debug
		
		wasmotion = ismotion
		
	cv2.destroyAllWindows()
	try:
		out.release()
	except:
		pass
	try:
		textfile.close()
	except:
		pass
	
##########################################################################################

if __name__ == "__main__":
	capture()
