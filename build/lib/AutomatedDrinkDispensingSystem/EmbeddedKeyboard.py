#!/usr/bin/env python3
"""
Programmer: Chris Blanks
Last Edited: 11/9/2018
Project: Automated Self-Serving System
Purpose: This script defines the EmbeddedKeyboard class. This
class creates a keyboard that takes a variable amount of entry fields
and can iterate through them with the "Next Field button"
"""


import tkinter as tk


class EmbeddedKeyboard:

    buttons = [
    'q','w','e','r','t','y','u','i','o','p','<-','7','8','9','-',
    'a','s','d','f','g','h','j','k','l','[',']','4','5','6','+',
    'z','x','c','v','b','n','m',',','.','?','shift','1','2','3','/',' Space ']

    upper = [
    'Q','W','E','R','T','Y','U','I','O','P','<-','7','8','9','-',
    'A','S','D','F','G','H','J','K','L','[',']','4','5','6','+',
    'Z','X','C','V','B','N','M',',','.','?','shift','1','2','3','/',' Space ']
    
    def __init__(self,master,target_entry_fields,background=None):
        
        self.master = master
        self.background_arg = background
        self.entries = []
        self.entries.extend(target_entry_fields)
        self.num_of_entries = len(self.entries)
        self.current_entry = 0     #starts at first given entry field

        self.setBindings()
        self.setBackgroundColorOfKeys()


        self.current_case = "lower"
        self.initializeKeyboard()


    def setBackgroundColorOfKeys(self):
        """Sets background color of keys in keyboard."""
        if self.background_arg != None:
            self.bg = self.background_arg
        else:
            self.bg = "#000000"


    def setBindings(self):
        """Sets the bindings for the entry fields. Six entries max."""
        entry_id = 0
        for entry in self.entries:
            if entry_id == 0:
                entry.bind("<Button-1>",lambda x='': self.select('Next Field',0))
            if entry_id == 1:
                entry.bind("<Button-1>",lambda x='': self.select('Next Field',1))
            if entry_id == 2:
                entry.bind("<Button-1>",lambda x='': self.select('Next Field',2))
            if entry_id == 3:
                entry.bind("<Button-1>",lambda x='': self.select('Next Field',3))
            if entry_id == 4:
                entry.bind("<Button-1>",lambda x='': self.select('Next Field',4))
            if entry_id == 5:
                entry.bind("<Button-1>",lambda x='': self.select('Next Field',5))
            if entry_id == 6:
                entry.bind("<Button-1>",lambda x='': self.select('Next Field',6))
            entry_id+=1
    
        
    def initializeKeyboard(self):
        """Creates the keyboard window."""
        varRow = 1
        varColumn = 0
        self.button_ref = []
        for button in self.buttons:
    
            command = lambda x=button: self.select(x)

            if button != " Space ":
                self.but = tk.Button(self.master, text= button, width = 5, bg=self.bg,fg="#ffffff",
                          activebackground="#ffffff",activeforeground="#000000", relief="raised",
                          padx= 8, pady=8, bd=8,command=command)

                self.but.grid(row=varRow,column=varColumn)
                self.button_ref.append(self.but)
                
            else:
                self.but = tk.Button(self.master, text= button, width = 60, bg= self.bg,fg="#ffffff",
                          activebackground="#ffffff",activeforeground="#000000", relief="raised",
                          padx= 4, pady=4, bd=4,command=command)

                self.but.grid(row=6,columnspan= 16)
                self.button_ref.append(self.but)

                
            varColumn += 1
            
            if varColumn > 14 and varRow == 1:
                varColumn = 0
                varRow += 1
            if varColumn > 14 and varRow == 2:
                varColumn = 0
                varRow += 1


    def setupUpper(self):
        """Sets up an uppercase keyboard."""
        varRow = 1
        varColumn = 0
        self.upper_but_ref = []
        for upper in self.upper:
            command = lambda x=upper: self.select(x)

            if upper != " Space ":
                self.but = tk.Button(self.master, text= upper, width = 5, bg=self.bg,fg="#ffffff",
                          activebackground="#ffffff",activeforeground="#000000", relief="raised",
                          padx= 8, pady=8, bd=8,command=command)

                self.but.grid(row=varRow,column=varColumn)
                self.upper_but_ref.append(self.but)
                
            else:
                self.but = tk.Button(self.master, text= upper, width = 60, bg= self.bg,fg="#ffffff",
                          activebackground="#ffffff",activeforeground="#000000", relief="raised",
                          padx= 4, pady=4, bd=4,command=command)

                self.but.grid(row=6,columnspan= 16)
                self.upper_but_ref.append(self.but)
                
            varColumn += 1
            
            if varColumn > 14 and varRow == 1:
                varColumn = 0
                varRow += 1
            if varColumn > 14 and varRow == 2:
                varColumn = 0
                varRow += 1            


    def shiftKeys(self):
        """Toggles between upper and lower case."""
        if self.current_case == "lower":
            for but in self.button_ref:
                but.grid_forget()
            self.current_case = "upper"
            self.setupUpper()
        else:
            for but in self.upper_but_ref:
                but.grid_forget()
            self.current_case = "lower"    
            self.initializeKeyboard()

    
    def select(self,value,entry__id = 0):
        """Defines the action for each button in the keyboard."""
        pos= self.entries[self.current_entry].index(tk.INSERT)
        self.entries[self.current_entry].icursor(pos)

        if value == "<-":
            if pos != 0:
                self.entries[self.current_entry].delete(pos-1)
        elif value == " Space ":
            self.entries[self.current_entry].insert(pos," ")
        elif value == "Next Field":
            if entry__id != self.current_entry:
                self.current_entry = entry__id
        elif value == "shift":
            self.shiftKeys()
        else:
            self.entries[self.current_entry].insert(pos, value)
