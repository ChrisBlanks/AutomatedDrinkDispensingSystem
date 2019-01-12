"""
Programmer: Chris Blanks
Last Edited: 1/09/2019
Project: Automated Self-Serving System
Purpose: This script defines the LogManager Class.
"""
import os

import tkinter as tk
from tkinter import messagebox


class LogManager():

    SYSTEM_LOG_PATH = "/log_files"
    SALES_LOG_PATH = "/drink_sales"
    SHARED_DATA_PATH = "/shared_data"
    FONT = ("Georgia",16,"bold")
    
    def __init__(self,master, main_app_instance):
        self.master = master               #top level window for log manager
        self.main_app = main_app_instance
        self.parent_menu = tk.Menu(self.main_app.employee_window.log_top)
        self.main_app.employee_window.log_top.config(menu=self.parent_menu)
        
        self.current_type = None
        self.log_content = None
        
        self.retrieveAllLogFileNames()
        self.configureWindow()


    def retrieveListOfFiles(self,dir_path):
        """Retrieves file list for given directory """
        return os.listdir(self.main_app.SYSTEM_INFO_PATH + dir_path)


    def retrieveAllLogFileNames(self):
        """Collects all of the log files for each type into their own respective lists."""
        self.sys_file_names = (self.retrieveListOfFiles(self.SYSTEM_LOG_PATH))
        self.sales_file_names = (self.retrieveListOfFiles(self.SALES_LOG_PATH))
        self.shared_file_names = (self.retrieveListOfFiles(self.SHARED_DATA_PATH))

        self.sys_file_names.sort(reverse=True) #newest first in listbox
        self.sales_file_names.sort(reverse=True)
        self.shared_file_names.sort(reverse=True)

    
    def configureWindow(self):
        """Creates a messagebox for exit condition and starts setup for window."""
        self.main_app.employee_window.log_top.protocol("WM_DELETE_WINDOW",self.deployExitMessageBox)
        self.setupLogManagerMainWindow()


    def setupLogManagerMainWindow(self):
        """Populates window with widgets needed to display log file contents."""
        self.setupLogMenu()
        self.setupLeftPane()
        self.setupRightPane()


    def setupLogMenu(self):
        """Sets up menu options for displaying log files."""
        self.log_menu= tk.Menu(self.parent_menu,tearoff=0)
        self.parent_menu.add_cascade(label="<<< Select A Log File Type >>>",menu=self.log_menu)

        self.log_menu.add_command(label="System Log Files",
                                  command= lambda log_type = "system": self.showLogFiles(log_type))
        self.log_menu.add_separator()
        self.log_menu.add_command(label="Sales Log Files",
                                  command=lambda log_type = "sales": self.showLogFiles(log_type))
        self.log_menu.add_separator()
        self.log_menu.add_command(label="Shared Data Files",
                                  command=lambda log_type = "shared": self.showLogFiles(log_type) )


    def showLogFiles(self,log_type):
        """Based on button pressed, a certain type of log file will be displayed."""
        if log_type == "system":
            if self.current_type == log_type:
                return #current is equivalent to button press, so do nothing
            self.current_type = log_type
            self.emptyListBox()
            self.populateLeftPlane(self.sys_file_names)
        elif log_type == "sales":
            if self.current_type == log_type:
                return #current is equivalent to button press, so do nothing
            self.current_type = log_type
            self.emptyListBox()
            self.populateLeftPlane(self.sales_file_names)
        elif log_type == "shared":
            if self.current_type == log_type:
                return #current is equivalent to button press, so do nothing
            self.current_type = log_type
            self.emptyListBox()
            self.populateLeftPlane(self.shared_file_names)
        else:
            print("....How?")


    def emptyListBox(self):
        """Clears out listbox for new entries."""
        self.log_options.delete(0,tk.END) #deletes all items

    
    def populateLeftPlane(self,file_names):
        """Fills left plane will log files depending on given type."""
        index = 0
        for file in file_names:
            self.log_options.insert(index,file)
            index +=1
        
        
    def setupLeftPane(self):
        """Creates the widgets necessary for the left pane."""
        self.log_options = tk.Listbox(self.master,font=self.FONT,selectmode=tk.SINGLE)
        self.log_options.bind('<<ListboxSelect>>',self.listboxCallback)
        self.master.add(self.log_options)
        
        
    def listboxCallback(self,event):
        """When a log file is selected, it is displayed in the right pane."""
        if self.log_content != None:
            self.log_content.destroy() #gets rid of previous content
        index = None
        index = self.log_options.curselection()

        if index == None or index == "":
            return #don't do anything if no selection
        
        self.selected_file = self.log_options.get(index)

        type_path = None
        if self.current_type == "system":
            type_path = self.SYSTEM_LOG_PATH
        elif self.current_type == "sales":
            type_path = self.SALES_LOG_PATH
        elif self.current_type == "shared":
            type_path = self.SHARED_DATA_PATH
        else:
            print("Weird error.")

        assert type_path != None, "Type path not given."
        
        file_path = self.main_app.SYSTEM_INFO_PATH + type_path +"/"+self.selected_file 
        self.populateRightPane(file_path)


    def setupRightPane(self):
        """Creates the widgets necessary for the right pane. """
        self.text_id = None
        self.frame = tk.Frame(self.master)
        self.master.add(self.frame)

        self.canvas = tk.Canvas(self.frame,width=300,height=300,scrollregion=(0,0,10000,10000))
        
        self.scroll = tk.Scrollbar(self.frame,width=25,orient= tk.VERTICAL)
        self.scroll.pack(side=tk.RIGHT,fill=tk.Y)
        
        self.canvas.config(yscrollcommand = self.scroll.set)
        self.canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
        self.scroll.config(command=self.canvas.yview)


    def populateRightPane(self,log_file_path):
        """Shows log file's contents in right plane. """
        if self.text_id != None:
            self.canvas.delete(self.text_id) #clears text id before writing next one
        with open(log_file_path,"r") as content:
            lines = content.readlines()
        file_content = " ".join(lines)
        
        canvas_height = self.canvas.winfo_height()
        canvas_width = self.canvas.winfo_width()

        center1 = int(canvas_width/5)
        center2 = int(canvas_height/7)
        
        self.text_id = self.canvas.create_text((center1,center2),text=file_content,anchor="nw")


    def deployExitMessageBox(self):
        """Prompts user before closing window."""
        if messagebox.askokcancel("Quit","Are you sure?"):
            self.main_app.employee_window.log_top.destroy()
            self.main_app.employee_window.master.deiconify()


    ######### Features for the Admin User  #####################################
    def clearTodayLog(self,desired_log):
        """Removes desired log from file system"""
        os.remove(desired_log)
        self.deployClearedMessageBox()
        self.main_app.writeToLog("Removed this file --> "+str(desired_log)+".")


    def deployClearedMessageBox(self):
        """Deploys the message box for when the log file is cleared."""
        if messagebox.askokcancel("Cleared desired log","press Ok to continue."):
            self.log_display.destroy()

