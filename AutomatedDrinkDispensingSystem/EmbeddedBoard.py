#!/usr/bin/env python3

"""
Programmer: Chris Blanks
Last Edited: April 2019
Project: Automated Self-Serving System
Purpose: This script defines the EmbeddedBoard class.
"""

#standard library imports
import time 

#3rd party module imports
from smbus2 import SMBusWrapper
import RPi.GPIO as GPIO

#my modules
from PeripheralDevice import PeripheralDevice



class EmbeddedBoard(PeripheralDevice):
	
	#Class variables
	TARGET_ADDRESS= 51 #51 = 0x33 is the address of the Embedded board
	REG_ADDRESS= 55    #55 = 0x37 is the address of a "register"
	DRINK_ADDRESS= 87  #87 = 0x57 is the address to write to in order to transmit Drink ID & time to pump
	
	TRANSMIT_DELAY = 0.1 #delay for for 100 milliseconds between data transmission
	
	def __init__(self,main_app_instance):
		"""Sets up an EmbeddedBoard device for communication with the
		main computer."""
		
		self.main_app = main_app_instance
        
        """
        pins 2 & 3 are used for i2c
        pin 4 is used as an input pin to determine whether the embedded
        board is ready for communication.
        """
        self.name = "Embedded Board"
        self.state = "off" 
        self.pin_number = ['2','3','4']  
        self.buffer = None             # Any data that needs to be used in the main app
        self.buffer_data_type = "Strings"
        

        GPIO.setmode(GPIO.BCM)
		GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_UP) 
        #setup pin 4 as input
		#pull-up is setup on pin 4


	def pollPinUntilLow(self):
    """Poll until pin 4 is low (signals that data transmission can start)"""
		while GPIO.input(4) == True:
			pass


	def writeToEmbeddedBoard(self,data_sequence=None):
		"""This function writes a series of data (HEX form) to the embedded
		boards via I2C."""
		
		DRINK_ID = 1 # Drink ID in the system; placeholder
		
		if data_sequence is None:
			DATA = [DRINK_ID,41,42,43,44,45,46,47,48,49,50]
			DATA2 =[DRINK_ID,20,41,43,44,45,46,47,48,49,50]
		else:
			DATA = data  #must be a list of data (each item is )
		
				
		with SMBusWrapper(1) as bus:
			bus.write_i2c_block_data(self.TARGET_ADDRESS,self.REG_ADDRESS,DATA)
			time.sleep(self.TRANSMIT_DELAY) #takes floats
			bus.write_i2c_block_data(self.TARGET_ADDRESS,self.DRINK_ADDRESS,DATA2)
			time.sleep(self.TRANSMIT_DELAY) #takes floats




if __name__ == "__main__":
    writeToEmbeddedBoard()
    """
    If the following error is received, the it is most likely due to a
    mismatch in the number of bytes that are meant to be sent on the 
    master computer side and to be received on the embedded board side.
    
    OSError: [Errno 121] Remote I/O error
    """

