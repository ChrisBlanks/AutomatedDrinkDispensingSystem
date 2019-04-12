#!/usr/bin/env python3

"""Test for reading pulses from bill acceptor."""

import RPi.GPIO as GPIO

def waitAndCount():
	"""Infinite loop that waits for a falling edge and writes number of
	falling edges to an output file."""
	GPIO.setmode(GPIO.BCM) #matches pin scheme of gpiozero's pinout command
	# aka channel numbers on Broadcom SOC

	#GPIO.setwarnings(False) #prevents unecessary warnings

	PULSE_PIN = 21
	GPIO.setup(PULSE_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP) #setup pulse pin as input & add pull-up circuit++

	ONE_SEC = 1000  #every function uses milliseconds, so need to do conversion
	MAX_WAIT_TIME = 30 * ONE_SEC  #Program will be stalled for a max of 30 seconds
	
	pulse_count = 0
	while 1: #just close shell to end loop
		result = GPIO.wait_for_edge(PULSE_PIN,GPIO.FALLING
			,timeout=MAX_WAIT_TIME) 
		#hold program until max wait time if is exceeded or falling edge is detected
		
		print(result) #result will be 21 if a falling edge is found
		if result is None:
			print("No cash was inserted.")
		else:	
			pulse_count = pulse_count + 1 #increment count for each 0 state
			msg = "pulse count:"+str(pulse_count) + "\n"
			print(msg)
			with open("out.txt",'a+') as out:
				if pulse_count == 1:
					out.write("\nnew session -- $\n")
				out.write(msg)
	
	GPIO.cleanup() #clears pins


class PulsePin:
	"""Sets up the GPIO #21 (BCM) for reading pulses from a bill acceptor."""
	PULSE_PIN = 21
	BOUNCE_TIME = 100
	
	
	def __init__(self):
		self.pulse_count = 0
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False) #prevents unecessary warnings
		GPIO.setup(self.PULSE_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP) 
		#setup pulse pin as input & add pull-up circuit++
	
	
	def __del__(self):
		print("Removing pin code.")
		GPIO.remove_event_detect(self.PULSE_PIN)
		GPIO.cleanup() #clears pins


	def detectPulseEvent(self):
		"""Detects whenever a falling edge happens on the PULSE_PIN """
		GPIO.add_event_detect(self.PULSE_PIN,GPIO.FALLING,bouncetime=self.BOUNCE_TIME
							,callback= self.pulseCallback)
		#if another falling edge happens within .1 seconds, then it is ignored
		#callback is executed in a separate thread
		while 1: 
			pass #supposed to simulate infinite tkinter root loop
			
		
	def pulseCallback(self,channel):
		"""Callback function for what to do when the falling edge is triggered """
		self.pulse_count +=1
		print("pulse count = " +str(self.pulse_count))


pp = PulsePin()
pp.detectPulseEvent()	

