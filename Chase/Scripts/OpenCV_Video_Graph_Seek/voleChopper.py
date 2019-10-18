###########################################################
# AUTHOR  : Chase Dudas
# CREATED : 10/9/2019
# Title   : videoParser.py
# COMMENT : A GUI used to edit and crop a video. For lab 
#           purposes, the video had 4 simultaneous 
#           experiments in a square-like pattern. The 
#           GUI is hard coded for this case, but it can 
#           easily be adjusted by editing how the video 
#           is cropped in the import video function. 
# Need    : Python, OpenCV, Tkinter
###########################################################
# PARAMETERS
###########################################################

import cv2 
import numpy as np 
from tkinter import *
import re
import skvideo.io
import os
import platform
import time
import pims #lazy loading of videos http://soft-matter.github.io/pims/v0.4.1/
#import av

###########################################################
# CLASSES
###########################################################

class voleEntry:
    def __init__(self, number, startTime, endTime):
        # Stores the vole's number in an IntVar()
        self.number = number
        # Stores the starting time in a StringVar()
        self.startTime = startTime
        # Stores the ending time in a StringVar()
        self.endTime = endTime
    
    def getInfo(self):
        print("----------------------------------")
        # Get is needed here to access the tkinter variables, IntVar() and StringVar()
        print("\tVole number is: %s\n" % self.number.get())
        print("\tStart time is: %s\n" % self.startTime.get())
        print("\tEnd time is: %s" % self.endTime.get())
        print("----------------------------------")

    def getVoleNumber(self):
        return self.number.get()

    def getStartTime(self):
        return self.startTime.get()

    def getEndTime(self):
        return self.endTime.get()

###########################################################
# END OF CLASSES DEF
###########################################################

###########################################################
# VARIABLE DEF
###########################################################
voleArrayQ1 = []
voleArrayQ2 = []
voleArrayQ3 = []
voleArrayQ4 = []

# voleNumQ1 = []
# voleNumQ2 = []
# voleNumQ3 = []
# voleNumQ4 = []

# voleStartTimeQ1 = []
# voleStartTimeQ2 = []
# voleStartTimeQ3 = []
# voleStartTimeQ4 = []

# voleEndTimeQ1 = []
# voleEndTimeQ2 = []
# voleEndTimeQ3 = []
# voleEndTimeQ4 = []

# Global counters used to keep track of the number of voles input into each quadrant
counterQ1 = 0
counterQ2 = 0
counterQ3 = 0
counterQ4 = 0

# Video path directs which input video should be used
VIDEO_PATH = r'd:\Donaldson Lab\Current Work\Video Split Gui\fourQuad.avi'
# Shared video path directs where the out put video(s) should be saved
SAVED_VIDEO_PATH = r'd:\Donaldson Lab\Current Work\Video Split Gui\voleChopper_'
# Date the video was created(Windows) or modified(Linux/OSx). Found in the properties of a file.
DATE_OF_VIDEO = ""
# split the video vertically
WIDTH = 640
# split the video horizontally
HEIGHT = 480

# Try to get the date that a file was created, falling back to when it was
# last modified if that isn't possible.
# Date is formated as such: DayOfTheWeek\sMonth\s\sDay\sHH:MM:SS\sYear
if platform.system() == 'Windows':
    DATE_OF_VIDEO = time.ctime(os.path.getctime(VIDEO_PATH))
else:
    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(VIDEO_PATH)
    DATE_OF_VIDEO = time.ctime(mtime)

cap = ""
fps = -1
###########################################################
# END OF VARIABLE DEF
###########################################################

###########################################################
# FUNCTION DEF
###########################################################

# Creates a 500 x 100 popup window
# Function takes in the title of the window and the message to be displayed 
def popupmsg(title, msg):
    # New window
    popup = Tk()
    # Set passed title and change to all caps
    popup.wm_title(title.upper())
    # Set default window geometry to 500 x 100
    popup.geometry("500x100") 
    # Set text for label to passed message
    label = Label(popup, text=msg, font=("Open Sans", 12))
    # Place on window
    label.pack(side="top", fill="x", pady=10)
    # Create button to close window
    B1 = Button(popup, text="Okay", command = popup.destroy)
    # Pack on window too
    B1.pack()
    popup.mainloop()


