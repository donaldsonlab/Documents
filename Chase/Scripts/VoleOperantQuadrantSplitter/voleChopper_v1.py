###########################################################
# AUTHOR  : Chase Dudas
# CREATED : 10/9/2019
# Title   : videoChopper.py
# COMMENT : A GUI used to edit and crop a video. For lab 
#           purposes, the video had 4 simultaneous 
#           experiments in a square-like pattern. The 
#           GUI is hard coded for this case, but it can 
#           easily be adjusted by editing how the video 
#           is cropped in the import video function. 
# Need    : Python, OpenCV, Tkinter, PIMS
###########################################################
# PARAMETERS
###########################################################

import cv2 
import numpy as np 
from tkinter import *
from tkinter.ttk import Progressbar
import re
import os
import platform
import time
import pims #lazy loading of videos http://soft-matter.github.io/pims/v0.4.1/
import queue

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
# FUNCTION DEF
###########################################################

# Creates a 500 x 100 popup window
# Function takes in the title of the window and the message to be displayed 
def popupmsg(title, msg, master):
    # New window
    popup = Toplevel()
    # Set passed title and change to all caps
    popup.wm_title(title.upper())
    # Set default window geometry to 500 x 100
    popup.geometry("400x200") 
    # Set text for label to passed message
    label = Label(popup, text=msg, font=("Open Sans", 12))
    # Place on window
    label.pack(side="top", fill="x", pady=10)
    # Create button to close window
    B1 = Button(popup, text="Okay", command = popup.destroy)
    # Pack on window too
    B1.pack()
    # Wait the code until popup window is destroyed
    master.wait_window(popup)


# Dynamically creates a new vole entry
#   Appends a new voleEntry object(number, starttime, endtime) to the passed voleEntryArray
#   Increments the passed counter 
#   Once the first voleEntry is added, enables the submit button 
def addVoleEntry(voleEntryArray, tkinterFrame, counterQueue, button, progressTrackerLabel):
    # Stores a new voleEntry object into the passed vole array. 
    # Default values:
    #   number = -1
    #   startTime = ""
    #   endTime = ""
    voleEntryArray.append(voleEntry(IntVar(value = -1),StringVar(value = ""), StringVar(value = "")))

    # Stores the current counter value
    counterValue = counterQueue.get()

    # Dynamically add a new Tkinter section for a vole entry
    Label(tkinterFrame, text='Vole #').pack()
    Entry(tkinterFrame, textvariable=voleEntryArray[counterValue].number).pack()
    Label(tkinterFrame, text='Start time').pack()
    Entry(tkinterFrame, textvariable=voleEntryArray[counterValue].startTime).pack()
    Label(tkinterFrame, text='End time').pack()
    Entry(tkinterFrame, textvariable=voleEntryArray[counterValue].endTime).pack()

    # Button logic to enable the button if the user adds another vole entry
    if str(button['state']) == 'disabled':
        button['state'] = 'normal'
        progressTrackerLabel['text'] = 'Ready'

    # Increments and stores the incremented counter
    counterQueue.put(1 + counterValue)


# Function called when the user hits the "Done" button in any of the quadrants
#    Function takes in a string which represnts the quadrant number of the pressed "Done" button
#    If elif logic checks which quadrant was pressed
#    For each quadrant, the info for each entry in the voleArrayQ(N) is printed to console
#    Then the function saveVideosUsingFrames is called and passed the quadrant number and the respective voleArray for that quadrant
def batchProcess(quadNumber, voleEntryList, button, fps, cap, HEIGHT, WIDTH, DATE_OF_VIDEO, master, SAVED_VIDEO_PATH, progressBar, progressTrackerLabel):
    button['state'] = 'disabled'

    print("Printing all objects in %s:" % quadNumber)
    for entry in voleEntryList:
        entry.getInfo()

    print("Batch processing for Q1...")
    progressTrackerLabel['text'] = 'Running...'
    saveVideosUsingFrames(quadNumber,voleEntryList, fps, cap, HEIGHT, WIDTH, DATE_OF_VIDEO, master, SAVED_VIDEO_PATH, progressBar)
    progressTrackerLabel['text'] = 'Finished!'


# Imports the selected video using OpenCV
#   global definitions are used to set the video capture, cap, and the frames per second, fps.
def importVideo(videoPath):
    # global cap 
    # global fps

    # No longer uses numpy slicing to access frames
    # Grab a frame: vid.get_frame(0) = frame 0
    cap = pims.open(videoPath) 

    # Grabs the video's FPS
    fps = int(cap.frame_rate)

    return cap, fps


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
        return -1

    # Multiply the total seconds by the frames per second
    frameFromTime = seconds * fps
    # Returns the frame number that is associated with the timestamp
    return int(frameFromTime)
    

