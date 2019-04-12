#!/usr/bin/env python3

import threading
import datetime
import imutils
from imutils.video import VideoStream
import os
import sys
import time

import tkinter as tk
from PIL import Image, ImageTk
import cv2

from button_gpio_test import setupButtonInput


class VideoFeed:
	def __init__(self, vs):
		"""Initializes basic members."""
		self.vs = vs #video stream object
		self.MAX_WIDTH = 300 #sets max width of frames
		
		self.CASCPATH = "haarcascade_frontalface_default.xml"
		self.face_cascade = cv2.CascadeClassifier(self.CASCPATH)
		
		self.frame = None
		self.panel = None
		self.thread = None #video will have to run a separate thread
		self.stopEvent = None

		
		self.setupTimerValues()
		
		self.root = tk.Tk()
		self.root.wm_protocol("WM_DELETE_WINDOW",self.onExit)
		
		self.checkButtonState() #initializes checking
		
		self.stopEvent = threading.Event() #controls exit behavior of GUI
		self.thread = threading.Thread(target=self.callback)
		self.thread.start()  #starts a separate thread to avoid conflicts w/ GUI
	
	
	def setupTimerValues(self):
		"""Sets the timer for reading the button state."""
		self.isBeginning = True
		self.DELAY = 3000  #seconds between each check of button
		self.REP_NUM = 3   #determines number of cycles before stop
		self.beginning_timer= self.REP_NUM * self.DELAY  #total checking time
	
		
	def callback(self):
		"""Does something """
		try:
			while not self.stopEvent.is_set() :
				self.frame = self.vs.read()
				self.frame = imutils.resize(self.frame,width=self.MAX_WIDTH) 
				
				#cv2 makes images use BGR color space by default, but
				#need RGB for Image objects
				self.image = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
				
				#intermediate processing
				gray = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
				faces = self.face_cascade.detectMultiScale(
					gray,
					scaleFactor=1.1,
					minNeighbors=5,
					minSize=(30,30),
					flags=cv2.CASCADE_SCALE_IMAGE
				)
				
				for (x,y,w,h,) in faces:
					cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,255,0),2) #draw a green rectangle for each face
				 
				self.image = Image.fromarray(self.image) #convets Mat object to Image
				self.image = ImageTk.PhotoImage(self.image) #image is now TK compatible
				
				if self.panel is None: #initialize if 1st run
					self.panel = tk.Label(image=self.image)
					self.panel.image = self.image  #save this instance variable
					self.panel.pack(side="left",padx=10,pady=10)
				else:
					self.panel.configure(image=self.image)
					self.panel.image = self.image  #needed so image will be displayed
				
		except RuntimeError:
			print("Runtime error!")

		
	def onExit(self):
		"""Sets the exit behavior."""
		print("Exiting...")
		self.stopEvent.set() #when set, the continuous loop in callback stops
		self.vs.stop() #stop video stream
		self.root.quit() #not needed for embedding in senior design GUI

	
	def checkButtonState(self):
		"""Recursively calls itself to check button state until the 
		beginning timer runs out."""
		setupButtonInput()
		if self.isBeginning:
			self.root.after(self.DELAY,self.checkButtonState)
			self.beginning_timer = self.beginning_timer - self.DELAY
			print(self.beginning_timer)
			if self.beginning_timer <= 0:
				self.isBeginning = False #ends checking


	def setupFaceDetection(self,cascpath):
		"""Starts process for face detection."""
		
		
		
		
	def imageProcessing(self):
		"""Does image processing for each frame."""

def runVideoFeed():
	"""Creates a video feed using a Picamera  """
	vs = VideoStream(usePiCamera=1).start()
	print("Warming up camera.")
	time.sleep(2.0)
	
	VF = VideoFeed(vs)
	VF.root.mainloop()


if __name__ == "__main__":
	runVideoFeed()