# Dynamically creates a new vole entry in the Q1 frame
#   Appends a new voleEntry object to voleArrayQ1
#   Variables are assigned to the voleEntry's properties.
#   Incriments the counter for Q1
def addVoleQ1():
    #This segment would eb used if the class doesnt work out 
    # WORKS!
    # voleNumQ1.append(IntVar())
    # voleStartTimeQ1.append(StringVar())
    # voleEndTimeQ1.append(StringVar())
    # global counterQ1
    # Label(quad1, text='Vole #').pack()
    # Entry(quad1, textvariable=voleNumQ1[counterQ1]).pack()
    # Label(quad1, text='Start time').pack()
    # Label(quad1, text='End time').pack()
    # Entry(quad1, textvariable=voleStartTimeQ1[counterQ1]).pack()
    # Entry(quad1, textvariable=voleEndTimeQ1[counterQ1]).pack()

    # Stores a new voleEntry object into the vole array for Q1. 
    # Default values:
    #   number = -1
    #   startTime = ""
    #   endTime = ""
    voleArrayQ1.append(voleEntry(IntVar(value = -1),StringVar(value = ""), StringVar(value = "")))

    # Global definition needed here to modify counterQ1
    global counterQ1

    # Dynamically add a new Tkinter section for a vole entry
    Label(quad1, text='Vole #').pack()
    Entry(quad1, textvariable=voleArrayQ1[counterQ1].number).pack()
    Label(quad1, text='Start time').pack()
    Entry(quad1, textvariable=voleArrayQ1[counterQ1].startTime).pack()
    Label(quad1, text='End time').pack()
    Entry(quad1, textvariable=voleArrayQ1[counterQ1].endTime).pack()

    # Increments the counter for Q1
    counterQ1 += 1


# Dynamically creates a new vole entry in the Q2 frame
#   Appends a new voleEntry object to voleArrayQ2
#   Variables are assigned to the voleEntry's properties.
#   Incriments the counter for Q2
def addVoleQ2():
    # Stores a new voleEntry object into the vole array for Q2. 
    # Default values:
    #   number = -1
    #   startTime = ""
    #   endTime = ""
    voleArrayQ2.append(voleEntry(IntVar(value = -1),StringVar(value = ""), StringVar(value = "")))

    # Global definition needed here to modify counterQ2
    global counterQ2

    # Dynamically add a new Tkinter section for a vole entry
    Label(quad2, text='Vole #').pack()
    Entry(quad2, textvariable=voleArrayQ2[counterQ2].number).pack()
    Label(quad2, text='Start time').pack()
    Entry(quad2, textvariable=voleArrayQ2[counterQ2].startTime).pack()
    Label(quad2, text='End time').pack()
    Entry(quad2, textvariable=voleArrayQ2[counterQ2].endTime).pack()

    # Increments the counter for Q2
    counterQ2 += 1


# Dynamically creates a new vole entry in the Q3 frame
#   Appends a new voleEntry object to voleArrayQ3
#   Variables are assigned to the voleEntry's properties.
#   Incriments the counter for Q3
def addVoleQ3():
    # Stores a new voleEntry object into the vole array for Q3. 
    # Default values:
    #   number = -1
    #   startTime = ""
    #   endTime = ""
    voleArrayQ3.append(voleEntry(IntVar(value = -1),StringVar(value = ""), StringVar(value = "")))

    # Global definition needed here to modify counterQ3
    global counterQ3

    # Dynamically add a new Tkinter section for a vole entry
    Label(quad3, text='Vole #').pack()
    Entry(quad3, textvariable=voleArrayQ3[counterQ3].number).pack()
    Label(quad3, text='Start time').pack()
    Entry(quad3, textvariable=voleArrayQ3[counterQ3].startTime).pack()
    Label(quad3, text='End time').pack()
    Entry(quad3, textvariable=voleArrayQ3[counterQ3].endTime).pack()

    # Increments the counter for Q3
    counterQ3 += 1


# Dynamically creates a new vole entry in the Q4 frame
#   Appends a new voleEntry object to voleArrayQ4
#   Variables are assigned to the voleEntry's properties.
#   Incriments the counter for Q4
def addVoleQ4():
    # Stores a new voleEntry object into the vole array for Q4. 
    # Default values:
    #   number = -1
    #   startTime = ""
    #   endTime = ""
    voleArrayQ4.append(voleEntry(IntVar(value = -1),StringVar(value = ""), StringVar(value = "")))

    # Global definition needed here to modify counterQ4
    global counterQ4

    # Dynamically add a new Tkinter section for a vole entry
    Label(quad4, text='Vole #').pack()
    Entry(quad4, textvariable=voleArrayQ4[counterQ4].number).pack()
    Label(quad4, text='Start time').pack()
    Entry(quad4, textvariable=voleArrayQ4[counterQ4].startTime).pack()
    Label(quad4, text='End time').pack()
    Entry(quad4, textvariable=voleArrayQ4[counterQ4].endTime).pack()

    # Increments the counter for Q4
    counterQ4 += 1