# Saves videos out to disk
#   Takes in a string quadrantNumber, a list of voleEntry objects (voleEntryList), the fps of the imported video,
#       the pims ImageSequence of the imported video, the height of a quadrant, the width of a quadrant,
#       the video date metadata, the main tkinter window, and the path to save the video.
#   Loops for every entry in voleEntryList
#   Using timeToFrame, converts start and end timestamps into frame numbers
#   If Else logic to see what quadrant to get a sample frame from for the ROI
#   ROI selection with popup messages
#   Opens video writer either using a quadrants dimensions or the ROI's
#   Loops over every frame between the timestamps and crops each frame to the specified region respectively
#   Each frame gets written out to disk and the loop increments
#   The writer is released after all frames have been edited. This prevents corruption of the newly saved video.
def saveVideosUsingFrames(quadrantNumber, voleEntryList, fps, cap, HEIGHT, WIDTH, DATE_OF_VIDEO, master, SAVED_VIDEO_PATH, progressBar):
    # Loop through each vole entry in the list
    for voleEntry in voleEntryList:
        # Convert timestamps to frames
        startingFrame = timeToFrame(voleEntry.getStartTime(),fps)
        print("Starting frame @: %s" % startingFrame)
        endingFrame = timeToFrame(voleEntry.getEndTime(),fps)
        print("Ending frame @: %s" % endingFrame)
        print("FPS @: %s" % fps)

        # Used as a counter to get the desired frames
        fc = startingFrame

        # Used to hold the number of frames needed to be captured.
        frameCount = endingFrame - startingFrame

        # Reset progress bar progression
        progressBar['value'] = 0 
        master.update()

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

        # ROI section. Let the user choose if they want to select a ROI. Popup message to display the decision they made. 
        popupmsg("How to use ROI", "Drag a ROI using the MOUSE.\n SPACE or ENTER submits the ROI.\n C will cancel the celected region.\n ESC quits the window.", master)
        r = cv2.selectROI("crop",img)
        cv2.destroyWindow("crop")
        if r != (0, 0, 0, 0):
            popupmsg("Success", "ROI selected was selected:\n x: %s\n y: %s\n width: %s\n height: %s" % (r[0], r[1], r[2], r[3]), master)
        elif r == (0, 0, 0, 0):
            popupmsg("Success", "Option for no ROI selected", master)

        # Append MetaData to the filename that will be written out. Specified as Date(MM-DD-YYYY), Timestamp(HH-MM-SS), Vole Number(#).
        splitDateAttributes = DATE_OF_VIDEO.split()
        saveVideoPathPlusMetadata = SAVED_VIDEO_PATH + ("%s-%s-%s_%s_%s.mp4" % (splitDateAttributes[1], splitDateAttributes[2], splitDateAttributes[4],  
                                                                                        splitDateAttributes[3].replace(':', "-"), voleEntry.getVoleNumber()))
        
        # Encoder to use for written clip
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        
        if r != (0, 0, 0, 0):
            # OpenCV Video Writer with dimensions for selected ROI
            writer= cv2.VideoWriter(saveVideoPathPlusMetadata, fourcc, fps, ( int(r[2]), int(r[3]) ))
        else:
            # OpenCV Video Writer with dimensions for regular quadrant
            writer= cv2.VideoWriter(saveVideoPathPlusMetadata, fourcc, fps, ( WIDTH, HEIGHT ))

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

            # If the user selected a ROI, crop the frame to the selected ROI
            if r != (0, 0, 0, 0):
                # Crop image to ROI
                originalFrame = originalFrame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

            # Wtire the newly cropped frame out to disk
            writer.write(originalFrame)

            # Incriment the frame counter by one frame
            fc += 1

            # Increment progress bar 
            progressBar['value'] = ((fc - startingFrame) / frameCount) * 100
            master.update()

            
        # Release the writer for each entry. This ensure the video is not corrupt after execution. 
        writer.release()
    

###########################################################
# END OF FUNCTION DEF
###########################################################

