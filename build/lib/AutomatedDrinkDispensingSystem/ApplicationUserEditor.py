#!/usr/bin/env python3
"""
Programmer: Chris Blanks
Last Edited: 11/3/2018
Project: Automated Self-Serving System
Purpose: This script defines the ApplicationUserEditor class that controls
user login information.
"""
from tkinter import messagebox
import tkinter as tk
from EmbeddedKeyboard import EmbeddedKeyboard


class ApplicationUserEditor:
    def __init__(self,master,main_app,size):
        self.master = master
        self.main_app = main_app
        
        self.width = size[0]
        self.height = size[1]
        self.font = ("Georgia",12,"")

        self.users = self.getUsers()
        self.configureWindow()


    def configureWindow(self):
        self.master.configure(width=self.width,height=self.height)
        self.master.protocol("WM_DELETE_WINDOW",self.deployExitMessageBox)
        self.addWindowElements()


    def getUsers(self):
        """Gets a list of users."""
        with open(self.main_app.USER_LOGIN_FILE_PATH,"rb+") as file:
            lines = file.read().splitlines()
        
        
        user_list = ""
        for line in lines:
            line = (self.main_app.cipher_suite.decrypt(line)).decode('ASCII')
            if "END" not in line:
                user_list = user_list + line+ "\n"
        return user_list
            
        

    def addWindowElements(self):
        self.user_list_label = tk.Label(self.master,text="Current Users:",
                                  font=self.font)
        self.user_list_label.grid(row=0,column=0)
        self.users_in_gui = tk.Label(self.master,text=self.users,font=self.font)
        self.users_in_gui.grid(row=1,column=0)

        self.add_button = tk.Button(self.master,text="Add",bg="green",
                                    command=lambda x="Add": self.launchEditorWindow(x,"Add a user"))
        self.add_button.grid(row=0,column=1)
        self.delete_button = tk.Button(self.master,text="Delete",bg="red",
                                    command=lambda x="Delete": self.launchEditorWindow(x,"Delete a user"))
        self.delete_button.grid(row=0,column=2)
        

    def launchEditorWindow(self,button_type,title):
        self.top = tk.Toplevel(self.master)
        self.top.tk.call("wm","iconphoto",self.top._w,self.main_app.icon_img) 
        self.top.title(title)
        self.top.geometry("{0}x{1}+0+0".format(self.width,self.height))

        self.frame = tk.Frame(self.top)
        
        username_label = tk.Label(self.frame,text="Username",font=self.font)
        username_label.grid(row=0,column = 0)
        self.user_name_entry = tk.Entry(self.frame,width=138)
        self.user_name_entry.grid(row=0,column=1)
        
        pass_label = tk.Label(self.frame,text="Password",font=self.font)
        pass_label.grid(row=1,column = 0)
        self.pass_entry = tk.Entry(self.frame,width=138)
        self.pass_entry.grid(row=1,column=1)
        
        if button_type == "Delete":
            self.setupDeleteItems()
        elif button_type == "Add":
            self.setupAddItems()
        else:
            print("How?")

        entries = [self.user_name_entry,self.pass_entry]
        
        keyboard_canvas = tk.Canvas(self.frame,width=350,height=350)
        embed_keyboard = EmbeddedKeyboard(keyboard_canvas,entries)
        keyboard_canvas.grid(column=1,sticky="s")
        self.frame.grid()
        


    def setupDeleteItems(self):
        self.done = tk.Button(self.frame,text="Done",bg="orange",
                              command=lambda x="delete": self.deployDoneMessageBox(x))
        self.done.grid(row=0,column=2,sticky="nsew",rowspan=2)
        
         
    
    def setupAddItems(self):
        self.done = tk.Button(self.frame,text="Done",bg="orange",
                              command=lambda x="add": self.deployDoneMessageBox(x))

        self.checkbut_state = tk.IntVar()
        self.admin_check = tk.Checkbutton(self.frame,text="Admin user?",variable=self.checkbut_state)
        self.admin_check.grid(row=0,column=2)
        self.done.grid(row=1,column=2,sticky="nsew",rowspan=2)


    def deployDoneMessageBox(self,button_type):
        """Destroys window and brings back previous window."""
        username = self.user_name_entry.get()
        password = self.pass_entry.get()
        
        if username == "" or password == "":
            self.deployIncompleteMessageBox() #if either empty, show warning
            return
        if messagebox.askokcancel("Done","Are you sure?",parent=self.master):
            if button_type == "add":
                user_type = ""   # when empty, user is regular user
                if self.checkbut_state.get() == 1:
                    user_type = "A"   # A = admin user
                self.main_app.addUserToLogin(user_type,username,password)
            elif button_type =="delete":
                self.main_app.deleteUserFromLogin(username,password)

            self.top.destroy()
            self.master.destroy()


    def deployIncompleteMessageBox(self):
        """Warns user about incomplete user login."""
        messagebox.showwarning("Incomplete","Please fill all fields.",parent=self.top)

        
    def deployExitMessageBox(self):
        """Destroys window and brings back previous window."""
        if messagebox.askokcancel("Quit","Are you sure?",parent=self.master):
            self.master.destroy()

    
