#!/usr/bin/env python3
"""
Programmer: Chris Blanks
Last Edited: 11/10/2018
Project: Automated Self-Serving System
Purpose: This script defines the DrinkProfileManager class
that offers editing features to the regular employee and manager.

Note:
    - The amount of file IO can be reduced greatly
"""

from tkinter import messagebox
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk

import os

#my classes
from DrinkProfile import DrinkProfile
from EmbeddedKeyboard import EmbeddedKeyboard
from AppWindow import AppWindow


class DrinkProfileManager:
    def __init__(self,master,main_app,admin_mode):
        self.master = master
        self.main_app = main_app
        self.admin_mode = admin_mode
        self.font1 = ("Georgia",12,"")
        
        self.current_inventory = self.main_app.inventory_items
        self.inventory_names = self.getInventoryNames()
        
        self.delete_button = None
        self.edit_button = None
        
        self.configureWindow()
        
        
    def configureWindow(self):
        """Sets window geometry and exit before launching profile manager."""
        self.master.configure(width=self.main_app.screen_width,
        height=self.main_app.screen_height,background=self.main_app.MASTER_BACKGROUND_COLOR)
        
        self.main_app.employee_window.top.protocol("WM_DELETE_WINDOW",self.deployExitMessageBox)
        self.createProfileManagerMainWindow()


    def getInventoryNames(self):
        """Gets all inventory names and returns as a list."""
        names = ["None"]
        for item in self.current_inventory:
            names.append(item.name)

        return names


    def createProfileManagerMainWindow(self):
        """Creates the main window of the profile manager."""
        self.drinks = tk.Listbox(self.master,font=("Georgia",16,"bold"))
        self.drinks.bind('<<ListboxSelect>>',self.listboxCallback)
        self.names = []
        
        self.drinks.insert(1,"Add A New Drink")
        count = 2
        for drink in self.main_app.all_drinks:
            self.drinks.insert(count,drink.name.title())
            self.names.append(drink.name.replace("_"," ").title())
            count +=1
        
        self.master.add(self.drinks)
        self.drink_selected = None
        
        self.canvas = tk.Canvas(self.master,background=self.main_app.MASTER_BACKGROUND_COLOR)
        
        drink_name = tk.Label(self.canvas,text="Name: ",font=self.font1)
        drink_name.grid(row=0,column=0)
        self.name_var = tk.StringVar()
        cur_drink_name = tk.Label(self.canvas,textvariable=self.name_var,font=self.font1)
        cur_drink_name.grid(row=0,column=1)


        drink_id = tk.Label(self.canvas,text="Drink Id: ",font=self.font1)
        drink_id.grid(row=1,column=0)
        self.id_var = tk.StringVar()
        cur_id = tk.Label(self.canvas,textvariable=self.id_var,font=self.font1)
        cur_id.grid(row=1,column=1)


        drink_ingredients= tk.Label(self.canvas,text="Ingredients: ",font=self.font1)
        drink_ingredients.grid(row=2,column=0)
        self.ingredients_var = tk.StringVar()
        cur_ingredients = tk.Label(self.canvas,textvariable=self.ingredients_var,font=self.font1)
        cur_ingredients.grid(row=2,column=1)
        

        pic_loc = tk.Label(self.canvas,text="Image Location: ",font=self.font1)
        pic_loc.grid(row=3,column=0)
        self.pic_loc_var = tk.StringVar()
        cur_loc = tk.Label(self.canvas,textvariable=self.pic_loc_var,font=self.font1)
        cur_loc.grid(row=3,column=1)


        price = tk.Label(self.canvas,text="Price: ",font=self.font1)
        price.grid(row=4,column=0)
        self.price_var = tk.StringVar()
        cur_price = tk.Label(self.canvas,textvariable=self.price_var,font=self.font1)
        cur_price.grid(row=4,column=1)
        

        active = tk.Label(self.canvas,text="Active Drink: ",font=self.font1)
        active.grid(row=5,column=0)
        self.active_var = tk.StringVar()
        cur_active = tk.Label(self.canvas,textvariable=self.active_var,font=self.font1)
        cur_active.grid(row=5,column=1)
        
        self.master.add(self.canvas)
        self.master.grid()
        

    def listboxCallback(self,event):
        """What's selected in the listbox is displayed in main window"""
        if self.edit_button != None:
            self.edit_button.grid_forget()
        if self.delete_button != None:
            self.delete_button.grid_forget()
            
        try:
            self.drink_selected = self.drinks.get(self.drinks.curselection())
            index = self.drinks.index(self.drinks.curselection())
        except tk._tkinter.TclError:
            return #suppresses empty listbox error
        
        if self.drink_selected == "Add A New Drink":
            self.createNewDrink()
        elif self.drink_selected in self.names:
            drink_to_display = None
            for drink in self.main_app.all_drinks:
                if self.drink_selected == drink.name.title():
                    drink_to_display = drink
                
            self.name_var.set(drink_to_display.name.replace("_"," "))
            self.id_var.set(str(drink_to_display.id_number))
            self.ingredients_var.set(drink_to_display.ingredients)
            self.pic_loc_var.set(drink_to_display.pic_location)
            self.active_var.set(str(drink_to_display.isActive))
            self.price_var.set(str(drink_to_display.price))

            self.edit_button = tk.Button(self.canvas,text="Edit",font=self.font1,bg="Orange",
                                    command=lambda x=drink_to_display: self.launchEditor(x))
            self.edit_button.grid(row=6,column=0)
            if self.admin_mode:
                self.delete_button = tk.Button(self.canvas,text="Delete",font=self.font1,bg="red",
                                    command=lambda x=drink_to_display: self.deployDeleteMessageBox(x,index))
                self.delete_button.grid(row=6,column=1)
        else:
            pass
        
         
    def createNewDrink(self):
        """A variation on the launchEditor() that creates a new drink."""
        self.new_drink = DrinkProfile(main_directory=self.main_app.MAIN_DIRECTORY_PATH)
        self.launchEditor(None,"Make A New Drink")
        self.main_app.employee_window.top.withdraw()

        
    def launchEditor(self,drink=None,title=None):
        """Launches an editor with an embedded keyboard"""
        if drink == None:
            title = "Make A New Drink"
        else:
            title = drink.name
        self.top = tk.Toplevel(background=self.main_app.MASTER_BACKGROUND_COLOR)
        self.top.tk.call("wm","iconphoto",self.top._w,self.main_app.icon_img) 
        self.top.title("Drink editor: " + title)
        self.top.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth()
                                                  ,self.master.winfo_screenheight()))
        self.top.protocol("WM_DELETE_WINDOW",self.deployCancelMessageBox)
        self.drinkToEdit = drink
        self.configureEditor(title)

        
    def configureEditor(self,title):
        """Sets up the window for editing drink profiles."""
        name_label = tk.Label(self.top,text="Name:")
        name_label.grid(row=1,column=0)
        self.name_entry = tk.Entry(self.top,width=138)
        self.name_entry.grid(row=1,column=1,sticky="w",pady=4)
        if title != "Make A New Drink":
            self.name_entry.insert(0,self.drinkToEdit.name)
        
        id_label = tk.Label(self.top,text="Id:")
        id_label.grid(row=2,column=0)
        self.id_entry = tk.Entry(self.top,width=138)
        self.id_entry.grid(row=2,column=1,sticky="w",pady=4)
        if title != "Make A New Drink":
            self.id_entry.insert(0,self.drinkToEdit.id_number)

        pic_loc_label = tk.Label(self.top,text="Image path:")
        pic_loc_label.grid(row=5,column=0)
        self.pic_loc_entry = tk.Entry(self.top,width=138)
        self.pic_loc_entry.grid(row=5,column=1,sticky="w",pady=4)
        if title != "Make A New Drink":
            self.pic_loc_entry.insert(0,self.drinkToEdit.pic_location)

        price_label = tk.Label(self.top,text="Price:")
        price_label.grid(row=6,column=0)
        self.price_entry = tk.Entry(self.top,width=138)
        self.price_entry.grid(row=6,column=1,sticky="w",pady=4)
        if title != "Make A New Drink":
            self.price_entry.insert(0,self.drinkToEdit.price)

        active_label = tk.Label(self.top,text="Active Drink:")
        active_label.grid(row=7,column=0)
        self.active_entry = tk.Entry(self.top,width=138)
        self.active_entry.grid(row=7,column=1,sticky="w",pady=4)
        
        if title != "Make A New Drink":
            ingredient_buffer = []
            drink_edit_names= " ".join(self.drinkToEdit.ingredients)
            for name in self.inventory_names:
                if name in drink_edit_names.replace("_"," ").title():
                    ingredient_buffer.append(name)
            
            if len(ingredient_buffer) < 4:
                for i in range(4-len(ingredient_buffer)):
                    ingredient_buffer.append("None")
            
            ordered_ounces = []
            list_of_OZ= self.drinkToEdit.ounces
            for oz in list_of_OZ:
                ordered_ounces.append(oz)
            print(ordered_ounces)    
            if len(ordered_ounces) < 4:
                for i in range(4-len(ordered_ounces)):
                    ordered_ounces.append(" ")
            
            #ingredients setions
            ingredient_canvas = tk.Canvas(self.top,background=self.main_app.MASTER_BACKGROUND_COLOR)
            
            ingredients_section1 = tk.Label(ingredient_canvas,text="Ingredient 1:")
            ingredients_section1.grid(row=0,column=0)
            
            self.ingredient_options1 = ttk.Combobox(ingredient_canvas,values=self.inventory_names)
            self.ingredient_options1.grid(row=0,column=1)
            self.ingredient_options1.set(ingredient_buffer[0])
            
            self.Ounce_entry1 = tk.Entry(ingredient_canvas,width=20)
            self.Ounce_entry1.insert(0,ordered_ounces[0])
            self.Ounce_entry1.grid(row=0,column=2,sticky="w",pady=4)
            
            ounce_label1 = tk.Label(ingredient_canvas,text="Ounce(s)")
            ounce_label1.grid(row=0,column=3)
            
            ingredients_section2 = tk.Label(ingredient_canvas,text="Ingredient 2:")
            ingredients_section2.grid(row=1,column=0)
            
            self.ingredient_options2 = ttk.Combobox(ingredient_canvas,values=self.inventory_names)
            self.ingredient_options2.grid(row=1,column=1)
            self.ingredient_options2.set(ingredient_buffer[1])
            
            self.Ounce_entry2 = tk.Entry(ingredient_canvas,width=20)
            self.Ounce_entry2.insert(0,ordered_ounces[1])
            self.Ounce_entry2.grid(row=1,column=2,sticky="w",pady=4)
            
            ounce_label2 = tk.Label(ingredient_canvas,text="Ounce(s)")
            ounce_label2.grid(row=1,column=3)
            
            ingredients_section3 = tk.Label(ingredient_canvas,text="Ingredient 3:")
            ingredients_section3.grid(row=2,column=0)
            
            self.ingredient_options3 = ttk.Combobox(ingredient_canvas,values=self.inventory_names)
            self.ingredient_options3.grid(row=2,column=1)
            self.ingredient_options3.set(ingredient_buffer[2])
            
            self.Ounce_entry3 = tk.Entry(ingredient_canvas,width=20)
            self.Ounce_entry3.insert(0,ordered_ounces[2])
            self.Ounce_entry3.grid(row=2,column=2,sticky="w",pady=4)
            
            ounce_label3 = tk.Label(ingredient_canvas,text="Ounce(s)")
            ounce_label3.grid(row=2,column=3)        
            
            ingredients_section4 = tk.Label(ingredient_canvas,text="Ingredient 4:")
            ingredients_section4.grid(row=3,column=0)
            
            self.ingredient_options4 = ttk.Combobox(ingredient_canvas,values=self.inventory_names)
            self.ingredient_options4.grid(row=3,column=1)
            self.ingredient_options4.set(ingredient_buffer[3])
            
            self.Ounce_entry4 = tk.Entry(ingredient_canvas,width=20)
            self.Ounce_entry4.grid(row=3,column=2,sticky="w",pady=4)
            self.Ounce_entry4.insert(0,ordered_ounces[3])
            ounce_label4 = tk.Label(ingredient_canvas,text="Ounce(s)")
            ounce_label4.grid(row=3,column=3)        
            
            ingredient_canvas.grid(column=1,sticky="s")
            
        else:
            ingredient_canvas = tk.Canvas(self.top,background=self.main_app.MASTER_BACKGROUND_COLOR)
            
            ingredients_section1 = tk.Label(ingredient_canvas,text="Ingredient 1:")
            ingredients_section1.grid(row=0,column=0)
            
            self.ingredient_options1 = ttk.Combobox(ingredient_canvas,values=self.inventory_names)
            self.ingredient_options1.grid(row=0,column=1)
            
            self.Ounce_entry1 = tk.Entry(ingredient_canvas,width=20)
            self.Ounce_entry1.grid(row=0,column=2,sticky="w",pady=4)
            
            ounce_label1 = tk.Label(ingredient_canvas,text="Ounce(s)")
            ounce_label1.grid(row=0,column=3)
            
            ingredients_section2 = tk.Label(ingredient_canvas,text="Ingredient 2:")
            ingredients_section2.grid(row=1,column=0)
            
            self.ingredient_options2 = ttk.Combobox(ingredient_canvas,values=self.inventory_names)
            self.ingredient_options2.grid(row=1,column=1)
            
            self.Ounce_entry2 = tk.Entry(ingredient_canvas,width=20)
            self.Ounce_entry2.grid(row=1,column=2,sticky="w",pady=4)
            
            ounce_label2 = tk.Label(ingredient_canvas,text="Ounce(s)")
            ounce_label2.grid(row=1,column=3)
            
            ingredients_section3 = tk.Label(ingredient_canvas,text="Ingredient 3:")
            ingredients_section3.grid(row=2,column=0)
            
            self.ingredient_options3 = ttk.Combobox(ingredient_canvas,values=self.inventory_names)
            self.ingredient_options3.grid(row=2,column=1)
            
            self.Ounce_entry3 = tk.Entry(ingredient_canvas,width=20)
            self.Ounce_entry3.grid(row=2,column=2,sticky="w",pady=4)
            
            ounce_label3 = tk.Label(ingredient_canvas,text="Ounce(s)")
            ounce_label3.grid(row=2,column=3)        
            
            ingredients_section4 = tk.Label(ingredient_canvas,text="Ingredient 4:")
            ingredients_section4.grid(row=3,column=0)
            
            self.ingredient_options4 = ttk.Combobox(ingredient_canvas,values=self.inventory_names)
            self.ingredient_options4.grid(row=3,column=1)
            
            self.Ounce_entry4 = tk.Entry(ingredient_canvas,width=20)
            self.Ounce_entry4.grid(row=3,column=2,sticky="w",pady=4)
            
            ounce_label4 = tk.Label(ingredient_canvas,text="Ounce(s)")
            ounce_label4.grid(row=3,column=3)        
            
            ingredient_canvas.grid(column=1,sticky="s")
        
        
        if title != "Make A New Drink":
            self.active_entry.insert(0,self.drinkToEdit.isActive)

        pic_select_button = tk.Button(self.top,text="Find Pic!", command=self.selectAnImage)
        pic_select_button.grid(row=4,column=0)
    
        entries = (self.name_entry,self.id_entry,self.pic_loc_entry,
                   self.price_entry,self.active_entry)
        
        keyboard_canvas = tk.Canvas(self.top,width=100,height=350,
                                    background=self.main_app.MASTER_BACKGROUND_COLOR)
        embed_keyboard = EmbeddedKeyboard(keyboard_canvas,entries)
        keyboard_canvas.grid(column=1,sticky="s")
        if title == "Make A New Drink":
            create_button = tk.Button(self.top,text="Create",bg="green",fg="white",
                                    command=self.createNewProfile)
            create_button.grid(column=0,sticky="new",rowspan=2)
            #create_button.grid(row=0,column=0,sticky="new",rowspan=2)
        else:
            save_button = tk.Button(self.top,text="Save",bg="green",fg="white",
                                command=self.saveChanges)
            save_button.grid(column=0,sticky="new",rowspan=2)
            #save_button.grid(row=0,column=0,sticky="new",rowspan=2)


    def selectAnImage(self):
        """Prompts the user to select an image for a drink &
        inserts it into the entry box for image location. """
        self.pic_path = filedialog.askopenfilename(initialdir="/home"
                                                   ,title="Select Drink Image (jpeg or png)"
                                                   ,filetypes=(("jpeg files","*.jpg"),("png files","*.png"))
                                                   ,parent=self.top)
        if self.pic_path == "":
            print("User canceled")
        elif ".jpg" in self.pic_path:
            print("Picture Path(new): "+self.pic_path)
            self.pic_loc_entry.delete(0,tk.END)
            self.pic_loc_entry.insert(0,self.pic_path)
        else:
            print("No support for other image types (i.e. png)")
            

        
    def createNewProfile(self):
        """Creates a drink profile from the given parameters"""
        self.new_drink.name = self.name_entry.get()
        self.new_drink.id_number = self.id_entry.get()
        pic_path = self.pic_loc_entry.get()
        self.new_drink.price = self.price_entry.get()
        self.new_drink.isActive = self.active_entry.get()
        
        #get ingredients
        ingredient1 = self.ingredient_options1.get()
        ounce_1 = self.Ounce_entry1.get() 
        
        ingredient2 = self.ingredient_options2.get()
        ounce_2 = self.Ounce_entry2.get() 

        ingredient3 = self.ingredient_options3.get()
        ounce_3 = self.Ounce_entry3.get() 

        ingredient4 = self.ingredient_options4.get()
        ounce_4 = self.Ounce_entry4.get() 
        
        
        ingre = "{} {} {} {}".format(ingredient1,ingredient2,
                                        ingredient3,ingredient4)
        ingre.replace("None","").lower().replace(" juice","_juice").replace(" sec","_sec")
        ounces = "{} {} {} {}".format(ounce_1,ounce_2,
                                        ounce_3,ounce_4)
        print("Ingredients:",ingre)
        print("Ounces:",ounces)
        
        
        self.new_drink.name = (self.new_drink.name).replace(" ","_") #prevents spaces in drink profile names
        if self.new_drink.name == "" or self.new_drink.id_number == "" or self.new_drink.ingredients == "" or \
           pic_path == "" or self.new_drink.price == "" or self.new_drink.isActive == "":
            self.deployIncompleteMessageBox()  #if any empty, show warning#if any empty, show warning
            return
        
        # Processing of ingredients
        #temp_edit = self.new_drink.ingredients.replace(","," ") #get rid of commas
        #self.new_drink.ingredients = temp_edit 
        #must be a space delimited string when creating a new drink profile
        self.new_drink.ingredients = ingre
        self.new_drink.ounces = ounces
        
        #limited for right now
        if ".jpg" in pic_path:
            self.new_drink.pic_extension = ".jpg"
        elif ".png" in pic_path:
            self.new_drink.pic_extension = ".png"   
        else:
            #will give it a dummy pic
            pic_path = "/home/pi/Pictures/drink.jpg"
            self.new_drink.pic_extension = ".jpg"
            
           
        self.new_drink.createDrinkProfile(pic_path)
        
        self.new_drink.ingredients = ingre.split()
        self.new_drink.ounces  = ounces.split()
        #split into a list by space delimiters for correct format in drink profile display
        
        self.main_app.all_drinks.append(self.new_drink)
        self.main_app.active_drink_objects.append(self.new_drink)
        self.main_app.writeToLog("Created new drink: "+self.new_drink.name)
        self.deploySuccesfulMessageBox()
        
        
        self.main_app.active_drink_objects = self.main_app.getDrinks()
        self.main_app.updateDrinkMenu()
        


    def deleteDrink(self,drink,index):
        """Deletes drink arg and cleans it from config file."""
        drink.deleteDrinkProfile()
        drinkTrash = drink
        for el in self.main_app.active_drink_objects:
            if el.name == drinkTrash.name:
                self.main_app.active_drink_objects.remove(drink)
                self.main_app.all_drinks.remove(drink)
                del drink
        self.drinks.delete(index)
        self.main_app.cleanOldDrinksFromConfig()
        dir(self.main_app.employee_window)
        #issue: self.main_app.employee_window.resetDrinkOptions()

        
    def saveChanges(self):
        """Checks for changed fields and puts into effect the changes."""
        new_name = self.name_entry.get()
        new_id = self.id_entry.get()
        
        new_pic_loc = self.pic_loc_entry.get()    #would have to parse and update extension here
        new_price = self.price_entry.get()
        new_active_condition = self.active_entry.get()
        
        #get ingredients
        ingredient1 = self.ingredient_options1.get()
        ounce_1 = self.Ounce_entry1.get() 
        
        ingredient2 = self.ingredient_options2.get()
        ounce_2 = self.Ounce_entry2.get() 

        ingredient3 = self.ingredient_options3.get()
        ounce_3 = self.Ounce_entry3.get() 

        ingredient4 = self.ingredient_options4.get()
        ounce_4 = self.Ounce_entry4.get() 
        
        ingre = "{} {} {} {}".format(ingredient1,ingredient2,
                                        ingredient3,ingredient4)
        ingre = ingre.replace("None",
        "").lower().replace(" juice","_juice").replace(" sec","_sec")
        
        ounces = "{} {} {} {}".format(ounce_1,ounce_2,
                                        ounce_3,ounce_4)
        print("Ingredients:",ingre)
        print("Ounces:",ounces)
        new_ingredients = ingre
        

        if new_name == "" or new_id == "" or new_ingredients == "" or new_pic_loc == "" \
           or new_price == "" or new_active_condition == "":
            self.deployIncompleteMessageBox()
            return
        
        if new_id != "" and new_id != self.drinkToEdit.id_number:
            self.drinkToEdit.id_number = new_id
            self.changeIdNum()
        if new_name != "" and new_name != self.drinkToEdit.name:
            self.drinkToEdit.name = new_name
            self.changeName()
        if new_ingredients != "" and new_ingredients != self.drinkToEdit.ingredients:
            print(new_ingredients)
            self.drinkToEdit.ingredients = new_ingredients
            self.changeIngredients()
        if ounces != "" and ounces != self.drinkToEdit.ounces:
            self.drinkToEdit.ounces = ounces
            self.changeOunces()
        if new_pic_loc != "" and new_pic_loc != self.drinkToEdit.pic_location:
            self.changeDrinkPicLocation(self.drinkToEdit,new_pic_loc)
        if new_price != ""  and new_price != self.drinkToEdit.price:
            self.drinkToEdit.price = new_price
            self.changePrice()
        if new_active_condition != self.drinkToEdit.isActive:
            if str(new_active_condition) == "1":
                print("active")
                self.makeActive(self.drinkToEdit)
            elif str(new_active_condition) == "0":
                print("not active")
                self.deactivateDrink(self.drinkToEdit)
            else:
                print("Incorrect state for isActive")
        
        self.main_app.updateDrinkMenu()
        self.main_app.writeToLog("Edited this drink: "+ self.drinkToEdit.name)
        self.top.destroy()


    def changeIdNum(self):
        """Changes drink id in its respective text file."""
        self.drinkToEdit.edited_attributes[0] = self.drinkToEdit.id_number
        self.drinkToEdit.editDrinkProfile()


    def changeName(self):
        """Changes drink name in its respective text file."""
        self.drinkToEdit.edited_attributes[1] = self.drinkToEdit.name
        self.drinkToEdit.editDrinkProfile()


    def changeIngredients(self):
        """Changes drink ingredients in its respective text file."""   
        self.drinkToEdit.edited_attributes[2] = self.drinkToEdit.ingredients
        self.drinkToEdit.editDrinkProfile()
        self.drinkToEdit.ingredients = self.drinkToEdit.ingredients.split()                            
    
    def changeOunces(self):
        """Changes ounces value. """
        self.drinkToEdit.edited_attributes[7] = self.drinkToEdit.ounces
        self.drinkToEdit.editDrinkProfile()
        self.drinkToEdit.ounces = self.drinkToEdit.ounces.split()
    
    def changePrice(self):
        """Changes drink name in its respective text file."""
        self.drinkToEdit.edited_attributes[6] = self.drinkToEdit.price
        self.drinkToEdit.editDrinkProfile()

    
    def makeActive(self,drink):
        """Makes inactive drinks active."""
        drink.isActive = "1"
        drink.edited_attributes[5] = drink.isActive
        drink.editDrinkProfile()


    def deactivateDrink(self,drink):
        """Makes active drinks inactive."""
        drink.isActive = "0"
        drink.edited_attributes[5] = drink.isActive
        drink.editDrinkProfile()

    
    def changeDrinkPicLocation(self,drink,new_pic_path):
        """Updates the drink path/location"""
        if os.path.exists(new_pic_path):
            drink.pic_location = new_pic_path
            drink.edited_attributes[3] = drink.pic_location
            drink.editDrinkProfile()
        else:
            print("Path does not exist.")


    def deploySuccesfulMessageBox(self):
        """Advises the user to finish making the new drink """
        if messagebox.showinfo("Successful!","Press Ok to continue...",parent=self.top):
            self.top.destroy()
            self.main_app.employee_window.master.deiconify()


    def deployDeleteMessageBox(self,drink,index):
        """Advises the user to finish making the new drink """
        if messagebox.askokcancel("Delete","Are you sure that you want to delete this drink?",parent=self.master):
            self.main_app.writeToLog("Deleted this drink: "+drink.name)
            self.deleteDrink(drink,index)

            
    def deployIncompleteMessageBox(self):
        """Advises the user to finish making the new drink """
        if messagebox.showwarning("Incomplete","Please fill all fields.",parent=self.top):
            pass

        
    def deployCancelMessageBox(self):
        """Prompts user before closing editor."""
        if messagebox.askokcancel("Cancel","Are you sure? All progress will be lost.",parent=self.top):
            self.top.destroy()
            self.main_app.employee_window.top.deiconify()
            
                
    def deployExitMessageBox(self):
        """Prompts user before closing window."""
        if messagebox.askokcancel("Quit","Are you sure?",parent=self.master):
            self.main_app.employee_window.master.deiconify()
            self.main_app.employee_window.top.destroy()
            
