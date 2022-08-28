import cv2
import numpy as np
import pandas as pd
from tkinter import filedialog

img_path = filedialog.askopenfilename()  # opens dialog box for selecting images

img = cv2.imread(img_path)  # enables to read images

# get the height and width of the image img
height = img.shape[0]
width = img.shape[1]

# resize the image without changing the aspect ratio
img = cv2.resize(img, (int(width / 1.5), int(height / 1.5)))

clicked = False  # used as a flag to check if the mouse has been clicked or not
r = g = b = xpos = ypos = 0

# Reading csv file using pandas and giving names to each column
'''names gives names to each column and header=None tells that the first row of file should not
be treated as the header'''
csv = pd.read_csv('colors.csv', names=["color", "color_name", "hex", "R", "G", "B"], header=None)


# function to calculate minimum distance from all colors and get the most matching colour
def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        # subtracts RGB after receiving other RGB values from csv file
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if (d <= minimum):
            minimum = d
            ColourName = csv.loc[i, "color_name"]
    return ColourName


# function to get hex code of the colour
def getHexCode(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if (d <= minimum):
            minimum = d
            Hexcode = csv.loc[i, "hex"]
    return Hexcode


# function to get x,y coordinates of mouse double click
def MouseEvent(event, x, y, flags, param):  # predefined format of parameters of this function
    if event == cv2.EVENT_LBUTTONDBLCLK:  # check if the left mous button has been clicked twice
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y

        # Using the unpacking feature of python
        b, g, r = img[y, x]  # b,g,r should be in the same sequence
        '''can also be written as: b=img[y,x,0]
                                   g=img[y,x,1]
                                   r=img[y,x,2]
                                   where 0,1,2 are colour channels'''
        # since the data type of b g r is Unsigned integer (0 to 255)
        # we will type cast it to int 
        b = int(b)
        g = int(g)
        r = int(r)


'''This function creates the window even before imshow does
the cv2.WINDOW_NORMAL flag makes the window resizable'''
cv2.namedWindow('Colour Detector')  # cv2.WINDOW_NORMAL)
cv2.moveWindow('Colour Detector', 80, 102)

'''used to call the mouse event function whenever a mouse activity is detected'''
cv2.setMouseCallback('Colour Detector', MouseEvent)

while (1):

    cv2.imshow("Colour Detector", img)  # displays image
    if (clicked):

        # cv2.rectangle(image, startpoint, endpoint, color, thickness)
        # (200,5) is the top reft coordinate and (750,25) is the bottom right
        cv2.rectangle(img, (50, 0), (750, 20), (b, g, r), -1)  # -1 fills the entire rectangle with the set colour

        '''Creating a string to display with colour name and RGB values in it'''
        text = "Name=" + getColorName(r, g, b) + '  HexCode=' + getHexCode(r, g, b) + '  (R, G, B)= (' + str(
            r) + ', ' + str(g) + ', ' + str(b) + ')'

        # cv2.putText(img,text,startingPoint,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (60, 15), 2, 0.5, (255, 255, 255), 1,
                    cv2.LINE_AA)  # draw shapes has only 4 lineTypes, the used one is AntiAliasing

        # Since on some very light backgrounds white text will not be visible, we display it in black
        if (r + g + b >= 300):
            cv2.putText(img, text, (60, 15), 2, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

        # set the clicked variable back to false for next coordinate flag check    
        clicked = False
    '''waitkey wait for the key event infinitely, when parameter is >0, it wait at least till
the time ms passed, larger number will delay the time between two outputs in the program
0xFF is hexadecimal const with binary value 11111111, cv2.waitKey() returns a 32 Bit
integer value (might be dependent on the platform). The key input is in ASCII which is an
8 Bit integer value. So you only care about these 8 bits and want all other bits to be 0'''
    if cv2.waitKey(10) & 0xFF == 27:  # MUST FOR 64 BIT SYSTEMS
        break

cv2.destroyAllWindows()  # destroys the opencv window