# Function called when the user hits the "Done" button in any of the quadrants
#    Function takes in a string which represnts the quadrant number of the pressed "Done" button
#    If elif logic checks which quadrant was pressed
#    For each quadrant, the info for each entry in the voleArrayQ(N) is printed to console
#    Then the function saveVideosUsingFrames is called and passed the quadrant number and the respective voleArray for that quadrant
def batchProcess(quadNumber):
    print("Printing all objects in %s:" % quadNumber)

    if quadNumber == "Q1":
        for i in range(counterQ1):
            # Used to access class variables
            voleArrayQ1[i].getInfo()
            
        print("Batch processing for Q1...")
        saveVideosUsingFrames("Q1",voleArrayQ1)

    elif quadNumber == "Q2":
        for i in range(counterQ2):
            # Used to access class variables
            voleArrayQ2[i].getInfo()
        print("Batch processing for Q2...")
        saveVideosUsingFrames("Q2",voleArrayQ2)

    elif quadNumber == "Q3":
        for i in range(counterQ3):
            # Used to access class variables
            voleArrayQ3[i].getInfo()
        print("Batch processing for Q3...")
        saveVideosUsingFrames("Q3",voleArrayQ3)

    elif quadNumber == "Q4":
        for i in range(counterQ4):
            # Used to access class variables
            voleArrayQ4[i].getInfo()
        print("Batch processing for Q4...")
        saveVideosUsingFrames("Q4",voleArrayQ4)


# Imports the selected video using OpenCV
#   global definitions are used to set the video capture, cap, and the frames per second, fps.
def importVideo():
    global cap 
    global fps

    # No longer uses numpy slicing to access frames
    # Grab a frame: vid.get_frame(0) = frame 0
    cap = pims.open(VIDEO_PATH) 

    # Grabs the video's FPS
    fps = int(cap.frame_rate)

# Converts timestamps to frame numbers
#   Regex checks for timestamps in the form of "00:00" or "00:00:00"
#   Depending which format is used, the timestamp is converted into total seconds
#   The frame number is found by multiplying seconds by frames per second
#   Returns the frame number as an int
def timeToFrame(timeStamp, fps):
    timestampRegexHours = r'[0-9]{2}:[0-9]{2}:[0-9]{2}'
    timestampRegexMinutes = r'[0-9]{2}:[0-9]{2}'

    if bool(re.match(timestampRegexHours, timeStamp)):
        # Split given time string into hours, minutes, and seconds. Map to ints
        hours, minutes, seconds = map(int, timeStamp.split(':'))
        # Convert hours into minutes and add to the current minutes
        minutes += hours * 60
        # Convert minutes into seconds and add to the current seconds
        seconds += minutes * 60

    elif bool(re.match(timestampRegexMinutes, timeStamp)):
        # Split given time string into minutes and seconds. Map to ints
        minutes, seconds = map(int, timeStamp.split(':'))
        # Convert minutes into seconds
        seconds += minutes * 60

    else:
        popupmsg("Error", "Time format not supported! Accepted formats are: 00:00:00 or 00:00")

    # Multiply the total seconds by the frames per second
    frameFromTime = seconds * fps
    # Returns the frame number that is associated with the timestamp
    return int(frameFromTime)
    

