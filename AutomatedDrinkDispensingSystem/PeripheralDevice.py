#!/usr/bin/env python3
"""
Programmer: Chris Blanks
Last Edited: 10/24/2018
Project: Automated Self-Serving System
Purpose: This script defines the Peripheral Device class.
"""


class PeripheralDevice:
    def __init__(self, main_app_instance):
        """Initializes device information for main application. 
        Behavior is defined in the derived classes."""
        
        self.main_app = main_app_instance
        
        #DEVICE INFO
        self.name = None                #string
        self.state = None               #either off, enabled, processing
        self.pin_number = None          #gpio pin on PI if used
        self.buffer = None              #passes data through this variable
        self.buffer_data_type = None    #data type of buffer


