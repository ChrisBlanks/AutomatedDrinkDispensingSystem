#!/usr/bin/env python3
"""
Programmer: Chris Blanks
Last Edited: 10/27/2018
Project: Automated Self-Serving System
Purpose: This script defines the Drink Class.

Note:
    - The current code can only handle JPGs, so have to make it capable of more
    file types if the user will eventually be able to pull images from google images
    - Possible additions:
        *a pop up window that displays current drink profiles and related ingredients
        *a method for retrieving images from url (or really from anywhere)
"""

import os
import pathlib
import shutil


class DrinkProfile:
    
    drink_profile_directory = "/home/pi/PYTHON_PROJECTS/AutomatedDrinkDispensingSystem/automated-self-serving-system/drink_profiles"
    config_file_path = "/home/pi/PYTHON_PROJECTS/AutomatedDrinkDispensingSystem/automated-self-serving-system/system_info/config.txt"
    
    def __init__(self,drink_txt_file_path = None):
        self.drink_txt_file = drink_txt_file_path
        self.pic_extension = None
        self.isNewDrink = False
        
        #drink attributes that can be set by GUI
        self.id_number = None
        self.name = None
        self.ingredients = None
        self.pic_location = None
        self.isUrl = "False"
        self.isActive = "1"
        self.price = 0.0
        
        """
        Note on self.edited_attributes:
        Changes in the values of this attribute will mean that the new value
        will replace the previous value in the text file for the drink profile.
        Each index corresponds to the drink attributes declared above in descending
        order, so index 0 is id_number and index 7 is price of the drinks
        """
        self.edited_attributes = [0,0,0,0,0,0,0]
        
        self.checkIfNew()


    def checkIfNew(self):
        """Checks to see if the drink object is a new drink option. If new then the isNewDrink boolean will be True
        until the instance's attributes are defined and the createDrinkProfile method is called on the instance.S"""
        if self.drink_txt_file == None:
            self.isNewDrink = True
        else:
            self.getDrinkProfile()


    def getDrinkProfile(self):
        """Retrieves drink profile information from a subdirectory"""
        with open(self.drink_txt_file,'r',encoding="ISO-8859-1") as file:
            line_count = 1
            for line in file:
                line = line.encode('utf8').decode('iso-8859-1')
                if line_count == 1:
                    self.id_number = line.split()[1]
                if line_count == 2:
                    print(line.split()[1])
                    self.name = line.split()[1].replace('_',' ')
                if line_count == 3:
                    ingredient_list = line.split()
                    self.ingredients = ingredient_list[1:len(ingredient_list)]
                if line_count == 4:
                    self.pic_location = line.split()[1]
                if line_count == 5:
                    self.isUrl = line.split()[1]
                if line_count == 6:
                    self.isActive = line.split()[1]
                if line_count == 7:
                    self.price = line.split()[1]

                line_count += 1

            if self.isUrl == "False":
                self.pic_extension = os.path.splitext(self.pic_location)[1]


    def createDrinkProfile(self,desired_pic_path=None):
        """Creates a new drink profile in the designated directory.
        *Functions as a callback for a GUI element after the instance's attributes are populated.
        *Drinks are by default active until changed to inactive in GUI."""

        self.drink_profile_path = self.drink_profile_directory + "/" + self.name
        self.pic_location = self.drink_profile_path + "/" + self.name + self.pic_extension
        pathlib.Path(self.drink_profile_path).mkdir(exist_ok = True)
        os.chdir(self.drink_profile_path)
        
        new_name = self.name +".txt"
        with open(new_name,"w",encoding="ISO-8859-1") as new_text_file :
            new_text_file.write("id_number " + self.id_number+"\n")
            new_text_file.write("name " + self.name+"\n")
            new_text_file.write("ingredients " + self.ingredients+"\n")
            new_text_file.write("picture_location " + self.pic_location+"\n")
            new_text_file.write("isUrl " + str(self.isUrl)+"\n")
            new_text_file.write("isActive " + self.isActive+"\n")
            new_text_file.write("Price "+str(self.price)+ "\n")
        
        if self.isUrl != "False":
            print("Somehow the impossible happened?")
            print(self.isURL)
            pass #grab pic from url
        else:
            if desired_pic_path == None:
                pass 
            elif os.path.exists(desired_pic_path):
                try:
                    shutil.copyfile(desired_pic_path,self.pic_location)
                except IOError as e:
                    print("Unable to copy file. %s" %e)
            else:
                print("Desired path does not exist.")
        
        self.isNewDrink = False
        
        #go back to main directory
        os.chdir("..")
        os.chdir("..")

    
    def editDrinkProfile(self):
        """Edits an existing drink profile with the value change that was packed into the instance's
        edited_attributes attribute."""
        attrib_indx = 0
        changes = []
        for attrib_change in self.edited_attributes:
            print(attrib_change)
            if attrib_change == 0:
                pass
            else:
                changes.append((attrib_indx + 1,attrib_change)) #attrib_indx must match line number
            attrib_indx +=1

        self.changeValuesInTextFile(changes)                

        #reset edited_attributes
        for i in range(len(self.edited_attributes)):
            self.edited_attributes[i] = 0


    def changeValuesInTextFile(self,changes):
        """Takes a tuple as input. The first parameter is the row number, and the second parameter
        is the new value."""
        with open(self.drink_txt_file,'r+',encoding="ISO-8859-1") as file:
            lines = file.read().splitlines()
            file.seek(0)
            
            line_headers = ["id_number ","name ","ingredients ","picture_location ", "isUrl ","isActive ","Price "]
            line_count = 1
            for line in lines:
                for i in range(len(changes)):
                    if line_count == changes[i][0]:
                        line = line_headers[line_count - 1]+str(changes[i][1])
                        print(line)
                        if changes[i][0] == 4:
                            self.acquireDesiredPic(changes[i][1]) #change picture
                file.write(line+"\n")
                line_count +=1


        
    def deleteDrinkProfile(self):
        """Deletes an existing drink profile """
        self.name = (self.name).replace(' ','_')
        
        drink_profile_path = self.drink_profile_directory + "/" + self.name
        pic_location = drink_profile_path + "/" + self.name + self.pic_extension
        txt_file = drink_profile_path + "/" + self.name + ".txt"
        
        os.remove(txt_file)
        os.remove(pic_location)
        os.rmdir(drink_profile_path)

    
    def addDrinkToConfig(self, path= config_file_path):
        """Adds a drink to the configuration file for the main application if it is new."""
        with open(path,"r+",encoding="ISO-8859-1") as f:
            lines = f.read().splitlines()
            f.seek(0)
            
            line_number = 1
            for line in lines:
                if line_number == 2:
                    occurences_indx = []
                    start = 0
                    while True:
                        index_new = line.find(self.name,start)
                        if index_new == -1:
                            break
                        start = index_new + len(self.name)
                        occurences_indx.append(index_new)
                    if not occurences_indx:
                        line = line +" "+ self.name
                    else:
                        isNotARepeat = True
                        for sub_indx in occurences_indx:
                            if  line.endswith(self.name) or line[ sub_indx + len(self.name)] == " ":
                                isNotARepeat = False
                        if isNotARepeat:
                            line = line +" "+ self.name + " "
                        
                f.write(line+"\n") #overwrites existing content
                line_number += 1


    def acquireDesiredPic(self,desired_pic_path):
        """Acquires the desired pic and sets the pic_location attribute of the drink object."""

        if ".jpg" in desired_pic_path:
            self.pic_extension = ".jpg" #setup extension
        elif "png" in desired_pic_path :
            self.pic_extension = ".png" #setup extension

        if " " in self.name:
            self.name = (self.name).replace(" ","_")
            
        self.drink_profile_path = self.drink_profile_directory + "/" + self.name
        self.pic_location = self.drink_profile_path + "/" + self.name + self.pic_extension
        if desired_pic_path == self.pic_location:
            pass #nothing to change
        else:
            shutil.copyfile(desired_pic_path,self.pic_location)
        
        
        

