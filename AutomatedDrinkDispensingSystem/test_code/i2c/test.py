#!/usr/bin/python3

from smbus2 import SMBusWrapper
import RPi.GPIO as GPIO
import time
    
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_UP) 
#setup pin 4 as input
#pull-up is setup on pin 4


#Will be used for when the drink ordering process needs to be started
def pollPinUntilLow():
    """Poll until pin 4 is low (signals that data transmission can start)"""
    while GPIO.input(4) == True:
        pass


def writeToEmbeddedBoard(data_sequence=None):
    """This function writes a series of data (HEX form) to the embedded
    boards via I2C."""
    
    DRINK_ID1 = 1 # Drink ID in the system
    DRINK_ID2 = 3 # Drink ID in the system
    TARGET_ADDRESS = 51 # 51 = 0x33 is the address of the Embedded board
    REG_ADDRESS = 55    # 55 = 0x37 is the address of a "register"
    DRINK_ADDRESS = 87  
    # 87 = 0x57 is the address to write to in order to transmit Drink ID & time to pump
    
    OFFSET = 0  
    TRANSMIT_DELAY = 0.1 #delay for for 100 milliseconds between data transmission
    
    if data_sequence is None:
        DATA1 =[DRINK_ID2,51,52,53,54,45,46,47,48,49,50]
        DATA2 =[DRINK_ID1,20,0,0,0,0,0,0,0,0,0]
    else:
        DATA = data  #must be a list of data (each item is )
    
        
    with SMBusWrapper(1) as bus:
        #Writing the recipe
        bus.write_i2c_block_data(TARGET_ADDRESS,REG_ADDRESS,DATA1)
        time.sleep(TRANSMIT_DELAY) #takes floats
        
        #Ordering the drink
        bus.write_i2c_block_data(TARGET_ADDRESS,DRINK_ADDRESS,DATA2)
        time.sleep(TRANSMIT_DELAY) #takes floats



def writeEverythingToBoard(data_sequence=None):
    """This function writes a series of data (HEX form) to the embedded
    boards via I2C. Note: Only can transmit 30 bytes of data."""
    
    I2C_SLAVE_ADDRESS = 51 # 51 = 0x33 is the address of the Embedded board
    RECIPE_MAKER_ADDRESS = 55    # 55 = 0x37 is the address of a "register"
    DRINK_ADDRESS = 87  #
    # 87 = 0x57 is the address to write to in order to transmit Drink ID & time to pump
    
    TRANSMIT_DELAY = 0.1 #delay for for 100 milliseconds between data transmission
    
    for i in range(24):
        print("Recipe #{}".format(str(i)))
        DRINK_ID = i
        
        ##### Format for data #####
        """
        Data length: 10
        
        recipe data format: [id, time_val_0,time_val_1,time_val_2,time_val_3,time_val_4,time5,time6,time7,valve_num ]
        
        order data format: [id, quantity,placeholder,placeholder,placeholder,placeholder,
        placeholder,placeholder,placeholder,placeholder ]
        
        """
        with SMBusWrapper(1) as bus:
            for j in range(4):
                
                print("Valve #{}".format(str(j)))
                valve_num = j
                
                DATA1= [DRINK_ID, 51+i,52+i,53+i,54+i ,55+i,56+i,57+i,58+i, valve_num]
                
                #Writing the recipe
                try:
                    bus.write_i2c_block_data(I2C_SLAVE_ADDRESS,RECIPE_MAKER_ADDRESS+j,DATA1)
                    time.sleep(TRANSMIT_DELAY) #takes floats
                except OSError:
                    print("Error: Not able to write data at recipe stage.")
               
            #Ordering the drink
            print("Ordering drink #{}".format(i))
            try:
                DATA2= [DRINK_ID, DRINK_ID*2 ,0,0,0   ,0,0,0,0  ,0]
                bus.write_i2c_block_data(I2C_SLAVE_ADDRESS,DRINK_ADDRESS,DATA2)
                time.sleep(TRANSMIT_DELAY) #takes floats
            except OSError:
                print("Error: Not able to write data at ordering stage.")





if __name__ == "__main__":
    writeEverythingToBoard()
    """
    If the following error is received, the it is most likely due to a
    mismatch in the number of bytes that are meant to be sent on the 
    master computer side and to be received on the embedded board side.
    
    OSError: [Errno 121] Remote I/O error
    """
    
