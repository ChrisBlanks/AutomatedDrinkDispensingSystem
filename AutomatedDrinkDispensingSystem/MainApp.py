#!/usr/bin/env python3
"""
Programmer: Chris Blanks
Last Edited: 1/13/2019
Project: Automated Self-Serving System
Purpose: This script defines the MainApp class that runs the desktop application.
Note:
    >This script takes command line arguments now
        >two arguments must be sent
            > when "enable" is sent as 1st arg, all peripheral devices are enabled
            > when "testing" is sent as the 2nd arg, the camera is not used
"""

import os
import sys

#allows all scripts to be disocoverable on system path
#Note: can use os.sep to create dynamic paths 
main_path = (os.path.abspath(__file__)).replace("/MainApp.py","")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
icon_path = "{}/resources/gui_images/martini.png".format(main_path)


#Standard library imports
import tkinter as tk
from tkinter import ttk
import time
import datetime

from subprocess import check_output
import subprocess

from threading import Timer
import _thread as thread

from cryptography.fernet import Fernet
import http.server as hs
import socketserver as ss

#My Modules
from CustomerWindow import CustomerWindow
from EmployeeWindow import EmployeeWindow
import DrinkProfile as     dp_class
from LoginWindow    import LoginWindow
from KeyboardWindow import KeyboardWindow

#Periphal Device classes
from EmployeeSwitch import EmployeeSwitch
from PulsePin import PulsePin
from Camera import Camera
from EmbeddedBoard import EmbeddedBoard


def runMainApplication():
    """Initializes the application and all of its features."""
    root = tk.Tk()                                              #initiliazes the tk interpreter
    root.title("Automated Drink Dispensing System")
    
    icon_img = tk.Image("photo",file= icon_path)  # found image online; created by RoundIcons
    root.tk.call("wm","iconphoto",root._w,icon_img)             #sets the application icon
    
    enableDevices = False
    enableEmbedBoard = False
    
    #checks command line arguments
    if len(sys.argv) > 1:
        print("CLI args:",sys.argv)
        for arg in sys.argv:
            if arg == "enable":
                enableDevices = True #if true is sent as a command line arg then enable devices
            if arg == "embed_en":
                enableEmbedBoard = True

    
    main_app = MainApp(root,icon_img,enableDevices,enableEmbedBoard) 
    
    style = ttk.Style()
    current_theme = style.theme_use('clam')  #sets up the clam style for all ttk widgets

    root.mainloop()                          #starts loop for displaying content


