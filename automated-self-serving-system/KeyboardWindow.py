#!/usr/bin/env python3
"""
Programmer: Chris Blanks
Last Edited: 11/3/2018
Project: Automated Self-Serving System
Purpose: This script defines the KeyboardWindow Class. It directly supports
the inter-GUI processes that need text input from the user.
"""


from tkinter import messagebox
import tkinter as tk


class KeyboardWindow:

    buttons = [
    'q','w','e','r','t','y','u','i','o','p','<-','7','8','9','-',
    'a','s','d','f','g','h','j','k','l','[',']','4','5','6','+',
    'z','x','c','v','b','n','m',',','.','?',' Enter ','1','2','3','/',' Space ']
    
    def __init__(self,main_app_instance):
        self.main_app = main_app_instance
        self.master = self.main_app.keyboard_top_lvl
        
        self.frame = tk.Frame(self.master)
        self.frame.grid()
        
        self.entry = tk.Entry(self.frame,width= 138)
        self.entry.grid(row= 0, columnspan = 20,sticky="n")
        
        #self.frame.grid_rowconfigure(0,weight=1)
        #self.frame.grid_columnconfigure(0,weight=1)
        
        self.initializeKeyboard()
        
        self.master.protocol("WM_DELETE_WINDOW",self.deployExitMessageBox)


    def initializeKeyboard(self):
        """Creates the keyboard window."""
        varRow = 1
        varColumn = 0
        
        for button in self.buttons:
    
            command = lambda x=button: self.select(x)

            if button != " Space ":
                tk.Button(self.frame, text= button, width = 5, bg="#000000",fg="#ffffff",
                          activebackground="#ffffff",activeforeground="#000000", relief="raised",
                          padx= 8, pady=8, bd=8,command=command).grid(row=varRow,column=varColumn)
            else:
                tk.Button(self.frame, text= button, width = 60, bg="#000000",fg="#ffffff",
                          activebackground="#ffffff",activeforeground="#000000", relief="raised",
                          padx= 4, pady=4, bd=4,command=command).grid(row=6,columnspan= 16)
                
            varColumn += 1
            
            if varColumn > 14 and varRow == 1:
                varColumn = 0
                varRow += 1
            if varColumn > 14 and varRow == 2:
                varColumn = 0
                varRow += 1


    def select(self,value):
        """Defines the action for each button in the keyboard."""
        if value == "<-":
            entry2 = self.entry.get()
            pos = self.entry.index(tk.INSERT)
            if pos != 0:
                self.entry.delete(pos-1)
        elif value == " Space ":
            self.entry.insert(tk.END," ")
        elif value == " Tab ":
            self.entry.insert(tk.END,"   ")
        elif value == " Enter ":
            entry2 = self.entry.get()
            print(entry2)
            #use the string in entry2 as input to other programs
        else:
            self.entry.insert(tk.END, value)


    def deployExitMessageBox(self):
        if messagebox.askokcancel("Quit","Are you sure?"):
            self.master.destroy()
