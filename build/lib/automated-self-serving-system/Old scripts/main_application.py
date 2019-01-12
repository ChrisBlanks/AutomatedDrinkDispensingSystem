"""
Programmer: Chris Blanks
Last Edited: 10/13/2018
Project: Automated Self-Serving System
Purpose:
    This script defines the high level functionality of the
    main application for this project.

To-Do:
    -more features (e.g. login screen, help window)
   *-create methods for updating/checking the config and data files
   *-store any used file path into a member variable
   *-method to change state in config file or make it a class thing
"""

#Needed for linux machines:
#! /usr/bin/env python3

import tkinter as tk
from PIL import Image,ImageTk
import os

#my scripts
import callback_functions as Cb_func
import DrinkProfile as DP_class

class MainApplication(tk.Frame):

    #member variables
    title = "Drink Mixer 1.0"
    default_menu_message = """Hello, User! This is the Drink Mixer 1.0\n
    Please, select a drink from the top left menu!"""
    config_file_path = "/Users/Cabla/Documents/PYTHON_MODULES/SENIOR_DESIGN_CODE/system_info/config.txt"
    drink_names = [] #a list of drink names for reference
    drink_profile_directory = "/Users/Cabla/Documents/PYTHON_MODULES/SENIOR_DESIGN_CODE/drink_profiles"
    isLocked = False #controls which entities can read and write the data/config files
    
    def __init__(self, master=None):
        super(MainApplication,self).__init__(master)

        self.parent_menu = tk.Menu(self)
        self.master.config(menu=self.parent_menu)

        self.drink_objects = self.getDrinks()
        self.retrieveConfigurationInformation()
        self.configureWindow()
        self.createDrinkMenu()
        self.createOptionsMenu()
        self.displayDrinkOptionsInGUI()
        #self.createIdleApplicationLabel()
        
        self.grid()

    def getDrinks(self):
        """Retrieves a list of Drink objects."""
        temp = []
        os.chdir(self.drink_profile_directory)
        drink_profile_names = os.listdir(os.getcwd())
        for name in drink_profile_names:
            path_builder = self.drink_profile_directory +"/"+ name
            os.chdir(path_builder)
            drink = DP_class.DrinkProfile(path_builder +"/"+ os.listdir(os.getcwd())[1])
            temp.append(drink)
        return temp
    
    def retrieveConfigurationInformation(self):
        """Retrieves configuration info (e.g. drink names) from config file """
        f = open(self.config_file_path,'r+')
        lines = f.read().splitlines()
        print("'{}' contents:\n".format((f.name).split("/")[-1]),'\n'.join(lines))
        line_number = 1
        for line in lines:
            if line_number == 1:
                if line.split()[1] == '0':
                    print("Config file is not locked.\n\n")
                else:
                    self.isLocked = True
                    print("Config file is locked.\n\n")
            if line_number == 2:
                drinks = line.split(" ")
                for i in range(len(drinks)-1):
                    self.drink_names.append(drinks[i+1])
            line_number+=1        
        f.close()
    
    def configureWindow(self):
        """Sets the window's size to be screen's size and sets the title"""
        self.master.title(self.title)
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth()
                                                  ,self.master.winfo_screenheight()))
        self.master.resizable(width=False, height=False)

    def createDrinkMenu(self):
        """Creates a menu list of drinks"""
        drink_menu = tk.Menu(self.parent_menu)
        self.parent_menu.add_cascade(label="Drink Menu",menu=drink_menu)
        count = 0
        for drink in self.drink_objects:
            self.current_drink = drink #sets argument for drinkCallback()
            #lambda function allows identification of which menu button has been pressed
            drink_menu.add_command(label=self.current_drink.name
                                   ,command= lambda drink_op=self.drink_objects[count]: self.initiateDrinkEvent(drink_op))
            drink_menu.add_separator()
            count += 1

    def displayDrinkOptionsInGUI(self):
        """Displays each drink button/image/label in the GUI."""
        drink_num = 0
        column_position = 0
        row_position = 0
        self.drink_option_references = []
        for drink in self.drink_objects:
            if column_position > 4:
                row_position = 2
                column_position = 0 #resets column position to fit all buttons
            drink_img = Image.open(drink.picture_path)
            drink_img = drink_img.resize((200,200),Image.ANTIALIAS)
            drink_photo = ImageTk.PhotoImage(drink_img)
            
            self.drink_button = tk.Button(self,image=drink_photo,bg="white"
                                          ,command=lambda drink_op=self.drink_objects[drink_num]: self.initiateDrinkEvent(drink_op))
            self.drink_button.img_ref = drink_photo
            self.drink_button.grid(row =row_position,column=column_position, padx = 10,pady = 10)
            
            self.drink_label = tk.Label(self,text=drink.name)
            self.drink_label.grid(row=row_position+1,column=column_position)
            
            self.drink_option_references.append( (self.drink_button,self.drink_label) )
            
            column_position = column_position + 1
            drink_num = drink_num + 1

    def clearDrinkOptionsFromGUI(self):
        """Clears drink option items in GUI in order to make room for the next window."""
        for item in self.drink_option_references:
            item[0].grid_forget()
            item[1].grid_forget()


    def setupDrinkProfileInGUI(self):
        """Creates a drink profile for the current drink."""
        img = Image.open(self.current_drink.picture_path)
        img = img.resize((500,400),Image.ANTIALIAS)
        tk_photo = ImageTk.PhotoImage(img)

        self.img_item = tk.Label(self,image=tk_photo)
        self.img_item_reference = tk_photo
        self.img_item.grid()
        
        text_builder =" ".join(self.current_drink.ingredients).replace(' ',', ').replace('_',' ')
        self.ingredient_text = tk.Label(self,text="Ingredients: " + text_builder)
        self.ingredient_text.grid(row=0,column = 1,columnspan=5)

        self.back_button = tk.Button(self, text="Back",bg="white",fg="red",command=self.resetDrinkOptions)
        self.back_button.grid()
        

    def resetDrinkOptions(self):
        """Brings drink options back to GUI."""
        self.img_item.grid_forget()
        self.ingredient_text.grid_forget()
        self.back_button.grid_forget()
        self.displayDrinkOptionsInGUI()

        
    def createOptionsMenu(self):
        """Creates a menu list of options """
        options_menu = tk.Menu(self.parent_menu)
        self.parent_menu.add_cascade(label="Options",menu=options_menu)

        options_menu.add_command(label="Account Login",command=self.attachLoginOption)
        options_menu.add_separator()
        options_menu.add_command(label="Help?",command=self.attachHelpOption)
        options_menu.add_separator()
        

    def createIdleApplicationLabel(self):
        """Creates the labels for the application."""
        self.menu_message_str = tk.StringVar(self)
        self.menu_message_str.set(self.default_menu_message)
        self.main_label = tk.Label(self,textvariable=self.menu_message_str
                                   ,font=("comic sans",30,"bold"))
        self.main_label.grid(pady=300) #brings label to the center of the window


    #Callback wrappers that are defined in callback_functions.py
    def attachLoginOption(self):
        Cb_func.loginToAccount(self)
        
    def attachHelpOption(self):
        Cb_func.provideHelp(self)
        
    def initiateDrinkEvent(self,drink_option):
        self.current_drink = drink_option
        Cb_func.drinkCallback(self)
        
        
def runMainApplication():
    """ Creates and runs an instance of the main application """
    root = tk.Tk()
    main_app = MainApplication(master = root)
    main_app.mainloop()

if __name__ == "__main__":
    runMainApplication()
