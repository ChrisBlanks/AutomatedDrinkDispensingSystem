#!/usr/bin/env python3

#standard libraries
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

#my modules
import Inventory


class InventoryManager:
	#Labels for windows
	NAME_LABEL_STR = "Item Name: {}"
	VALVE_NUM_LABEL_STR= "Valve Number: {}"
	ORIG_QTY_LABEL_STR= "Original QTY (Ounces): {}"
	CUR_QTY_LABEL_STR= "Current QTY (Ounces): {}"


	def __init__(self,master,main_app):
		self.top_level = master
		self.main_app = main_app
		self.inventory_items = self.main_app.inventory_items
		self.inventory_names = self.getNames()

		self.current_item = None
		self.replace_but = None
		
		self.configureWindow()

	
	def getNames(self):
		"""Get inventory item names """
		names = []
		for item in self.inventory_items:
			names.append(item.name)
		return names


	def configureWindow(self):
		"""Creates a messagebox for terminating toplevel and then
		sets up window for displaying inventory info."""
		self.main_app.employee_window.inventory_manager.protocol(
			"WM_DELETE_WINDOW",self.deployExitMessageBox)

		self.setupEachPane()


	def setupEachPane(self):
		"""Sets up each individual pane of the toplevel window."""
		self.setupLeftPane()
		self.setupRightPane()


	def populateListbox(self):
		"""Inserts inventory names into listbox."""
		index = 0

		for item_name in self.inventory_names:
			self.inventory_options.insert(index,item_name)
			index+=1


	def setupLeftPane(self):
		"""Creates listbox and adds in inventory item names."""
		self.inventory_options = tk.Listbox(self.top_level,selectmode=tk.SINGLE)

		self.inventory_options.bind('<<ListboxSelect>>',self.listboxCallback)
		self.top_level.add(self.inventory_options) #puts listbox into left pane
		self.populateListbox() #add names to listbox


	def listboxCallback(self,event):
		"""Listbox selection is used to generate content on the right pane"""
		index = self.inventory_options.curselection()

		if index == None or index == "":
			return #don't do anything

		try:
			self.selected_item = self.inventory_options.get(index)
			print(self.selected_item)
		except tk._tkinter.TclError:
			return #supporess empty listbox error
		
		
		for item in self.inventory_items:
			if self.selected_item.lower() in item.name.lower():
				 self.current_item = item
				 break
		
		if self.replace_but is not None:
			self.replace_but.grid_forget() #get rid of last button
		
		self.populateRightPane()



	
	def setupRightPane(self):
		"""Initializes elements for right pane."""
		self.frame = tk.Frame(self.top_level)
		self.top_level.add(self.frame) #add frame to right pane

		#make buttons & labels here
		self.name_label = tk.Label(self.frame,text=self.NAME_LABEL_STR.format(""))
		self.name_label.grid(row=0)
		
		self.valve_num_label = tk.Label(self.frame,text=self.VALVE_NUM_LABEL_STR.format(""))
		self.valve_num_label.grid(row=1)
		
		self.original_qty_label = tk.Label(self.frame,text=self.ORIG_QTY_LABEL_STR.format(""))
		self.original_qty_label.grid(row=2)

		self.current_qty = tk.Label(self.frame,text=self.CUR_QTY_LABEL_STR.format(""))
		self.current_qty.grid(row=3)
		
		self.replace_but = ttk.Button(self.frame,text="Edit",command= self.launchEditor)
		
		#self.switch_valves_but = tk.Button(self.frame,text="Switch Valves")

	
	def populateRightPane(self):
		"""Adds in the inventory item information & other widgets."""
		self.name_label.configure(text=self.NAME_LABEL_STR.format(self.current_item.name))
		self.valve_num_label.configure(text=self.VALVE_NUM_LABEL_STR.format(self.current_item.valve_number))
		self.original_qty_label.configure(text=self.ORIG_QTY_LABEL_STR.format(self.current_item.org_quant))
		self.current_qty.configure(text=self.CUR_QTY_LABEL_STR.format(self.current_item.cur_quant))
		#place button when an item is selected
		self.replace_but.grid(row=4)


	def launchEditor(self):
		"""Launches the editor for changing inventory information."""
		#top = tk.Toplevel()
		print("Launching inventory editor.")
		pass



	def deployExitMessageBox(self):
		"""Prompts user before closing window."""
		if messagebox.askokcancel("Quit","Are you sure?",parent=self.top_level):
			self.main_app.employee_window.inventory_manager.destroy()
			self.main_app.employee_window.master.deiconify()