class MainApp:
    
    #class member variables
    MAIN_DIRECTORY_PATH = main_path
    RESOURCES_PATH = "{}/resources".format(MAIN_DIRECTORY_PATH)
    
    DRINK_PROFILE_DIRECTORY_PATH = "{}/drink_profiles".format(RESOURCES_PATH)
    SYSTEM_INFO_PATH = "{}/system_info".format(RESOURCES_PATH)
    GUI_IMAGES_PATH = "{}/gui_images".format(RESOURCES_PATH)
    OTHER_PATH = "{}/other".format(RESOURCES_PATH)
    
    WAIT_SCREEN_IMG_PATH = "{}/drink_pour.jpg".format(GUI_IMAGES_PATH)
    DELIVERY_SCREEN_IMG_PATH = "{}/pick_up_drink.jpg".format(GUI_IMAGES_PATH)
    
    CONFIG_FILE_PATH = "{}/config.txt".format(SYSTEM_INFO_PATH)
    USER_LOGIN_FILE_PATH= "{}/user_login.txt".format(SYSTEM_INFO_PATH)
    ENCRYPTION_KEY_FILE_PATH = "{}/key.txt".format(SYSTEM_INFO_PATH)
    DRINK_MENU_FILE_PATH = "{}/drink_menu.txt".format(SYSTEM_INFO_PATH)
    CASCADES_PATH = "{}/haar_cascade_files".format(OTHER_PATH)
    
    
    MASTER_BACKGROUND_COLOR = "LightCyan3"
    
    #DEVICE CONFIGURATION
    BUTTON_ENABLE = True
    DELAY = 2000         # button input will be polled every 2 seconds
    AMOUNT_PAID = 0  # keeps track of how much a customer has paid; $0

    drink_names = []             #keeps a record of drink names

    isEmployeeMode= False        #controls what is displayed in employee mode
    isValidLogin = False         #controls whethere a user is given access to employee mode
    isWithoutLogin = False       #controls whether a new user login file is created
    data_demo_key = True         #toggles between pre-made shared data messages

    
    
    def __init__(self,master,icon_img,peripheral_device_enable=False,embedded_board_enable=False):
        self.master = master
        
        stored_color = self.retrieveBackgroundColor()
        if stored_color != self.MASTER_BACKGROUND_COLOR:
            print("Change in background color")
            self.MASTER_BACKGROUND_COLOR = stored_color
        
        self.master.configure(background=self.MASTER_BACKGROUND_COLOR)
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        self.geometry_string = str(self.screen_width)+"x"+ str(self.screen_height)
        self.icon_img = icon_img                          #included for use in children windows

        self.ip_address = self.getIPAddress()             #retrieves current wlan0 IP address
        self.writeToLog("Running main application")
        self.writeToSharedData()
        self.startHTTPThread()
        self.cipher_suite = self.setupUserEncryption()    #A cipher suite object is returned for decryption

        if self.isWithoutLogin == True:
            self.createDefaultUserLoginFile()             #creates a new user login file

        self.active_drink_objects = self.getDrinks()      #returns a list of drink_objects for later use
        
        self.device_enable = peripheral_device_enable
        self.embedded_board_enable = embedded_board_enable
        
        #check args
        if self.device_enable:
            self.createDevices() #creates device instances for later use
            self.initializeDrinkMenuOnEmbeddedBoard(self)
        elif self.embedded_board_enable:
            #if other devices off & want to still test embedded board
            self.embedded_board = EmbeddedBoard(self)
            self.embedded_board.initializeDrinkMenuOnBoard()
        
        self.createMainWindow()
        #self.selectWindow()

        self.retrieveConfigurationInformation()
        self.cleanOldDrinksFromConfig()


    
    def retrieveBackgroundColor(self):
        """Reads background color file for last saved background value."""
        path= "{}/background_color.txt".format(self.SYSTEM_INFO_PATH)
        with open(path ,"r") as file:
            color = file.read()
        
        return color

    
    def selectWindow(self,selection):
        """Determines what window is open."""
        if hasattr(self, 'employee_top_lvl'):
            self.employee_top_lvl.destroy()  #destroys old windows
            
        if hasattr(self, 'customer_top_lvl'):
            self.customer_top_lvl.destroy()  #destroys old windows
            
        if selection == 1:
            self.isEmployeeMode = True
            self.launchLoginWindow()
        else:
            self.isEmployeeMode = False
            self.master.withdraw()
            self.createCustomerWindow()


    def createMainWindow(self):
        """Displays main window elements. """
        self.master.geometry(self.geometry_string)
        print("\nWindow Size(Width): {}".format( self.master.winfo_screenwidth() ) )
        print("Window Size(Width): {}".format( self.master.winfo_screenheight() ) )

        self.main_title = ttk.Label(self.master,text="Selection Window")
        self.main_title.pack()

        self.customer_window_btn = ttk.Button(self.master,text="customer window"
                                             ,command= lambda window="customer": self.relaunchWindow(window))
        self.customer_window_btn.pack(fill=tk.BOTH)
        self.employee_window_btn = ttk.Button(self.master,text="employee window"
                                             ,command= lambda window="employee": self.relaunchWindow(window))
        self.employee_window_btn.pack(fill=tk.BOTH)


    def relaunchWindow(self,window):
        """ Relaunches the selected window."""
        
        if hasattr(self, 'switch'):
            self.BUTTON_ENABLE = True #enable button before entering a mode
            self.switch.state = "enabled"
        
        if window == "customer":
            self.isEmployeeMode = False
            self.master.withdraw()
            self.createCustomerWindow()
        elif window == "employee":
            self.isEmployeeMode = True
            self.master.withdraw()
            self.launchLoginWindow()
        else:
            print("What the heck?")


    def createCustomerWindow(self):
        """Creates separate customer window."""
        self.customer_top_lvl = tk.Toplevel(self.master,background=self.MASTER_BACKGROUND_COLOR)
        self.customer_top_lvl.tk.call("wm","iconphoto",self.customer_top_lvl._w,self.icon_img)
        self.customer_window = CustomerWindow(self)


    def createEmployeeWindow(self,isAdminMode):
        """Creates separate employee window """
        self.employee_top_lvl = tk.Toplevel(self.master,background=self.MASTER_BACKGROUND_COLOR)
        self.employee_top_lvl.tk.call("wm","iconphoto",self.employee_top_lvl._w,self.icon_img)
        self.employee_window = EmployeeWindow(self,isAdminMode)


    def launchLoginWindow(self):
        """Launches login window when employee mode is selected."""
        self.login_top_lvl = tk.Toplevel(self.master,background=self.MASTER_BACKGROUND_COLOR)
        self.login_top_lvl.tk.call("wm","iconphoto",self.login_top_lvl._w,self.icon_img)
        self.login_window = LoginWindow(self)


    def launchKeyboardWindow(self):
        """Launches a top level window that contains a keyboard that can deliver
        input to processes that need it."""
        self.keyboard_top_lvl = tk.Toplevel(self.master,background=self.MASTER_BACKGROUND_COLOR)
        self.keyboard_window = KeyboardWindow(self)


    def getDrinks(self):
        """Retrieves a list of active Drink objects."""
        active_drinks = []
        self.all_drinks = []

        os.chdir(self.DRINK_PROFILE_DIRECTORY_PATH)
        drink_profile_names = os.listdir(self.DRINK_PROFILE_DIRECTORY_PATH)

        #removes the __pycache__ directory and __init__.py file that gets initiated in this directory
        if "__pycache__" in drink_profile_names:
            drink_profile_names.remove("__pycache__")
        if "/__pycache__" in drink_profile_names:
            drink_profile_names.remove("/__pycache__")
        if "__init__.py" in drink_profile_names:
            drink_profile_names.remove("__init__.py")
        if "__init_.py" in drink_profile_names:
            drink_profile_names.remove("__init_.py")
        
        for name in drink_profile_names:
            path_builder = self.DRINK_PROFILE_DIRECTORY_PATH +"/"+ name
            os.chdir(path_builder)

            #finds index of text file in individual drink directory listings
            text_file_index = 0
            if ".txt" in os.listdir(path_builder)[0]:
                pass
            else:
                text_file_index= 1

            drink = dp_class.DrinkProfile("{}/{}".format(path_builder, os.listdir(path_builder)[text_file_index]),self.MAIN_DIRECTORY_PATH)

            if drink.isActive == "1":
                drink.name = (drink.name).replace(" ","_")
                drink.addDrinkToConfig()             #config file keeps record of active drinks
                active_drinks.append(drink)          #creates a separate list for active drinks (drinks to be displayed)

            self.all_drinks.append(drink)    #creates a list of active and inactive drinks

        os.chdir(self.MAIN_DIRECTORY_PATH)
        return active_drinks


    def retrieveConfigurationInformation(self):
        """Retrieves configuration info (e.g. drink names) from config file """
        with open(self.CONFIG_FILE_PATH,'r+') as f:
            lines = f.read().splitlines()

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


    def updateConfigurationFile(self,item_to_update,updated_value= None):
        """ """
        with open(self.CONFIG_FILE_PATH,"r+") as f:
            lines = f.read().splitlines()
            f.seek(0)

            line_headers = ["locked ","active_drink_list ","system_status "]
            line_to_edit = 0

            if item_to_update == "data_lock":
                line_to_edit = 1
            if item_to_update == "drink_list":
                line_to_edit = 2
            if item_to_update == "system_status":
                line_to_edit = 3

            line_number = 1
            for line in lines:
                if line_number == line_to_edit and updated_value != None:
                   line = line_headers[line_to_edit - 1] + updated_value
                   f.write(line+"\n")
                else:
                    f.write(line+"\n")
                if line_number == 3:
                    break
                line_number+=1


    def cleanOldDrinksFromConfig(self):
        """Updates the active drinks in the config file."""
        cleaned_list_of_names = ""
        loaded_drink_object_names = []
        for drink in self.active_drink_objects:
            loaded_drink_object_names.append((drink.name).replace("_"," "))
        for config_name in self.drink_names:
            if config_name.replace("_"," ") in loaded_drink_object_names:
                cleaned_list_of_names = cleaned_list_of_names + config_name + " "
        self.updateConfigurationFile("drink_list",cleaned_list_of_names)
        self.writeToLog("Cleaned Config file.")


    def writeToLog(self, message):
        """Writes messages into the log.txt file."""
        self.todays_log = "{}/log_files/log_on_{}.txt".format(self.SYSTEM_INFO_PATH, str( datetime.date.today() ) )
        with open(self.todays_log,"a+") as log:
            log.write("{} : {}\n".format( str( datetime.datetime.now() ) , message))


    def writeToDrinkSalesLog(self, message):
        """Writes time-stamped sales info into a log for each day."""
        self.todays_drink_sales = "{}/drink_sales/drink_sales_{}.txt".format(self.SYSTEM_INFO_PATH , str( datetime.date.today() ) )
        with open(self.todays_drink_sales,"a+") as log:
            log.write("{} : {}\n".format( str( datetime.datetime.now() ) , message))


    def addUserToLogin(self,user_type,username,password):
        """Creates a new user in the user_login file. Ex: self.addUserToLogin("R","Lei","Zhang")"""
        with open(self.USER_LOGIN_FILE_PATH,"rb+") as file:
            lines = file.read().splitlines()
            file.seek(0)
            line_num = 1
            next_line = False

            #if admin user, then add to admin section of user login file
            if user_type == "A":
                for line in lines:
                    line = str((self.cipher_suite.decrypt(line)).decode('ASCII'))
                    if next_line == True:
                        file.write(temp+b"\n")
                        next_line = False
                    if "ADMIN USER" in line:
                        temp = "{} {}".format(username,password)
                        temp = self.cipher_suite.encrypt(temp.encode(encoding='UTF-8'))
                        next_line = True
                    if "END" in line:
                        line = self.cipher_suite.encrypt(line.encode(encoding='UTF-8'))
                        file.write(line+b"\n")
                        break

                    line = self.cipher_suite.encrypt(line.encode(encoding='UTF-8'))
                    file.write(line+b"\n")
            #if regular user ("R"), then add to regular section of user login file
            else:
                for line in lines:
                    line = str((self.cipher_suite.decrypt(line)).decode('ASCII'))
                    if "REGULAR USER" in line:
                        line = self.cipher_suite.encrypt(line.encode(encoding='UTF-8'))
                        file.write(line+b"\n") #write REGULAR USER and add a new line

                        new_login = "{} {}".format(username,password)
                        new_encrypt = self.cipher_suite.encrypt(new_login.encode(encoding='UTF-8'))
                        file.write(new_encrypt+b"\n") #write new login and a new line before next line
                        continue

                    if "END" in line:
                        line = self.cipher_suite.encrypt(line.encode(encoding='UTF-8'))
                        file.write(line+b"\n")
                        break

                    line = self.cipher_suite.encrypt(line.encode(encoding='UTF-8'))
                    file.write(line+b"\n")

        self.writeToLog("Added {} account to login.".format(username) )


    def deleteUserFromLogin(self, username, password):
        """Deletes a user in the user_login file (besides the original admin account)."""
        login_combo = username +" " + password
        with open(self.USER_LOGIN_FILE_PATH,"rb+") as file:
            lines = file.read().splitlines()
            file.seek(0)
            print("Looking for: " + login_combo)
            for line in lines:
                line = str((self.cipher_suite.decrypt(line)).decode('ASCII'))
                print("line content: "+ line)

                if "END" in line:
                    line = self.cipher_suite.encrypt(line.encode(encoding='UTF-8'))
                    file.write(line+b"\n")
                    break     #last line, so break out of loop
                elif login_combo not in line:
                    print("not desired login: "+str(line) )
                    line = self.cipher_suite.encrypt(line.encode(encoding='UTF-8'))
                    file.write(line+b"\n")
                else:
                    print("Found {} in this line: {}".format(login_combo, line)) #skips over line if login_combo is in it
        
        self.writeToLog("Removed {} account from login.".format(username) )
 
        
    def setupUserEncryption(self):
        """Creates an encryption key if one is not already made """
        #if there's a key file, then acquire key from encryption
        if os.path.exists(self.ENCRYPTION_KEY_FILE_PATH):
            with open(self.ENCRYPTION_KEY_FILE_PATH,"rb") as file:
                key = file.readline() #one line file

                # if no user login file, then it will be created
                if os.path.exists(self.USER_LOGIN_FILE_PATH):
                    pass
                else:
                    self.isWithoutLogin = True

        else:
            key = Fernet.generate_key()
            with open(self.ENCRYPTION_KEY_FILE_PATH,"wb") as file:
                file.write(key)   #store key in file system
            self.isWithoutLogin = True

        cipher_suite = Fernet(key)
        return cipher_suite


    def createDefaultUserLoginFile(self):
        """Creates a default user_login.txt file that has the
        default login credentials in an encrypted form. """

        admin_str = "ADMIN USER"
        default_usr_str="admin admin"
        reg_usr_str = "REGULAR USER"
        end_str = "END"

        with open(self.USER_LOGIN_FILE_PATH,'wb') as new_user_login:
            admin_str = self.cipher_suite.encrypt(admin_str.encode(encoding='UTF-8'))
            default_usr_str = self.cipher_suite.encrypt(default_usr_str.encode(encoding='UTF-8'))
            reg_usr_str = self.cipher_suite.encrypt(reg_usr_str.encode(encoding='UTF-8'))
            end_str = self.cipher_suite.encrypt(end_str.encode(encoding='UTF-8'))

            new_user_login.write(admin_str+b"\n")
            new_user_login.write(default_usr_str+b"\n")
            new_user_login.write(reg_usr_str+b"\n")
            new_user_login.write(end_str+b"\n")

        self.isWithoutLogin = False
        self.writeToLog("Made new login file")


    def getIPAddress(self):
        host_info = check_output(['hostname','-I'])
        ip_address = host_info.split()[0].decode('ascii')
        print( "IP: {}\n".format(ip_address) )
        return ip_address


    def writeToSharedData(self):
        """Updates the write to shared data every 5 minutes."""
        MILLI = 1000
        MIN_IN_SEC = 60

        now = time.strftime("%H:%M:%S")
        print(now) #keeps track of write time

        self.todays_shared_data= "{}/shared_data/shared_data_{}.txt".format(self.SYSTEM_INFO_PATH, str( datetime.date.today() ) )
        with open(self.todays_shared_data,"w") as shared_log:


            msg = """STATUS
    idle
    employee
    chris
    INVENTORY
    rum 300 1000
    vodka 300 900
    tequila 300 1000
    gin 1000 1000
    triple_sec 300 400
    soda_water 200 1500
    SALES
    cuba_libre 55.00
    daiquiri 10.00
    kamikaze 0.00
    long_island_iced_tea 23.00
    naval_gimlet 5.00
    rum_and_coke 10.00
    screwdriver 10.00
    tequila 0.00
    vodka 100.00
    vodka_and_cranberry 20.00"""

            msg2 = """STATUS
    mixing
    employee
    admin
    INVENTORY
    rum 300 1000
    vodka 500 900
    tequila 300 1000
    gin 1000 1000
    triple_sec 300 400
    soda_water 200 1500
    SALES
    cuba_libre 25.00
    daiquiri 10.00
    kamikaze 10.00
    long_island_iced_tea 23.00
    naval_gimlet 5.00
    rum_and_coke 10.00
    screwdriver 10.00
    tequila 0.00
    vodka 19.00
    vodka_and_cranberry 20.00"""

            if self.data_demo_key == True:
                shared_log.write(msg)
            else:
                shared_log.write(msg2)

        self.data_demo_key = not self.data_demo_key                #toggles between the two shared data sets

        self.master.after(MIN_IN_SEC*MILLI,self.writeToSharedData) #recursively writes to shared data every 5 minutes


    def startHTTPThread(self):
        """Creates a http server in a separate thread from the GUI in order to prevent delays in the GUI."""
        thread.start_new_thread(self.startHTTPServer,tuple())


    def startHTTPServer(self):
        """Opens a http server in the shared data directory."""
        try:
            os.chdir(self.SYSTEM_INFO_PATH+"/shared_data")
            subprocess.call(["sudo", "python", "-m", "SimpleHTTPServer","80"])
        except: 
            print("Port is already open.") #printed in the abyss
            e = sys.exc_info()[0]
            print(e)


        os.chdir(self.MAIN_DIRECTORY_PATH)


    
    def createDevices(self):
        """Instantiates all devices."""
        
        self.switch = EmployeeSwitch(self)  #pass main app instance
        print("\n{} : {}".format(self.switch.name,self.switch.state))
        self.checkButtonState()
        
        self.pulse_pin = PulsePin(self) 
        print("\n{} : {}".format(self.pulse_pin.name,self.pulse_pin.state))
        
        self.camera = Camera(self)
        print("\n{} : {}".format(self.camera.name,self.camera.state) )
        
        self.embedded_board = EmbeddedBoard(self)
        print("\n{} : {}".format(self.embedded_board.name,self.embedded_board.state) )
        print("\n")
        

        
    def checkButtonState(self):
        """Recursively calls itself to check button state."""
        self.switch.checkButtonInput()   #check pin input
        self.master.after(self.DELAY,self.checkButtonState)
    
        
    def initializeDrinkMenuOnEmbeddedBoard(self):
        """Acquire drink information for file and send to EmbeddedBoard device
        for future use."""
        print("Starting initialization of drink menu")
        self.embedded_board.initializeDrinkMenuOnBoard()


    def updateDrinkMenu(self):
        """Drink Menu file is updated when drink profile of a drink is changed"""
        #sort by id_number of drinks
        self.active_drink_objects.sort(key=lambda x: x.id_number)
        
        for drink in sorted_drinks:
            
            """
            Need to generate a string of pump times that corresponds to valves on
            boards, so ingredients must be associated with valve numbers
            
            Need to convert ounces of ingredients to a pump time and then
            make a comma delimited string that will be represent pump times
            for each valve.
            
            Need to make unused valves get a value of 0.
            
            conversion between ounces to millimeters:
            1 fluid Oz = 29.5753 milliliters
            
            Time resolution: 30/256 = 0.117 sec = 0.117 milliliter
            
            Calculation:
              time_res = 30/256 #30 seconds divided by 255 (A byte max value)
              milli_req = OZ_num * 29.5735 
              pump_time = int(milli_req / time_res)
            """
            pump_times = "51,52,53,54,55,56,57,58"
            with open(self.main_app.DRINK_MENU_FILE_PATH,"w") as drink_menu:
                for i in range(4):
                    drink_menu_item = "{},{},{}\n".format(drink.id_number,pump_times,i)
                    drink_menu.write(drink_menu_item)


if __name__ == "__main__":
    runMainApplication()