# Saves videos out to disk
#   Takes in a string quadrantNumber and a list of voleEntry objects voleEntryList
#   Loops for every entry in voleEntryList
#   Using timeToFrame, the current frame position flag is set equal to the starting timestamp
#   ...
def saveVideosUsingFrames(quadrantNumber, voleEntryList):
    
    # Loop through each vole entry in the list for quadrant 1
    for voleEntry in voleEntryList:
        # Convert timestamps to frames
        startingFrame = timeToFrame(voleEntry.getStartTime(),fps)
        print("Starting frame @: %s" % startingFrame)
        endingFrame = timeToFrame(voleEntry.getEndTime(),fps)
        print("Ending frame @: %s" % endingFrame)

        # Used to hold the number of frames needed to be captured.
        frameCount = endingFrame - startingFrame

        # Allow user to select a region of intrest
        if quadrantNumber == "Q1":
            # Q1: Bottom Right Video Quadrant
            img = cap.get_frame(int((startingFrame + endingFrame) / 2))[HEIGHT:(2*HEIGHT), WIDTH:(2*WIDTH)]

        elif quadrantNumber == "Q2":
            # Q2: Bottom Left Video Quadrant
            img = cap.get_frame(int((startingFrame + endingFrame) / 2))[HEIGHT:(2*HEIGHT), :WIDTH]

        elif quadrantNumber == "Q3":
            # Q3: Top Left Video Quadrant
            img = cap.get_frame(int((startingFrame + endingFrame) / 2))[:HEIGHT, :WIDTH]

        elif quadrantNumber == "Q4":
            # Q4: Top Right Video Quadrant
            img = cap.get_frame(int((startingFrame + endingFrame) / 2))[:HEIGHT, WIDTH:(2*WIDTH)]
        
        r = cv2.selectROI("crop",img)
        cv2.destroyWindow("crop")

        # Append MetaData to the filename that will be written out. Specified as Date(MM-DD-YYYY), Timestamp(HH-MM-SS), Vole Number(#).
        splitDateAttributes = DATE_OF_VIDEO.split()
        saveVideoPathPlusMetadata = SAVED_VIDEO_PATH + ("%s-%s-%s_%s_%s.mp4" % (splitDateAttributes[1], splitDateAttributes[2], splitDateAttributes[4],  
                                                                                        splitDateAttributes[3].replace(':', "-"), voleEntry.getVoleNumber()))
        # OpenCV Video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') #encoder to use
        writer= cv2.VideoWriter(saveVideoPathPlusMetadata, fourcc, fps, ( int(r[2]), int(r[3]) ))

        # Used as a counter to get the desired frames
        fc = startingFrame

        # Loop over each desired frame
        while fc < endingFrame:
            # Grab frame #fc from the ImageSequence cap
            originalFrame = cap.get_frame(fc)

            # Crop the video based on the quadrant number.
            if quadrantNumber == "Q1":
                # Q1: Bottom Right Video Quadrant
                originalFrame = originalFrame[HEIGHT:(2*HEIGHT), WIDTH:(2*WIDTH)]

            elif quadrantNumber == "Q2":
                # Q2: Bottom Left Video Quadrant
                originalFrame = originalFrame[HEIGHT:(2*HEIGHT), :WIDTH]

            elif quadrantNumber == "Q3":
                # Q3: Top Left Video Quadrant
                originalFrame = originalFrame[:HEIGHT, :WIDTH]

            elif quadrantNumber == "Q4":
                # Q4: Top Right Video Quadrant
                originalFrame = originalFrame[:HEIGHT, WIDTH:(2*WIDTH)]

            if r != (0, 0, 0, 0):
                # Crop image
                originalFrame = originalFrame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

            writer.write(originalFrame)

            #Incriment
            fc += 1

        writer.release()

###########################################################
# END OF FUNCTION DEF
###########################################################

###########################################################
# TESTS
###########################################################
print("Staring Tests:\n")

# Tests for timeToFrame
print("Testing timeToFrame...")
print("Expected: 5400")
print("Got: %s\n" % timeToFrame("01:30", 60))

#Tests for importVideo
print("Testing importVideo()...")
importVideo()
# if cap.isOpened():
#     print("Video import succeeded")
# else:
#     print("Video import failed")
print("FPS set to: %s\n" % fps)

###########################################################
# END OF TESTS
###########################################################

###########################################################
# MAIN FUNCTION
###########################################################

master = Tk() 
master.resizable(width=FALSE, height=FALSE)

quad1 = Frame(master)
quad2 = Frame(master)
quad3 = Frame(master)
quad4 = Frame(master)

voleNum = StringVar()
startFrame = StringVar()
endFrame = StringVar()

# Pack on the headers
Label(quad1, text='Quad 1', font=("Open Sanse", 13)).pack()
Label(quad2, text='Quad 2', font=("Open Sanse", 13)).pack()
Label(quad3, text='Quad 3', font=("Open Sanse", 13)).pack()
Label(quad4, text='Quad 4', font=("Open Sanse", 13)).pack()

# Pack on buttons to submit a batch job for processing.
Button(quad1, text='Done!', width=30, command=lambda: batchProcess("Q1")).pack(padx=5, pady=10,side = BOTTOM)
Button(quad2, text='Done!', width=30, command=lambda: batchProcess("Q2")).pack(padx=5, pady=10,side = BOTTOM)
Button(quad3, text='Done!', width=30, command=lambda: batchProcess("Q3")).pack(padx=5, pady=10,side = BOTTOM)
Button(quad4, text='Done!', width=30, command=lambda: batchProcess("Q4")).pack(padx=5, pady=10,side = BOTTOM)

# Pack on buttons to dynamically add more Vole entries.
Button(quad1, text='+Add Vole', width=30, command=addVoleQ1).pack(padx=5, pady=10,side = BOTTOM)
Button(quad2, text='+Add Vole', width=30, command=addVoleQ2).pack(padx=5, pady=10,side = BOTTOM)
Button(quad3, text='+Add Vole', width=30, command=addVoleQ3).pack(padx=5, pady=10,side = BOTTOM)
Button(quad4, text='+Add Vole', width=30, command=addVoleQ4).pack(padx=5, pady=10,side = BOTTOM)

# Pack on the four frames side by side 
quad1.pack(side = LEFT)
quad2.pack(side = LEFT)
quad3.pack(side = LEFT)
quad4.pack(side = LEFT)

mainloop() 

cap.close()

###########################################################
# END OF MAIN
###########################################################