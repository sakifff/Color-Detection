import cv2
import numpy as np
import pandas as pd
import argparse

#Creating argument parser to take image path from command line
#https://www.pyimagesearch.com/2018/03/12/python-argparse-command-line-arguments/
#https://docs.python.org/3/library/argparse.html

argparse = argparse.ArgumentParser()
argparse.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(argparse.parse_args())
img = args['image']

#Reading the image with opencv

img = cv2.imread(img)

#global variables (used later on)

clicked = False
r = 0
g = 0
b = 0
xpos = 0
ypos = 0

#Read in data, name the columns accordingly

cols = ["color", "color_name", "hex", "R", "G", "B"]
df = pd.read_csv('colors.csv', names=cols, header=None)

#function to calculate minimum distance from all colors and get the most matching color

def ColorName(R,G,B):
    minimum = 10000
    for i in range(len(df)):
        d = abs(R- int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if(d<=minimum):
            minimum = d
            color = df.loc[i,"color_name"]
    return color

#function to get x,y coordinates when double clicking mouse

def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)
       
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_function)

while(1):

    cv2.imshow("image",img)
    if (clicked):
   
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        #Creating text string to display the color name and RGB values
        text = ColorName(r, g, b)
        
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        #For very light colours, the text needs to be displayed in black
        if(r+g+b >= 600):
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
            
        clicked=False

    #Make sure pressing "esc" exits the loop and closes the app   
    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()
