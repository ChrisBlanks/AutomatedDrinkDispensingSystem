#!/usr/bin/env python3
"""
Programmer: Chris Blanks
Last Edited: Feb 2019
Project: Automated Self-Serving System
Purpose: This script defines the EmployeeSwitch class, which reads input
from the GPIO pins of the raspberry pi and controls whether employee mode
is switched on.
"""

from gpiozero import Button

from PeripheralDevice import PeripheralDevice


class EmployeeSwitch(PeripheralDevice):
	def __init__(self,main_app):
		super().__init__(main_app)
		self.name = "switch"
		self.state = "enabled"
		self.pin_number = 17	# GPIO pin 17
		
		self.button = Button(17)  #assign pin 17 to button object


	def checkButtonInput(self):
		"""Sets up a button on GPIO7 & runs the react(). """
		
		if self.button.is_pressed:
			self.switchToEmployeeMode()
	
		
	def switchToEmployeeMode(self):
		"""Turns on employee mode."""
		print("Employee Mode ON")
		#self.state = "off"  needs to be enabled somewhere later
		self.main_app.selectWindow(1)  #starts the employee window