### Functions for testing DrinkProfile class' robustness

def testExistingDrink():
    """Tests viewing the attributes of an existing drink profile."""
    test_drink = DrinkProfile(self.drink_profile_directory+"/cuba_libre/cuba_libre.txt")

    print(test_drink.name,"\nId:",test_drink.id_number,"\n",test_drink.ingredients)
    print(test_drink.pic_location,"\n",test_drink.isUrl,"\n",test_drink.pic_extension)
    print(test_drink.price)


def testNewDrink():
    """Tests creating a drink profile."""
    test_drink2 = DrinkProfile()
    test_drink2.name = "test_drink_2"
    test_drink2.id_number = "24"
    test_drink2.ingredients = "stuff ingredients nothing really"
    test_drink2.isUrl = "False"
    test_drink2.pic_extension = ".jpg"
    test_drink2.price = 5.99

    test_drink2.createDrinkProfile("/home/pi/Pictures/drink.jpg")    


def testAddingDrinkToConfig():
    """Tests adding a drink name to the config file for the system."""
    test_drink3 = DrinkProfile()
    test_drink3.name = "vodka"
    test_drink3.id_number = "25"
    test_drink3.ingredients = "stuff ingredients nothing really"
    test_drink3.isUrl = "False"
    test_drink3.pic_extension = ".jpg"

    test_drink3.addDrinkToConfig("config_copy.txt")


def testDeletingADrinkProfile():
    """Tests deleting a drink profile."""
    test_drink4 = DrinkProfile(self.drink_profile_directory+"/Test_drink_2/test_drink_2.txt")
    test_drink4.deleteDrinkProfile()


def testEditDrinkProfile():
    """Tests editing a drink profile."""
    test_drink5 = DrinkProfile(self.drink_profile_directory+"/Test_drink_2/test_drink_2.txt")
    test_drink5.id_number = "100"
    test_drink5.isActive = "0"
    test_drink5.price = 4.05
    
    test_drink5.edited_attributes[0] = test_drink5.id_number
    test_drink5.edited_attributes[6] = test_drink5.isActive
    test_drink5.edited_attributes[7] = test_drink5.price
    test_drink5.editDrinkProfile()
    print(test_drink5.edited_attributes)
    

if __name__ == "__main__":
    #testExistingDrink()
    #testNewDrink()
    #testAddingDrinkToConfig()
    #testDeletingADrinkProfile()
    #testEditDrinkProfile()
    pass
