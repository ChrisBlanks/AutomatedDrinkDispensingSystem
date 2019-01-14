#!/usr/bin/env python3
"""
Programmer: Chris Blanks
Last Edited: 1/11/2019
Project: Automated Self-Serving System
Purpose: This script defines the AppWindow Class, which
the Employee and Customer windows inherit from.

"""

from tkinter import messagebox
from tkinter import ttk
import tkinter as tk

from PIL import Image
from PIL import ImageTk
import math


class AppWindow():
    background_color = "LightCyan3"
    bg_color_other = "mint cream"
    var = 10
    
    def __init__(self,main_app):
        """Provides basic functionality to each window of the main application."""
        self.main_app_instance = main_app
        pass

    def displayDrinkOptionsInGUI(self):
        """Displays each drink button/image/label in the GUI."""
        num_of_drinks = len(self.main_app.active_drink_objects)
        necessary_rows = math.ceil(num_of_drinks/5) #5 drinks fill up a row in the window
        width_of_bar = 25    #scrollbar width
        canvas_width = self.main_app.screen_width - width_of_bar
        canvas_height = self.main_app.screen_height
        scroll_width = self.main_app.screen_width  #fills up window
        # 2 rows fill up most of the screen, so the canvas height will be multiples of the screen height
        scroll_height = math.ceil(necessary_rows/2) * self.main_app.screen_height
        
        self.canvas = tk.Canvas(self.frame,width=canvas_width,height=canvas_height,bg = self.background_color,
                                scrollregion=(0,0,scroll_width,scroll_height))
        self.scrollbar = tk.Scrollbar(self.frame,width=width_of_bar,orient= tk.VERTICAL)
        self.scrollbar.pack(side=tk.LEFT,fill=tk.Y)

        self.canvas.config(yscrollcommand = self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
        self.scrollbar.config(command=self.canvas.yview)

        self.canvas_frame = tk.Frame(self.canvas,bg = self.background_color)
        #for widgets to be scrollable, a window(or frame in this case) must be made for the canvas
        self.canvas.create_window((0,0),window=self.canvas_frame,anchor="nw")
        
        drink_num = 0
        column_position = 0
        row_position = 0
        self.drink_option_references = []
        for drink in self.main_app.active_drink_objects:
            if column_position > 4:
                row_position = row_position + 2 #goes to next set of rows
                column_position = 0 #resets column position to fit all buttons
            drink_img = Image.open(drink.pic_location)
            drink_img = drink_img.resize((200,200),Image.ANTIALIAS)
            drink_photo = ImageTk.PhotoImage(drink_img)
            
            self.drink_button = ttk.Button(self.canvas_frame,image=drink_photo
                                          ,command=lambda drink_op= self.main_app.active_drink_objects[drink_num]: self.setupDrinkEvent(drink_op))
            self.drink_button.img_ref = drink_photo
            self.drink_button.grid(row =row_position,column=column_position, padx = 25
                                   ,pady = 15)

            drink.name =(drink.name).replace("_"," ")
            self.drink_label = ttk.Label(self.canvas_frame,text=(drink.name).title(),
                                        font=("Georgia","15","bold"))
            self.drink_label.grid(row=row_position+1,column=column_position)
            
            self.drink_option_references.append( (self.drink_button,self.drink_label) )
            
            column_position = column_position + 1
            drink_num = drink_num + 1


    def setupDrinkEvent(self,drink_option):
        """Changes current drink before initiating drink event."""
        self.current_drink = drink_option
        self.initiateDrinkEvent()


    def initiateDrinkEvent(self):
        """Initiates drink event """
        print("Drink #",int(self.current_drink.id_number)+1,": ",(self.current_drink.name).replace("_"," "))
        self.clearDrinkOptionsFromGUI()
        self.setupDrinkProfileInGUI()

            
    def clearDrinkOptionsFromGUI(self):
        """Clears drink option items in GUI in order to make room for the next window."""
        for item in self.drink_option_references:
            item[0].grid_forget()
            item[1].grid_forget()

        #must be discarded, so that grid widgets can be put in self.frame
        self.canvas.pack_forget()   
        self.scrollbar.pack_forget()


    def setupDrinkProfileInGUI(self):
        """Creates a drink profile for the current drink."""
        self.drink_profile_elements = []
        
        img = Image.open(self.current_drink.pic_location)
        img = img.resize((500,400),Image.ANTIALIAS)
        tk_photo = ImageTk.PhotoImage(img)
        self.img_item_reference = tk_photo #keeping a reference allows photo to display
        
        img_item = ttk.Label(self.frame,image=tk_photo)
        img_item.grid(row=0,column=0)

        name_of_drink = ttk.Label(self.frame,text=(self.current_drink.name).title())
        name_of_drink.grid(row=1,column=0)
        
        text_builder =" ".join(self.current_drink.ingredients).replace(' ',', ').replace('_',' ')
        ingredient_text = ttk.Label(self.frame,text="Ingredients: " + text_builder)
        ingredient_text.grid(row=0,column = 1,columnspan=10,sticky="n")


        if self.main_app.isEmployeeMode == False:
            drink_price_str = "Price: $"+str(self.current_drink.price)
            drink_price = tk.Label(self.frame,text= drink_price_str)
            drink_price.grid(row=1,column=2)
            
            buy_button = ttk.Button(self.frame,text="Buy?",command=self.startBuyEvent)
            buy_button.grid(row=2,column=2,sticky="nsew")

            self.drink_profile_elements.extend((buy_button,drink_price))
        else:
            quantity_label = ttk.Label(self.frame,text="Order Quantity:")
            quantity_label.grid(row=2,column=1,sticky="n")
            self.drink_profile_elements.append(quantity_label)
            
            for i in range(5):
                quantity_btn = ttk.Button(self.frame,text=str(i+1),
                                         command= lambda x = i+1: self.startEmployeeOrderEvent(x) )
                quantity_btn.configure(width=2)
                quantity_btn.grid(row= 2,column=i+2,padx=6,sticky="w")
                self.drink_profile_elements.append(quantity_btn)
        
        back_button = ttk.Button(self.frame, text="Back",command=self.resetDrinkOptions)
        back_button.grid(row=3,column=0)
            
        self.drink_profile_elements.extend((img_item,name_of_drink,ingredient_text,back_button))
         

    def startBuyEvent(self):
        """Starts the buying process for the customer mode."""
        self.isOrdered = self.displayConfirmationMessageBox()
        if self.isOrdered:
            pass

			
    def startEmployeeOrderEvent(self,num_of_drinks):
        """Starts the ordering process for the employee mode."""
        self.isOrdered = self.displayConfirmationMessageBox("Employee",num_of_drinks)
        if self.isOrdered:
            pass

			
    def displayConfirmationMessageBox(self,mode="Customer",num_of_drinks=1):
        """Asks the user if they are sure about their drink selection """
        if mode == "Customer":
            if messagebox.askokcancel("Confirmation","Are you sure that you want a "+self.current_drink.name+"?",
                                      parent=self.master):
                print("Order is confirmed.")
                print("One order of "+self.current_drink.name +" on the way.")

                msg = "1 "+ self.current_drink.name + " was ordered."
                self.main_app_instance.writeToDrinkSalesLog(msg)
                return True
            else:
                return False
        else:
            if messagebox.askokcancel("Confirmation",
                                      "Are you sure that you want "+str(num_of_drinks)+" "+self.current_drink.name.title().replace("_"," ")+"(s) ?",
                                      parent=self.master):
                print("Order is confirmed.")
                print( str(num_of_drinks)+" order(s) of "+self.current_drink.name +" on the way.")
                if num_of_drinks == 1:
                    msg = str(num_of_drinks)+" "+ self.current_drink.name + " was ordered."
                elif num_of_drinks > 1:
                    msg = str(num_of_drinks)+" "+ self.current_drink.name + "s were ordered."
                self.main_app_instance.writeToDrinkSalesLog(msg)
                return True
            else:
                return False
            
   
    def resetDrinkOptions(self):
        for element in self.drink_profile_elements:
            element.grid_forget()
        self.displayDrinkOptionsInGUI()


    def createHelpMenu(self,menu_name=""):
        """Defines a menu that offers information about the machine."""
        help_menu = tk.Menu(self.parent_menu,tearoff=0)
        self.parent_menu.add_cascade(label=menu_name, menu= help_menu)

        help_menu.add_separator()
        help_menu.add_command(label="", command= self.secret) #allows exit out of customer window  
        help_menu.add_separator()

        #for employee window
        if menu_name != "":
            help_menu.add_separator()
            help_menu.add_command(label="How to operate", command= self.showOperationInstructions)
            help_menu.add_separator()
            
            help_menu.add_command(label="Info About Contributors",command=self.showContributors)
            help_menu.add_separator()

        
    def secret(self):
        """Does a secret action."""
        self.var = self.var - 1
        if self.var == 0:
            self.master.destroy()
            self.main_app.master.deiconify()

        
    def showContributors(self):
        """Lists contributors of the project in a top level window's message box."""
        top = tk.Toplevel()
        top.tk.call("wm","iconphoto",top._w,self.main_app.icon_img)
        top.attributes('-topmost','true')
        top.title("Contributors:")
        top.geometry("350x280")
        
        self.contributors_msg = tk.Message(top)
        msg= """Nathan Bane:\nEmbedded Systems Design\n\nChris Blanks:\nSoftware Design
\nRyan Valente:\nMechanical Design\n\n University of Maryland Eastern Shore\n\nContact >>> Cablanks@umes.edu
\nIcon Creator: RoundIcons\nhttps://www.flaticon.com/authors/roundicons"""
        self.contributors_msg.config(text=msg,font= ("Arial",12,""))
        self.contributors_msg.grid()

        
    def showOperationInstructions(self):
        """Instructs the user on how to order from the GUI."""
        with open(self.operation_instructions_file_path,'r') as file:
            lines = file.readlines()
        
        msg = " ".join(lines)
        
        top = tk.Toplevel()
        
        top.tk.call("wm","iconphoto",top._w,self.main_app.icon_img)
        top.attributes('-topmost','true')
        top.title("How to Operate:")
        top.geometry("600x230")
        
        
        scroll = tk.Scrollbar(top,orient= tk.VERTICAL)
        scroll.grid(row=0,column=1,sticky="ns")
        
        canvas = tk.Canvas(top,width=350,
                           height=230,
                           scrollregion=(0,0,2000,2000))
        canvas.grid(row=0,column=0,sticky="nsew")

        scroll.config(command=canvas.yview)
        canvas.config(yscrollcommand = scroll.set)
        canvas.create_text((0,0),text=msg,anchor="nw") #top left and anchored to the right
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)
        








        