###########################################################
# MAIN FUNCTION
###########################################################
def main():
    ###########################################################
    # VARIABLE DEF
    ###########################################################
    voleArrayQ1 = []
    voleArrayQ2 = []
    voleArrayQ3 = []
    voleArrayQ4 = []

    # Global counters used to keep track of the number of voles input into each quadrant
    counterQ1 = queue.Queue(maxsize=1)
    counterQ1.put(0)
    counterQ2 = queue.Queue(maxsize=1)
    counterQ2.put(0)
    counterQ3 = queue.Queue(maxsize=1)
    counterQ3.put(0)
    counterQ4 = queue.Queue(maxsize=1)
    counterQ4.put(0)

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

    cap, fps = importVideo(VIDEO_PATH)

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

    # Progress bar widget to track process status
    progressBarQ1 = Progressbar(quad1, orient = HORIZONTAL, length = 100, mode = 'determinate')
    progressBarQ1.pack(padx=5, pady=10,side = BOTTOM)
    progressTrackerLabelQ1 = Label(quad1, text=' ', font=("Open Sanse", 13))
    progressTrackerLabelQ1.pack(padx=5, pady=5,side = BOTTOM)
    progressBarQ2 = Progressbar(quad2, orient = HORIZONTAL, length = 100, mode = 'determinate')
    progressBarQ2.pack(padx=5, pady=10,side = BOTTOM)
    progressTrackerLabelQ2 = Label(quad2, text=' ', font=("Open Sanse", 13))
    progressTrackerLabelQ2.pack(padx=5, pady=5,side = BOTTOM)
    progressBarQ3 = Progressbar(quad3, orient = HORIZONTAL, length = 100, mode = 'determinate')
    progressBarQ3.pack(padx=5, pady=10,side = BOTTOM)
    progressTrackerLabelQ3 = Label(quad3, text=' ', font=("Open Sanse", 13))
    progressTrackerLabelQ3.pack(padx=5, pady=5,side = BOTTOM)
    progressBarQ4 = Progressbar(quad4, orient = HORIZONTAL, length = 100, mode = 'determinate')
    progressBarQ4.pack(padx=5, pady=10,side = BOTTOM)
    progressTrackerLabelQ4 = Label(quad4, text=' ', font=("Open Sanse", 13))
    progressTrackerLabelQ4.pack(padx=5, pady=5,side = BOTTOM)

    # Pack on buttons to submit a batch job for processing.
    DoneQ1 = Button(quad1, text='Done!', width=30, state=DISABLED, command=lambda: batchProcess("Q1", voleArrayQ1, DoneQ1, fps, cap, HEIGHT, WIDTH, DATE_OF_VIDEO, 
                                                                                                master, SAVED_VIDEO_PATH, progressBarQ1, progressTrackerLabelQ1))
    DoneQ1.pack(padx=5, pady=10,side = BOTTOM)
    DoneQ2 = Button(quad2, text='Done!', width=30, state=DISABLED, command=lambda: batchProcess("Q2", voleArrayQ2, DoneQ2, fps, cap, HEIGHT, WIDTH, DATE_OF_VIDEO, 
                                                                                                master, SAVED_VIDEO_PATH, progressBarQ2, progressTrackerLabelQ2))
    DoneQ2.pack(padx=5, pady=10,side = BOTTOM)
    DoneQ3 = Button(quad3, text='Done!', width=30, state=DISABLED, command=lambda: batchProcess("Q3", voleArrayQ3, DoneQ3, fps, cap, HEIGHT, WIDTH, DATE_OF_VIDEO, 
                                                                                                master, SAVED_VIDEO_PATH, progressBarQ3, progressTrackerLabelQ3))
    DoneQ3.pack(padx=5, pady=10,side = BOTTOM)
    DoneQ4 = Button(quad4, text='Done!', width=30, state=DISABLED, command=lambda: batchProcess("Q4", voleArrayQ4, DoneQ4, fps, cap, HEIGHT, WIDTH, DATE_OF_VIDEO, 
                                                                                                master, SAVED_VIDEO_PATH, progressBarQ4, progressTrackerLabelQ4))
    DoneQ4.pack(padx=5, pady=10,side = BOTTOM)

    # Pack on buttons to dynamically add more Vole entries.
    Button(quad1, text='+Add Vole', width=30, command=lambda: addVoleEntry(voleArrayQ1, quad1, counterQ1, DoneQ1, progressTrackerLabelQ1)).pack(padx=5, pady=10,side = BOTTOM)
    Button(quad2, text='+Add Vole', width=30, command=lambda: addVoleEntry(voleArrayQ2, quad2, counterQ2, DoneQ2, progressTrackerLabelQ2)).pack(padx=5, pady=10,side = BOTTOM)
    Button(quad3, text='+Add Vole', width=30, command=lambda: addVoleEntry(voleArrayQ3, quad3, counterQ3, DoneQ3, progressTrackerLabelQ3)).pack(padx=5, pady=10,side = BOTTOM)
    Button(quad4, text='+Add Vole', width=30, command=lambda: addVoleEntry(voleArrayQ4, quad4, counterQ4, DoneQ4, progressTrackerLabelQ4)).pack(padx=5, pady=10,side = BOTTOM)

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

if __name__ == "__main__":
        main()
