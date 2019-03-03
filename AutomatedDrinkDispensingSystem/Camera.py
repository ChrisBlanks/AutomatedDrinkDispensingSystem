#!/usr/bin/env python3

"""
Programmer: Chris Blanks
Last Edited: March 2019
Project: Automated Self-Serving System
Purpose: This script defines the Camera class.
"""


#Built-Ins
import os
import time
import threading
import datetime
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

	def __init__(self,main_app_instance):
		super().__init__(main_app_instance)
		
		#PeripheralDevice info
		self.name = "camera"
		self.state = "enabled"               
		self.pin_number = None         
		self.buffer = None  #will pass images through this variable            
		self.buffer_data_type = "ImageTk's PhotoImages"
		
		self.face_xml_path = self.main_app.CASCADES_PATH + "/haarcascade_frontalface_default.xml"
		self.face_cascade = cv2.CascadeClassifier(self.face_xml_path) #takes about 0.2 seconds to complete
		
	
	def startThreading(self,video_tk_label):
		"""Starts thread for reading camera input. Takes video_tk_label arg
		for continuously updating a Tk label's image parameter in order to show
		the Picamera's video output."""
		
		self.vs = VideoStream(usePiCamera=1).start() #video stream object
		self.MAX_WIDTH = 500  #sets max width of frames
		
		self.frame = None
		self.panel = None
		self.thread = None #video will have to run a separate thread
		
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
				
				UF.drawEars(self.frame,self.buffer,self.face_cascade)
				
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

