"""
Programmer: Chris Blanks
Last Edited: March 2019
Project: Automated Self-Serving System
Purpose: This script defines miscellaneous utility functions that don't need to be in a class.
Notes:
	- a cvRectangle has the following data members:
		> img : image for the rectangle to be drawn on
	 	> pt1 : vertex of rectangle
	 	> pt2 : vertex of rectangle opposite to pt1
	 	> color : color of line generated; tuple of the form (R,G,B)
	 	> thickness : thickness of line
	 	> lineType : line type to us
	 	> shift : number of fractional bits in point coordinates
	 
	 - a cvCircle has the following data members:
		> img : image for the circle to be drawn on
	 	> center : center point of circle
	 	> radius : radius of the circle
	 	> color : color of line generated; tuple of the form (R,G,B)
	 	> thickness : thickness of line
	 	> lineType : line type to us
	 	> shift : number of fractional bits in point coordinates
"""

import cv2
import math

def detectFace(in_frame,out_frame,classifier ):
	"""Detects faces in an input frame (a.k.a in_frame), and draws a rectangle
	centered at the detected area on to the corresponding coordinates in the output
	frame (a.k.a out_frame)"""
	gray = cv2.cvtColor(in_frame,cv2.COLOR_BGR2GRAY) #convert original BGR to Grayscale
	
	faces = classifier.detectMultiScale(
		gray,  #CV_8U or cv 8 bit unsigned type
		scaleFactor=1.1,  #how much image size is reduced at each image scale
		minNeighbors=5,   #how many neighbors each candidate rectangle should have
		minSize=(30,30),  #min pssible object size ; no max specified
		flags=cv2.CASCADE_SCALE_IMAGE
	)
	
	# returns a list of rectangles representing detected faces in a frame 
	#format:
	# [ [1st_point 2nd_point width height ] [2nd rectangle dectected] ... ]

	for (x,y,w,h,) in faces:
		cv2.rectangle(out_frame,(x,y),(x+w,y+h),(0,0,255),2) 
		center = ( int(x+w/2) , int(y + h/2) )  #needs to be an integer
		cv2.circle(out_frame,center,int(h/2),(0,0,255),2) 
		#centers circle on rect & makes radius the same height as square
		
		#calculate new points around edge of circle
		x_center = int(x+ w/2) 
		y_center = int(x+ h/2)
		
		theta = math.radians(30) #30 degrees -> pi/6
		
		# add center offset to calculated value of x and y
		# adding an offset of -90 degrees to account for (0,0) being in the top left
		y2 = y_center + ((h/2)* math.sin(theta -90) )
		y3 = y_center + ((h/2)* math.sin(-1*theta - 90) )
		x2 = y_center + ((h/2)* math.cos(theta -90) )
		x3 = y_center + ((h/2)* math.cos(-1*theta - 90) )
		
		if y2 < 0 or y3 < 0  or x2 < 0 or x3 < 0:
			pass #can't plot negative coodinates
		else:
			center_2 = (int(x2),int(y2))
			center_3 = (int(x3),int(y3))
			
			cv2.circle(out_frame,center_2,10,(255,255,255),2)
			cv2.circle(out_frame,center_3,10,(255,255,255),2)
		
	


