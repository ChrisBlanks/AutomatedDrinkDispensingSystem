#!/usr/bin/env python3

"""
Programmer: Chris Blanks
Last Edited: Feb 2019
Project: Automated Self-Serving System
Purpose: This script defines the PulsePin class, which reads the pulsating
output of a MEI bill acceptor. The output from the bill acceptor is formed
by a open-collector circuit, so this requires a pull-up resistor on the 
RasPi input, attaching the ground wire of the bill acceptor to the Raspi's ground,
and reading a falling edge to find out how much money has been
inserted into the bill acceptor. Also a software debounce was used to reduce
false-positives.
"""

import RPi.GPIO as GPIO

#my modules
from PeripheralDevice import PeripheralDevice

class PulsePin(PeripheralDevice):
	"""Sets up the GPIO #21 (BCM) for reading pulses from a bill acceptor."""
	PULSE_PIN = 21
	BOUNCE_TIME = 100
	
	
	def __init__(self,main_app_instance):
		super().__init__(main_app_instance)
		
		self.name = "PulsePinForBillAcceptor"
		self.state = "enabled"
		self.pin_number = self.PULSE_PIN
		
		self.pulse_count = 0
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False) #prevents unecessary warnings
		GPIO.setup(self.PULSE_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP) 
		#setup pulse pin as input & add pull-up circuit++
	
	
	def __del__(self):
		print("Removing pin code.")
		GPIO.cleanup() #clears pins


	def detectPulseEvent(self):
		"""Detects whenever a falling edge happens on the PULSE_PIN and
		 sets a callback functions """
		GPIO.add_event_detect(self.PULSE_PIN,GPIO.FALLING,bouncetime=self.BOUNCE_TIME
							,callback= self.pulseCallback)
			
		
	def pulseCallback(self,channel):
		"""Callback function for what to do when the falling edge is triggered """
		self.pulse_count +=1
		print("pulse count = " +str(self.pulse_count))

		
	def disablePulseEvent(self):
		"""Disables detection of falling edge."""
		print("Disable pulse detection.")
		GPIO.remove_event_detect(self.PULSE_PIN)
		

