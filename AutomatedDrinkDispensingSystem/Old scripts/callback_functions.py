"""
Programmer: Chris Blanks
Last Edited: 10/6/2018
Project: Automated Self-Serving System
Purpose: This script defines the callback functions used by each feature 
in the main application.

"""
from PIL import Image, ImageTk

def drinkCallback(self):
    """Sets up the window for a specific drink out of the set """
    print("Drink #",int(self.current_drink.id_number)+1,": ",self.current_drink.name)
    self.clearDrinkOptionsFromGUI()
    self.setupDrinkProfileInGUI()
    
def loginToAccount(self):
    """Allows known users to access the system manager mode """
    print("Someone wants to login...")
def provideHelp(self):
    """Displays information about how to operate the machine """
    print("Calling 911 in 5...4...3...2...1...")
