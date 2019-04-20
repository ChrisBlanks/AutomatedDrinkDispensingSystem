#!/usr/bin/env python3

"""
Programmer: Chris Blanks
Last Edited: April 2019
Project: Automated Self-Serving System
Purpose: This script defines the EmbeddedBoard class.

Notes:
  >	If the following error is received, the it is most likely due to a
    mismatch in the number of bytes that are meant to be sent on the 
    master computer side and to be received on the embedded board side.
    
    'OSError: [Errno 121] Remote I/O error'
    
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
	HALT_ADDRESS = 16      # 16 = 0x10
	#Have to send dummy data (1 byte)
	
	I2C_SLAVE_ADDRESS = 51 # 51 = 0x33 is the address of the Embedded board
	RECIPE_MAKER_ADDRESS = 55    # 55 = 0x37 is the address of a "register"
	ORDER_DRINK_ADDRESS = 87  #
	# 87 = 0x57 is the address to write to in order to transmit Drink ID & time to pump
	
	TRANSMIT_DELAY = 0.1 #delay for for 100 milliseconds between data transmission
	COMM_INPUT_PIN = 4   #GPIO pin used for communication protocol with embedded board  
	
	
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
		GPIO.setup(self.COMM_INPUT_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP) 
		#setup pin 4 as input
		#pull-up is setup on pin 4


	def getStateOfPin(self):
		return GPIO.input(self.COMM_INPUT_PIN)
	
	
	def pollPinUntilLow(self):
		"""Poll until pin 4 is low (signals that data transmission can start)"""
		print(GPIO.input(self.COMM_INPUT_PIN))
		while str(GPIO.input(self.COMM_INPUT_PIN)) == "1":
			print(GPIO.input(self.COMM_INPUT_PIN))


	def initializeDrinkMenuOnBoard(self, data_sequence=None):
		"""This function writes a series of data (HEX form) to the embedded
		boards via I2C. Note: Only can transmit 30 bytes of data.
		
		Recipe Data Format: [id, time_val_0,time_val_1,time_val_2,time_val_3,time_val_4,time5,time6,time7,valve_num ]
		Data length: 10 items/Bytes
		"""
		
		data_buffer = None  #stores recipe data from drink menu file
		
		if self.main_app is not None:
			#If not testing, then grab data from drink menu file.
			with open(self.main_app.DRINK_MENU_FILE_PATH,"r") as drink_menu:
				data_buffer = drink_menu.readlines()
				buffer_count = 0
		
		#write data for all 24 potential recipes
		for i in range(24):
			print("Recipe #{}".format(str(i)))
			DRINK_ID = i

			with SMBusWrapper(1) as bus:
				for j in range(4):
					valve_array_num = j #there are 4 valve arrays; 2 boards with 2 registers dedicated to valves
					print("Valve #{}".format(str(j)))
					
					if self.main_app is None:
						DATA= [DRINK_ID, 51+i,52+i,53+i,54+i ,55+i,56+i,57+i,58+i, valve_array_num]
						#each element after DRINK_ID represents a pump time for each valve connected to the embedded board
					else:
						DATA = (data_buffer[buffer_count]).split(",")
						DATA = [int(x) for x in DATA] #convert into a list of integers
						buffer_count +=1
						pass 
					
					#Writing the recipe
					try:
						bus.write_i2c_block_data(self.I2C_SLAVE_ADDRESS,self.RECIPE_MAKER_ADDRESS+j,DATA)
						time.sleep(self.TRANSMIT_DELAY) #takes floats
					except OSError:
						print("Error: Not able to write data at recipe stage.")
				   


	def orderDrink(self,data_sequence=None):
		"""This function writes data to embedded board device, so that the drink
		specified in the data_sequence variable is ordered

		Order Data Format: [id, quantity_of_drinks,placeholder,placeholder,placeholder,placeholder,
		placeholder,placeholder,placeholder,placeholder ]	
		
		Data length: 10 items/Bytes
		
		*Placeholder values will not be used by embedded board..
		"""
		
		if data_sequence is None:
			# Test data
			DRINK_ID = 1 
			DATA =[DRINK_ID,2,0,0,0,0,0,0,0,0]
		else:
			DATA = data_sequence 
		
		print("Sending drink data now.")	
		with SMBusWrapper(1) as bus:
			# Ordering the drink(s)
			bus.write_i2c_block_data(self.I2C_SLAVE_ADDRESS,self.ORDER_DRINK_ADDRESS,DATA)
			time.sleep(self.TRANSMIT_DELAY) #takes floats


	def sendHaltCommand(self):
		"""Commands the embedded board to stop making a drink."""
		with SMBusWrapper(1) as bus:
					# Ordering the drink(s)
					bus.write_byte_data(self.I2C_SLAVE_ADDRESS,self.HALT_ADDRESS,0)
					time.sleep(self.TRANSMIT_DELAY) #takes floats

		


if __name__ == "__main__":
	MainApp = None
	embedded_dev = EmbeddedBoard(MainApp)
	embedded_dev.orderDrink()
	

