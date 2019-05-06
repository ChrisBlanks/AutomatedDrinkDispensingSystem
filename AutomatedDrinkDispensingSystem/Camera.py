#!/usr/bin/env python3

"""
Programmer: Chris Blanks
Last Edited: March 2019
Project: Automated Self-Serving System
Purpose: This script defines the Camera class. It inherits the basic attributes
of the peripheral device class, so that it can have a standard interface that
a MainApp instance can use. Also it uses UtilityFuncs functions in order
to apply filters to frames captured by a PiCamera.
"""


#Built-Ins
import os
import time
import threading
import datetime
import random 

import tkinter as tk

#3rd Party
import imutils
import cv2
from PIL import Image, ImageTk
from imutils.video import VideoStream

#My Modules
import UtilityFuncs as UF
from PeripheralDevice import PeripheralDevice



class Camera(PeripheralDevice):
	
	ALIAS_NAME = "UF"  #concatenated with strings of functions
	
	def __init__(self,main_app_instance):
		super().__init__(main_app_instance)
		
		#PeripheralDevice info
		self.name = "camera"
		self.state = "off" #not on until threading starts              
		self.pin_number = None         
		self.buffer = None  #will pass images through this variable            
		self.buffer_data_type = "ImageTk's PhotoImages"
		
		self.face_xml_path = "{}/haarcascade_frontalface_default.xml".format(self.main_app.CASCADES_PATH)
		self.eyes_xml_path = "{}/haarcascade_eye.xml".format(self.main_app.CASCADES_PATH)
		
		self.face_cascade = cv2.CascadeClassifier(self.face_xml_path) #takes about 0.2 seconds to complete
		self.eyes_cascade = cv2.CascadeClassifier(self.eyes_xml_path)  #another performance hit.. oh no!
		
	
	def startThreading(self,video_tk_label):
		"""Starts thread for reading camera input. Takes video_tk_label arg
		for continuously updating a Tk label's image parameter in order to show
		the Picamera's video output."""
		
		self.vs = VideoStream(usePiCamera=1).start() #video stream object
		self.state = "enabled"
		self.MAX_WIDTH = 500  #sets max width of frames
		
		self.frame = None
		self.panel = None
		self.thread = None #video will have to run a separate thread
		
		draw_funcs = [] #will store name of functions as strings
		format_str = "{}.{}(self.frame,self.buffer,self.face_cascade)"
		format_str2 = "{}.{}(self.frame,self.buffer,self.face_cascade,self.eyes_cascade)"
		
		[draw_funcs.append( dir(UF)[j] ) for j in range(0, len(dir(UF))-1) if "draw" in dir(UF)[j] ]
		#searches for any items in UtilityFuncs that has "draw" in its name
		
		face_funcs = [format_str.format(self.ALIAS_NAME,item) for item in draw_funcs if "Eyes" not in item]
		eye_funcs = [format_str2.format(self.ALIAS_NAME,item) for item in draw_funcs if "Eyes" in item]
		
		all_funcs = face_funcs + eye_funcs 
		#after doing separate formatting, select one for the current filter 
		
		selection = random.randint(0,len(all_funcs)-1)
		self.current_filter = all_funcs[selection]
		print("\nFilter function to execute is: {}\n".format(self.current_filter))
		
		self.stopEvent = threading.Event() #controls exit behavior of GUI
		self.thread = threading.Thread(target=self.updateFrame,kwargs={'tk_label': video_tk_label})
		self.thread.start()  #starts a separate thread to avoid conflicts w/ GUI


	def updateFrame(self,tk_label):
		"""Starts an infinite loop in the thread that will read each frame
		from the Picamera and display it in the GUI application."""
		
		self.panel = tk_label
		time.sleep(2.0) #allow the camera to warm up
		try:
			initialFrame = True
			while not self.stopEvent.is_set() :
				self.frame = self.vs.read()
				self.frame = imutils.resize(self.frame,width=self.MAX_WIDTH) 
				
				#cv2 makes images use BGR color space by default, but
				#need RGB for Image objects
				self.buffer = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB) 
				
				exec(self.current_filter) #executes the function in the string
				
				
				self.buffer = Image.fromarray(self.buffer) #convets Mat object to Image
				self.buffer = ImageTk.PhotoImage(self.buffer) #image is now TK compatible
				
				if initialFrame:
					self.panel.configure(image=self.buffer)
					self.panel.image = self.buffer
					self.panel.pack(padx=10,pady=10)
					
					initialFrame = False
				else:
					self.panel.configure(image=self.buffer)
					self.panel.image = self.buffer  #needed so image will be displayed
					
				
		except RuntimeError:
			print("Runtime error!")

		
	def onExit(self):
		"""Performs the exit behavior."""
		print("Exiting...")
		self.stopEvent.set() #when set, the continuous loop in callback stops
		self.vs.stop() #stop video stream
		self.state = "off"

