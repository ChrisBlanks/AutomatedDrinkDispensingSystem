#!/usr/bin/env python3
"""
Programmer: Chris Blanks
Last Edited: May 2019
Project: Automated Self-Serving System
Purpose: This script defines the EmployeeWindow Class.
"""

import tkinter as tk
from tkinter import messagebox
import os

#ThirdParty Libraries
from tkcolorpicker import askcolor #pip3 install tkcolorpicker

#My Scripts
from LogManager import LogManager
from AppWindow import AppWindow
from DrinkProfileManager import DrinkProfileManager
from ApplicationUserEditor import ApplicationUserEditor
from InventoryManager import InventoryManager


class EmployeeWindow(AppWindow):
    
    
    
    def __init__(self,main_app_instance, isAdminMode = False):
        AppWindow.__init__(self,main_app_instance)
        self.main_app = main_app_instance
        self.master = main_app_instance.employee_top_lvl
        self.master.configure(background= self.main_app.MASTER_BACKGROUND_COLOR)
        self.size= [self.master.winfo_screenwidth() , self.master.winfo_screenheight() ]
        
        self.frame = tk.Frame(self.master)
        self.frame.configure(bg= self.main_app.MASTER_BACKGROUND_COLOR)
            
        self.parent_menu = tk.Menu(self.frame)
        self.master.config(menu= self.parent_menu)
        
        
        self.operation_instructions_file_path = self.main_app.SYSTEM_INFO_PATH +"/instructions_4_employee.txt"
        
        self.isAdminMode = isAdminMode

        self.configureWindow()
        self.frame.grid()
        
        self.createHelpMenu(menu_name="Help")
        self.displayDrinkOptionsInGUI() #Method from AppWindow
        
        


    def configureWindow(self):
        """Sets window geometry and limits."""
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth()
                                                  ,self.master.winfo_screenheight()))   
        self.master.protocol("WM_DELETE_WINDOW",self.deployExitMessageBox)

        if self.isAdminMode:
            self.setupAdminMenuBar()
        else:
            self.setupOptionsMenuBar()


    def setupAdminMenuBar(self):
        """Provides extra features in the menu bar for full control of the app."""
        print("Admin status.")
        self.admin_menu = tk.Menu(self.parent_menu,tearoff=0)
        self.parent_menu.add_cascade(label="Admin Options",menu=self.admin_menu)
        
        self.admin_menu.add_command(label="Launch Drink Profile Manager",command= self.launchDrinkProfileManager)
        self.admin_menu.add_separator()
        self.admin_menu.add_command(label="Display Log" ,command= self.launchLogManger) #allow option to delete them
        self.admin_menu.add_separator()
        self.admin_menu.add_command(label="Edit Configuration" ,command= self.editConfigFile)
        self.admin_menu.add_separator()
        self.admin_menu.add_command(label="Edit User Logins" ,command= self.editUserLogins)
        self.admin_menu.add_separator()
        self.admin_menu.add_command(label="Show URL for Phone App" ,command= self.showURL)
        self.admin_menu.add_separator()
        self.admin_menu.add_command(label="Show IP Address" ,command= self.showIPAddress)
        self.admin_menu.add_separator()
        self.admin_menu.add_command(label="Change background color" ,command= self.switchBackgroundColor)
        self.admin_menu.add_separator()
        self.admin_menu.add_command(label="Edit Inventory" ,command= self.launchInventoryManager)

    
    def setupOptionsMenuBar(self):
        """Provides regular features in the menu bar for employees"""
        print("Employee status.")
        self.options_menu = tk.Menu(self.parent_menu,tearoff=0)
        self.parent_menu.add_cascade(label="Employee Options",menu= self.options_menu)

        self.options_menu.add_command(label="Launch Drink Profile Manager" ,command= self.launchDrinkProfileManager)
        self.options_menu.add_separator()
        self.options_menu.add_command(label="Show URL for Phone App" ,command= self.showURL)
        self.options_menu.add_separator()
        self.options_menu.add_command(label="Show IP Address" ,command= self.showIPAddress)
        self.options_menu.add_separator()
        self.options_menu.add_command(label="Change background color" ,command= self.switchBackgroundColor)
        self.options_menu.add_separator()
        self.options_menu.add_command(label="Edit Inventory" ,command= self.launchInventoryManager)


    def switchBackgroundColor(self):
        """Creates a dialog box that the user can use to select a new background color."""
        color_request = askcolor(color=self.main_app.MASTER_BACKGROUND_COLOR,
                                parent=self.frame)
        if color_request[1] is None:
                return
        
        self.main_app.MASTER_BACKGROUND_COLOR = color_request[1] #RGB HEX code
        self.main_app.master.configure(background=self.main_app.MASTER_BACKGROUND_COLOR)
        
        path= "{}/background_color.txt".format(self.main_app.SYSTEM_INFO_PATH)
        with open(path ,"w") as file:
                file.write(color_request[1])
                
        self.main_app.master.update_idletasks()
        #should write this to a file eventually


    def launchInventoryManager(self):
        """Launchs inventory manager."""
        self.inventory_manager = tk.Toplevel(self.master,background=self.main_app.MASTER_BACKGROUND_COLOR)
        self.inventory_manager.tk.call("wm","iconphoto",self.inventory_manager._w,self.main_app.icon_img) 
        self.inventory_manager.title("Inventory Manager")
        #self.inventory_manager.geometry(self.main_app.geometry_string)
        # args for geometry(): width,height,x-offset,y-offset
        self.inventory_manager.geometry("{}x{}+{}+{}".format(400,300,0,0))
        self.inventory_manager_win = tk.PanedWindow(self.inventory_manager,
                                                orient= tk.HORIZONTAL)
        self.inventory_manager_win.pack(fill=tk.BOTH,expand=1)
        self.inventory_manager_obj = InventoryManager(self.inventory_manager_win,self.main_app)
        #self.master.withdraw()
        
        

    def launchDrinkProfileManager(self):
        """Allows the employee to add, edit, or delete drink profiles."""
        self.top = tk.Toplevel(self.master,background=self.main_app.MASTER_BACKGROUND_COLOR)
        self.top.tk.call("wm","iconphoto",self.top._w,self.main_app.icon_img) 
        self.top.title("Drink Profile Manager")
        self.top.geometry(self.main_app.geometry_string)
        
        self.profile_manager_win = tk.PanedWindow(self.top,orient= tk.HORIZONTAL,
                                                background=self.main_app.MASTER_BACKGROUND_COLOR)
        self.profile_manager_win.pack(fill=tk.BOTH,expand=1)
        self.drink_profile_manager = DrinkProfileManager(self.profile_manager_win
                                                         ,self.main_app,self.isAdminMode)
        self.master.withdraw()


    def launchLogManger(self):
        self.log_top = tk.Toplevel(self.master,background=self.main_app.MASTER_BACKGROUND_COLOR)
        self.log_top.tk.call("wm","iconphoto",self.log_top._w,self.main_app.icon_img) 
        self.log_top.title("Log Manager")
        self.log_top.geometry(self.main_app.geometry_string)

        log_manager_win = tk.PanedWindow(self.log_top,orient=tk.HORIZONTAL,
                                        background=self.main_app.MASTER_BACKGROUND_COLOR)
        log_manager_win.pack(fill=tk.BOTH,expand=1)
        
        self.log_manager = LogManager(log_manager_win,self.main_app)
        self.master.withdraw()

    
    def displayLogFile(self):
        """OBSOLETE. Handled by LogManager class now. Displays the most recent log file."""
        with open(self.main_app.todays_log,'r') as file:
            lines = file.readlines()
            
        msg = " ".join(lines)
        
        self.log_display = tk.Toplevel()
        self.log_display.title("Current Log File:")
        
        scroll = tk.Scrollbar(self.log_display,orient= tk.VERTICAL)
        scroll.grid(row=0,column=1,sticky="ns")
        
        canvas = tk.Canvas(self.log_display,width=600,
                           height=500,
                           scrollregion=(0,0,2000,2000))
        canvas.grid(row=0,column=0,sticky="nsew")

        scroll.config(command=canvas.yview)
        canvas.config(yscrollcommand = scroll.set)
        canvas.create_text((0,0),text=msg,anchor="nw") #top left and anchored to the right

        log_menu = tk.Menu(self.log_display)
        log_options = tk.Menu(log_menu,tearoff=0)
        log_menu.add_cascade(label="Options",menu=log_options)

        self.log_display.config(menu=log_menu)
        
        log_options.add_command(label="Clear Log"
                                    ,command= self.clearTodayLog)
        self.log_display.rowconfigure(0,weight=1)
        self.log_display.columnconfigure(0,weight=1)


    def clearTodayLog(self):
        """OBSOLETE. Handled by LogManager class now. Clears the current log."""
        os.remove(self.main_app.todays_log)
        self.deployClearedMessageBox()
        self.main_app.writeToLog("Cleaned log file.")


    def deployClearedMessageBox(self):
        """OBSOLETE. Handled by LogManager class now. Deploys the message box for when the log file is cleared."""
        if messagebox.askokcancel("Cleared today's log","press Ok to continue."):
            self.log_display.destroy()


    def editUserLogins(self):
        """Displays current registered users. Allows for adding or deleting users."""
        user_editor_top = tk.Toplevel(background=self.main_app.MASTER_BACKGROUND_COLOR)
        user_editor_top.attributes("-topmost",True)
        user_editor_top.tk.call("wm","iconphoto",user_editor_top._w,self.main_app.icon_img)
        user_editor_top.title("Application User Editor")
        self.user_editor =  ApplicationUserEditor(user_editor_top,self.main_app,self.size)

    
    def editConfigFile(self):
        """Allows editing of the contents in the configuration file. """
        pass #Will be defined at a later time


    def showIPAddress(self):
        """Shows the current IP address in a top level window. """
        ip_window = tk.Toplevel(background=self.main_app.MASTER_BACKGROUND_COLOR,width="300")
        ip_window.attributes("-topmost",True)
        ip_window.tk.call("wm","iconphoto",ip_window._w,self.main_app.icon_img)
        ip_window.title("IP Address")
        
        ip_address = str(self.main_app.ip_address)
        ip_label = tk.Label(ip_window,text=ip_address,font=("Georgia","20","bold"),
        fg="red",background=self.main_app.MASTER_BACKGROUND_COLOR)
        
        ip_label.grid()


    def showURL(self):
        """Shows the current ngrok URL in a top level window. """
        url_window = tk.Toplevel(background=self.main_app.MASTER_BACKGROUND_COLOR,width="300")
        url_window.attributes("-topmost",True)
        url_window.tk.call("wm","iconphoto",url_window._w,self.main_app.icon_img)
        url_window.title("URL for Phone App")
        
        
        if self.main_app.url is None:
            url="Could not make a ngrok URL"
        else:
            url = str(self.main_app.url)
            
        url_label = tk.Label(url_window,text=url,font=("Georgia","20","bold"),
        fg="red",background=self.main_app.MASTER_BACKGROUND_COLOR)
        
        url_label.grid()


    def deployExitMessageBox(self):
        """Destroys employee window and brings up root window."""
        if messagebox.askokcancel("Quit","Are you sure?",parent=self.master):
            self.isAdminMode = False
            self.master.destroy()
            self.main_app.master.deiconify()
