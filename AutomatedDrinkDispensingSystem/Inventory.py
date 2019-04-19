#!/usr/bin/env python3

class InventoryItem:
	LOW_MSG = "Inventory item {} is low."
	EMPTY_MSG = "Inventory item {} is empty."
	
	def __init__(self,path,name,original_quantity,current_quantity,valve_num):
		self.inventory_file_path = path
		self.name = name
		self.org_quant = original_quantity
		self.cur_quant = current_quantity
		self.ratio_left = self.cur_quant / self.org_quant
		self.valve_number = valve_num
		
		self.checkRatio()


	def checkRatio(self):
		"""Updates ratio value and sends a notification if low or empty."""
		self.ratio_left= self.cur_quant / self.org_quant
		
		if self.ratio_left < 0.5:
			if self.ratio_left <= 0:
				return self.EMPTY_MSG.format(self.name)
			else:
				return self.LOW_MSG.format(self.name)
		else:
			return "At least half of inventory left." #empty string returned if more than half full
			
	
	def updateQuantityLeft(self,new_quantity):
		"""A new quantity value is inserted into the drink menu file."""
		lines = None
		with open(self.inventory_file_path ,"r+") as inventory_file:
			lines = inventory_file.readlines()
			lines[self.valve_number] ="{},{},{}\n".format(self.name,new_quantity,self.org_quant)
		
		with open(self.inventory_file_path ,"w") as inventory_file:	
			inventory_file.writelines(lines)
		
		self.cur_quant = new_quantity
		self.checkRatio()
	
	
	def switchValves(self,new_valve):
		"""Switches the place of the current item and the given item position.
		The inventory values should be retrieved from file after this function."""
		lines = None
		with open(self.inventory_file_path ,"r+") as inventory_file:
			
			lines = inventory_file.readlines()
			if new_valve > len(lines) -1 or new_valve < 1: #don't include header
				return #invalid argument values
			
			old_line = lines[self.valve_number] #get current drink menu line
			new_line = lines[new_valve] #get the new position's line
			
			lines[self.valve_number] = new_line
			lines[new_valve] = old_line
			
		with open(self.inventory_file_path ,"w") as inventory_file:	
			inventory_file.writelines(lines)

	
	def replaceItem(self,new_name,new_current_quantity,new_original_quantity):
		"""Replaces current Inventory item with the new one specified in
		the argument values. Should recollect inventory values from file
		after using this method."""
		lines = None
		with open(self.inventory_file_path ,"r+") as inventory_file:
			lines = inventory_file.readlines()
			lines[self.valve_number] ="{},{},{}\n".format(new_name,
						new_current_quantity,new_original_quantity)

		with open(self.inventory_file_path ,"w") as inventory_file:	
			inventory_file.writelines(lines)
			
			
