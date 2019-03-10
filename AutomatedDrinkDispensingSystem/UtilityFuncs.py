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
import random as rd


def drawEars(in_frame,out_frame,classifier ):
	"""Detects faces in an input frame (a.k.a in_frame), and draws bunny ears on a person's head"""
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
		
		"""
		#original bounding rectangle and circle
		
		cv2.rectangle(out_frame,(x,y),(x+w,y+h),(0,0,255),2) 
		center = ( int(x+w/2) , int(y + h/2) ) 
		radius = int(h/2)
		radius = int(math.sqrt((w*w) + (h*h) ) /2)
		cv2.circle(out_frame,center,radius,(0,0,255),2) 
		centers circle on rect & makes radius the same height as square
		"""
		
		x_center = int(x+ w/2) 
		y_center = int(y+ h/2)
		
		radius = int(math.sqrt((w*w) + (h*h) ) /2) 
		#radius of circle that future shapes will be residing on 
		
		theta = math.radians(30) #determines ear position on circle edge
		
		#Points (x2,y2) & (x3,y3) will define the centers of the following shapes
		# adding an offset of -90 degrees to account for (0,0) being in the top left
		y2 = y_center + (radius* math.sin(theta - math.radians(90) ) )
		y3 = y_center + (radius* math.sin(-1*theta - math.radians(90) ) )
		
		x2 = x_center + (radius* math.cos(theta - math.radians(90) ) )
		x3 = x_center + (radius* math.cos(-1*theta - math.radians(90) ) )
		
		if y2 < 0 or y3 < 0  or x2 < 0 or x3 < 0:
			pass #can't plot negative coodinates
		else:
			
			"""
			#circles used for experimentation
			
			center_2 = (int(x2),int(y2))
			center_3 = (int(x3),int(y3))
			
			cv2.circle(out_frame,center_2,10,(255,255,255),2)
			cv2.circle(out_frame,center_3,10,(255,255,255),2)
			"""
			
			#will shift shapes closer to the top of the frame
			center_4 = (int(x2),int(y2 -25))
			center_5 = (int(x3),int(y3 -25))
			
			DEGREES = 15  #degrees of tilt of ellipse
			AXES_LENGTHS = (10,30)  # defines a big ellipse to make a bunny ear
			AXES_LENGTHS_2 = (4,18)  # defines a smaller ellipse to make the inner ear
			ARC_START = 0
			ARC_END = 360   #draws a full ellipse when from 0 to 360
			W_COLOR = (255,255,255)  #white color
			P_COLOR = (255,228,225)  #pink color (apparently misty rose)
			FILL = -1 #passing a negative number fills the ellipse
			
			#creates bunny ears around the top of someone's head
			#tilt the ellipses away from each other 
			cv2.ellipse(out_frame,center_4,AXES_LENGTHS,DEGREES,ARC_START,ARC_END,W_COLOR,FILL)
			cv2.ellipse(out_frame,center_5,AXES_LENGTHS,-1*DEGREES,ARC_START,ARC_END,W_COLOR,FILL) #rotate other direction
			
			cv2.ellipse(out_frame,center_4,AXES_LENGTHS_2,DEGREES,ARC_START,ARC_END,P_COLOR,FILL)
			cv2.ellipse(out_frame,center_5,AXES_LENGTHS_2,-1*DEGREES,ARC_START,ARC_END,P_COLOR,FILL) #rotate other direction



def drawMask(in_frame,out_frame,classifier ):
	"""Detects faces in an input frame (a.k.a in_frame), and draws
	superimposed multicolored mask on face."""
	gray = cv2.cvtColor(in_frame,cv2.COLOR_BGR2GRAY) #convert original BGR to Grayscale
	
	faces = classifier.detectMultiScale(
		gray,  #CV_8U or cv 8 bit unsigned type
		scaleFactor=1.1,  #how much image size is reduced at each image scale
		minNeighbors=5,   #how many neighbors each candidate rectangle should have
		minSize=(30,30),  #min pssible object size ; no max specified
		flags=cv2.CASCADE_SCALE_IMAGE
	)
	
	overlay = out_frame.copy() #make a copy of output frame
	
	for (x,y,w,h,) in faces:
		center = ( int(x+w/2) , int(y + h/2) ) 
		radius = int(h/2)
		
		cv2.circle(overlay,center,radius,
		(rd.randint(0,255),rd.randint(0,255),rd.randint(0,255)),-1) 
		
		cv2.addWeighted(overlay,0.4,out_frame,1- 0.4, 0, out_frame)
		
		
		
		
		
		
		
		
		
		
		
