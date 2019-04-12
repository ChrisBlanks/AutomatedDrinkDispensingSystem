#!/usr/bin/env python3

from gpiozero import Button
from signal import pause

def react():
	print("Employee Mode ON")

def setupButtonInput():
	"""Sets up a button on GPIO7 & runs the react(). """
	button = Button(17)
	#button.when_pressed = react
	if button.is_pressed:
		react()

if __name__ == "__main__":
	setupButtonInput()
		
	
