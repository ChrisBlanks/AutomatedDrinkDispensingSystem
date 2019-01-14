"""
Programmer: Chris Blanks
Last Edited: 11/3/2018
Project: Automated Self-Serving System
Purpose: This script defines the CustomerWindow Class.
"""

import tkinter as tk
from tkinter import messagebox

#my scripts
from AppWindow import AppWindow

class CustomerWindow(AppWindow):
    
    def __init__(self,main_app_instance):
        AppWindow.__init__(self,main_app_instance)
        
        self.main_app = main_app_instance
        self.operation_instructions_file_path = self.main_app.SYSTEM_INFO_PATH +"/instructions_4_customer.txt"
        self.master = self.main_app.customer_top_lvl
        self.master.configure(bg= AppWindow.background_color)
        
        self.frame = tk.Frame(self.master)
        self.frame.grid()
        self.frame.configure(bg= AppWindow.background_color)

        self.parent_menu = tk.Menu(self.frame)
        self.master.config(menu= self.parent_menu)
        
        self.configureWindow()
        
        self.displayDrinkOptionsInGUI() #Method from AppWindow
        self.createHelpMenu()
        

    def configureWindow(self):
        """Sets window geometry and limits."""
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth()
                                                  ,self.master.winfo_screenheight()))
        self.master.resizable(width=False, height=False)
        self.master.attributes('-fullscreen',True)
        #self.master.overrideredirect(True) #no window options (e.g. resizing)
        self.master.protocol("WM_DELETE_WINDOW",self.deployExitMessageBox) #ALT + F4 will close the window in Windows

        
    def deployExitMessageBox(self):
        pass
        #if messagebox.askokcancel("Quit","Are you sure?",parent=self.master)):
        #    
            #self.master.destroy()
            #self.main_app.master.deiconify()

