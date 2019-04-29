#!/usr/bin/env python3

import tkinter as tk

class Draw(tk.Frame):
    def __init__(self):
        super().__init__() #call the __init__ of parent
        self.configureFrame()

    def configureFrame(self):
        self.master.title("Lines")
        self.pack(fill=tk.BOTH, expand=1)
        
        canvas = tk.Canvas(self)
        canvas.pack(fill=tk.BOTH,expand=1)
        
        top_left_x = 30
        top_left_y = 10
        bottom_right_x = 100
        bottom_right_y = 80
        height_of_box = 120

        box_bot_left_x = top_left_x 
        box_bot_left_y = top_left_y + height_of_box
        box_bot_right_x = bottom_right_x
        box_bot_right_y = box_bot_left_y
        
        liquid_height = box_bot_left_y-top_left_y
        ratio = 0.78 #the "filled" to "not filled" ratio of box

        level = int((1-ratio) * liquid_height)

        outline="#05f"
        fill="#05f"
        canvas.create_rectangle(top_left_x,top_left_y+level,
                    box_bot_right_x,box_bot_right_y,
                    outline=outline,fill=fill)
        
        # arg list for create_line: X1,Y1,X2,X3,option= ...
        canvas.create_line(top_left_x,top_left_y,bottom_right_x,top_left_y) #top line
        canvas.create_line(box_bot_left_x,box_bot_left_y,box_bot_right_x,box_bot_right_y) 
        #bottom line               
        
        canvas.create_line(top_left_x,top_left_y,top_left_x,box_bot_left_y) # left side of box
        canvas.create_line(bottom_right_x,top_left_y,box_bot_right_x,box_bot_right_y)
        
        mid_offset = 0.5 * (bottom_right_x-top_left_x)
        text_center_x = top_left_x + mid_offset
        text_center_y = top_left_y+level
        canvas.create_text(text_center_x,text_center_y,text="{}% left".format(ratio*100))




def main():
    """Draws a line on a canvas."""

    root = tk.Tk()
    win = Draw()
    root.geometry("400x250+300+300")
    root.mainloop()

if __name__ == "__main__":
    main()
