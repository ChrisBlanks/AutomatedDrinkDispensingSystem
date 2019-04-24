#!/usr/bin/env python3

#standard libraries
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

#my modules
import Inventory


class InventoryManager:
	MAX_ITEMS = 32 #cannot have more than 32 inventory items
	#Labels for windows
	NAME_LABEL_STR = "Item Name: {}"
	VALVE_NUM_LABEL_STR= "Valve Number: {}"
	ORIG_QTY_LABEL_STR= "Original QTY (Ounces): {}"
	CUR_QTY_LABEL_STR= "Current QTY (Ounces): {}"


	def __init__(self,master,main_app):
		self.top_level = master
		self.main_app = main_app
		
		self.inventory_items = None
		self.inventory_names = None
		self.valve_numbers = None

		self.current_item = None
		self.replace_but = None
		
		self.collectInventoryItemsInfo()
		self.configureWindow()

	
	def collectInventoryItemsInfo(self):
		"""Updates changes to listbox."""
		self.inventory_items = self.main_app.inventory_items
		self.inventory_names = self.getNames()
		self.valve_numbers = self.getValveNumbers()

	
	def getNames(self):
		"""Get inventory item names """
		names = []
		for item in self.inventory_items:
			names.append(item.name)
		return names


	def getValveNumbers(self):
		"""Get the current valve numbers."""
		return list(range(1,len(self.inventory_items)))
		

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
		self.inventory_options.insert(0,"Add New/Replace Old")
		index = 1
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
		self.add_new_flag = False 
		
		index = self.inventory_options.curselection()

		if index == None or index == "":
			return #don't do anything
		
		try:
			self.selected_item = self.inventory_options.get(index)
			print(self.selected_item)
		except tk._tkinter.TclError:
			return #supporess empty listbox error
		
		if self.selected_item == "Add New/Replace Old":
			if len(self.valve_numbers) >= self.MAX_ITEMS:
				messagebox.showinfo("Exception:","Max limit of items reached.")
			else: #can still add more items
				self.add_new_flag = True
		else:
			for item in self.inventory_items:
				if self.selected_item.lower() in item.name.lower():
					 self.current_item = item
					 break
				else:
					print("Item not found.")
		
		if self.replace_but is not None:
			self.replace_but.grid_forget() #get rid of last button
		
		self.populateRightPane()



	
	def setupRightPane(self):
		"""Initializes elements for right pane."""
		self.frame = tk.Frame(self.top_level,background=self.main_app.MASTER_BACKGROUND_COLOR)
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


	def populateRightPane(self):
		"""Adds in the inventory item information & other widgets."""
		if self.add_new_flag:
			self.launchEditor() #Go straight to editor
		else:	
			self.name_label.configure(text=self.NAME_LABEL_STR.format(self.current_item.name))
			self.valve_num_label.configure(text=self.VALVE_NUM_LABEL_STR.format(self.current_item.valve_number))
			
			self.original_qty_label.configure(
			text=self.ORIG_QTY_LABEL_STR.format(self.current_item.org_quant))
			
			self.current_qty.configure(
			text=self.CUR_QTY_LABEL_STR.format(self.current_item.cur_quant))
			
			#place button when an item is selected
			self.replace_but.grid(row=4)


	def launchEditor(self):
		"""Launches the editor for changing inventory information."""
		print("Launching inventory editor.")
		self.top = tk.Toplevel(background=self.main_app.MASTER_BACKGROUND_COLOR)
		self.top.tk.call("wm","iconphoto",self.top._w,self.main_app.icon_img) 
		self.top.title("Inventory editor: ")
		#self.top.geometry("{0}x{1}+0+0".format(self.top_level.winfo_screenwidth()
		#										  ,self.top_level.winfo_screenheight()))
		self.top.protocol("WM_DELETE_WINDOW",self.deployCancelMessageBox)
		
		self.configureEditor()


	def configureEditor(self):
		"""Adds widgets to the editor top level."""
		name_label = tk.Label(self.top,text="Item Name:")
		name_label.grid(row=0,column=0)
		self.name_entry = tk.Entry(self.top)
		self.name_entry.grid(row=0,column=1,sticky="w")
		
		valve_num_label = tk.Label(self.top,text="Valve Number:")
		valve_num_label.grid(row=1,column=0)
		self.possible_valves = ttk.Combobox(self.top,values=self.valve_numbers)
		self.possible_valves.grid(row=1,column=1)
		
		original_qty_label = tk.Label(self.top,text="Initial Quantity (Ounces)")
		original_qty_label.grid(row=2,column=0)
		self.original_qty_entry = tk.Entry(self.top)
		self.original_qty_entry.grid(row=2,column=1,sticky="w")
		
		cur_qty_label = tk.Label(self.top,text="Current Quantity (Ounces)")
		cur_qty_label.grid(row=3,column=0)
		self.cur_qty_entry = tk.Entry(self.top)
		self.cur_qty_entry.grid(row=3,column=1,sticky="w")
		
		if self.add_new_flag:
			new_vals = ["Use new valve"]
			for num in self.valve_numbers:
				new_vals.append(num)
			self.possible_valves.configure(values=new_vals)
			save_but = ttk.Button(self.top,text="Save",command=self.processGivenData)
			save_but.grid()
		else:
			self.name_entry.insert(0,self.current_item.name)
			self.possible_valves.set(self.current_item.valve_number)
			self.original_qty_entry.insert(0,self.current_item.org_quant)
			self.cur_qty_entry.insert(0,self.current_item.cur_quant)
			change_but = ttk.Button(self.top,text="Replace",command=self.processGivenData)
			change_but.grid()
			

	def processGivenData(self):
		"""Retrieve information for entry & exits editor."""
		rtrv_name = self.name_entry.get()
		rtrv_valve_num = self.possible_valves.get()
		rtrv_org_qty = self.original_qty_entry.get()
		rtrv_cur_qty =self.cur_qty_entry.get()
		
		if rtrv_name == "" or rtrv_name == "" or rtrv_name == "" or rtrv_name == "":
			messagebox.showinfo("Error","Incomplete form!")
			return
		
		if self.add_new_flag:
			isNewValve= False
			if rtrv_valve_num == "Use new valve":
				rtrv_valve_num = len(self.inventory_items)+1
				isNewValve=True
				#make a new entry for a new valve
				
			new_inventory = Inventory(self.main_app.INVENTORY_FILE_PATH,
			rtrv_name.title(),float(rtrv_org_qty),float(rtrv_cur_qty),int(rtrv_valve_num))
			
			if isNewValve:
				new_inventory.addNewItem()
			else:
				#replace the item that was at the rtrv_valve_num's valve
				new_inventory.replaceItem(new_inventory.name,
							new_inventory.cur_quant,new_inventory.org_quant)
		else:
			
			isSameValve = str(rtrv_valve_num) == str(self.current_item.valve_number)
			isSameName = rtrv_name == self.current_item.name
			isSameOrgQuant = str(rtrv_org_qty) == str(self.current_item.org_quant)
			isSameCurQuant = str(rtrv_cur_qty) == str(self.current_item.cur_quant)
			
			if not isSameValve and isSameName and isSameOrgQuant and isSameCurQuant:
				#not the same valve, but same info = switch valve numbers
				self.current_item.switchValves(int(rtrv_valve_num))
			else: #update file in all other cases
				self.current_item.replaceItem(rtrv_name.title(),float(rtrv_cur_qty),float(rtrv_org_qty))

		#update inventory items			
		self.main_app.inventory_items = self.main_app.collectInventoryInfo()
		self.updateListbox()
		self.main_app.updateDrinkMenu()
		self.top.destroy() #close editor
		

	def updateListbox(self):
		"""Updates listbox content to show changes."""
		self.collectInventoryItemsInfo()
		self.inventory_options.delete(0,tk.END) #clear listbox
		self.populateListbox()


	def deployCancelMessageBox(self):
		"""Prompts user before closing editor."""
		if messagebox.askokcancel("Cancel","Are you sure? All progress will be lost.",parent=self.top):
			self.top.destroy()


	def deployExitMessageBox(self):
		"""Prompts user before closing window."""
		if messagebox.askokcancel("Quit","Are you sure?",parent=self.top_level):
			self.main_app.employee_window.inventory_manager.destroy()
			self.main_app.employee_window.master.deiconify()

