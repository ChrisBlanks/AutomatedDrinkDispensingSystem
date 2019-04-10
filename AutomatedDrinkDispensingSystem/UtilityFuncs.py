"""
Programmer: Chris Blanks
Last Edited: March 2019
Project: Automated Self-Serving System
Purpose: This script defines miscellaneous utility functions that don't need to be in a class.
Notes:
	- Any function with 'draw' in its name can be dynamically selected by 
	the Camera object and executed
		>these functions must have this format for their arguments:
			def foo(input_frame, output_frame, classifier_used)
			
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
		
		radius = int(math.sqrt((w*w) + (h*h) ) /2) #half of hypotenuse will give a good radius
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



def drawRainbowMask(in_frame,out_frame,classifier ):
	"""Detects faces in an input frame (a.k.a in_frame), and draws
	superimposed multicolored mask on face."""
	
	#the addWeighted() &  Mat.copy() functions are pretty slow
	
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
		
		#does the weighted sum of two matrices
		# args: input, alpha, input2, beta, gamma, output
		#basically doing a cross-dissolve here
		cv2.addWeighted(overlay,0.4,out_frame,1- 0.4, 0, out_frame) 
		#superimposes the copied image on the output image
		
		
def drawGlassesForEyes(in_frame,out_frame,face_classifier, eyes_classifier):	
	"""Draws glasses on the face of the user."""
	gray = cv2.cvtColor(in_frame,cv2.COLOR_BGR2GRAY) #convert original BGR to Grayscale
	
	faces = face_classifier.detectMultiScale(
		gray,  #CV_8U or cv 8 bit unsigned type
		scaleFactor=1.1,  #how much image size is reduced at each image scale
		minNeighbors=5,   #how many neighbors each candidate rectangle should have
		minSize=(30,30),  #min pssible object size ; no max specified
		flags=cv2.CASCADE_SCALE_IMAGE
	)
	
	for (x,y,w,h) in faces:
		roi_gray= gray[y:y+h,x:x+h] #index the cells that make up the detected face
		roi_out = out_frame[y:y+h,x:x+h] #same size for output frame
		
		glasses_color = (rd.randint(0,255),rd.randint(0,255),rd.randint(0,255))
		
		eyes = eyes_classifier.detectMultiScale(roi_gray,1.1,3) #detects eyes
		
		candidate_points = [] #list of points around perimeter of eye circles 
		radii_rank = []
		count = 0
		for(eye_x,eye_y,eye_w,eye_h) in eyes:
			center = (int(eye_x+ eye_w/2), int(eye_y+ eye_h/2))
			radius = int(math.sqrt( (eye_w*eye_w) + (eye_h*eye_h) ) /2)
			
			cv2.circle(roi_out,center,radius,glasses_color,2) 
			
			#get two points that are diametrically opposed
			#the sin(0) or sin(180) should be zero, but added in for completion
			theta_180 = math.radians(180) #convert degrees to radians
			
			candidate_1 = (radius*math.cos(0) + int(eye_x+ eye_w/2),
							radius*math.sin(0) + int(eye_y+ eye_h/2) )
			
			candidate_2 = (radius*math.cos(theta_180) + int(eye_x+ eye_w/2),
							radius*math.sin(theta_180) + int(eye_y+ eye_h/2) )
			
			#creates a way of determining the largest detected eyes
			radii_rank.append((count,radius))
		
			candidate_points.append((candidate_1,candidate_2)) #add points as a tuple 
			count += 1
		
		#need at least two eyes to draw glasses
		#only one person will get glasses (as of now)
		if len(eyes) > 1:

			pos = [] #stores position of two largest circles for indexing candidate_points
			#run two times to get two largest circles
			for i in range(2):
				largest = None
				for k in range(len(radii_rank)):
					if k == 0:
						largest = radii_rank[k] #initial is largest
					else: 
						#check the rest against the largest
						if radii_rank[k][1] > largest[1] :
							largest = radii_rank[k]			
				#should have the largest radii by here
				pos.append(largest[0]) #save which circle is the biggest
				radii_rank.remove(largest) #remove largest, so that the second largest can be found
			
			big_candidates = candidate_points[pos[0]] #largest eye detected
			small_candidates = candidate_points[pos[1]] #2nd largest eye detected
			
			first_dist = abs(big_candidates[0][0] - small_candidates[1][0])
			second_dist = abs(big_candidates[1][0] - small_candidates[0][0])
			
			#draw a line between the shorter distances
			#offset for lines of eye glasses frame that goes to ears
			offset_y = -30
			offset_x = -30
			
			if first_dist > second_dist:
				# point 1 bet
				x1 = int(big_candidates[1][0])
				y1 = int(big_candidates[1][1])
				
				x2 = int(small_candidates[0][0])
				y2 = int(small_candidates[0][1])
				
				outer1 = (int(big_candidates[0][0]),
				int(big_candidates[0][1]))
				
				outer2= (int(small_candidates[1][0]),
				int(small_candidates[1][1]))
										
				offset1 = (int(big_candidates[0][0] -offset_x),
				int(big_candidates[0][1] +offset_y))
				
				offset2= (int(small_candidates[1][0] +offset_x),
				int(small_candidates[1][1] +offset_y))
			else:
				x1 = int(big_candidates[0][0])
				y1 = int(big_candidates[0][1])
				
				y2 = int(small_candidates[1][1])
				x2 = int(small_candidates[1][0])
				
				outer1 = (int(big_candidates[0][0]),
				int(big_candidates[0][1]))
				
				outer2= (int(small_candidates[1][0]),
				int(small_candidates[1][1]))
							
				offset1 = (int(big_candidates[1][0] -offset_x),
				int(big_candidates[1][1] +offset_y))
				
				offset2= (int(small_candidates[0][0] +offset_x),
				int(small_candidates[0][1]+ offset_y))
			
			#draw a line between the circles
			cv2.line(roi_out,(x1,y1),(x2,y2),glasses_color,2)
			
			#line for ear part of frames
			cv2.line(roi_out,outer1,offset1,glasses_color,2)
			cv2.line(roi_out,outer2,offset2,glasses_color,2)
		
		
		
