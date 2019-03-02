"""
Programmer: Chris Blanks
Last Edited: March 2019
Project: Automated Self-Serving System
Purpose: This script defines miscellaneous utility functions that don't need to be in a class.
"""

import cv2
import time

def detectFace(in_frame,out_frame,classifier ):
	"""Detects faces in an input frame (a.k.a in_frame), and draws a rectangle
	centered at the detected area on to the corresponding coordinates in the output
	frame (a.k.a out_frame)"""
	gray = cv2.cvtColor(in_frame,cv2.COLOR_BGR2GRAY) #convert original BGR to Grayscale
	
	#create a list of detected faces in a frame  
	faces = classifier.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30,30),
		flags=cv2.CASCADE_SCALE_IMAGE
	)
	
	for (x,y,w,h,) in faces:
		cv2.rectangle(out_frame,(x,y),(x+w,y+h),(0,255,0),2) #draw a green rectangle for each face
	
