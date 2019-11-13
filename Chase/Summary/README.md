# Summary
This is a summary of the work I have completed for the Donaldson Lab.

## [UI Lab Capture](https://github.com/donaldsonlab/UI-lab-capture)
The goal was to create a simple GUI to interface with scientific instruments. The equipment being used included two Blackfly S cameras and a labjack U3-LV. The **UI Lab Capture** solves the problem of making mistakes while initializing different equipment for an experiment. I used multi-threading to help to organize the scheduling of tasks and multi-processing to relieve the stress caused by computatonally intensive tasks.The result was no missed frames which means data can be aligned properly and no post processing is needed to be done. This project taught me alot about outsourcing for help, project deadlines, and how to backtrack once you hit a dead end. 

<p align="center">
  <img width="660" height="400" src="Images/gui.png">
</p>
<p align="center">
  <img width="460" height="300" src="Images/Bad_gif.gif">
</p>
<p align="center">
  <img width="560" height="300" src="Images/cam.png">
</p>
<p align="center">
  <img width="560" height="300" src="Images/buffer.png">
</p>
<p align="center">
  <img width="460" height="300" src="Images/Okay_gif.gif">
</p>
<p align="center">
  <img width="460" height="300" src="Images/process.png">
</p>
<p align="center">
  <img width="460" height="300" src="Images/Good_gif.gif">
</p>
<p align="center">
  <img width="560" height="300" src="Images/chart.png">
</p>
<p align="center">
  <img width="460" height="400" src="Images/UILabCapture.png">
</p>

## [Automating behavioral scoring using Deep Lab Cut](https://github.com/donaldsonlab/DonaldsonDLC)
Currently there is lots of fantastic data, but someone has to manually watch and score each and every frame which can take hours. In adition we can only ask basic questions, like “Did they mate?”. Using markerless pose estimation, we can begin to analyze and quantify behavioral scoring in areas like mating bouts, partner preferences, and operant paradigms. The project uses a convolutional neural network to analyze videos which returns a labeled video, a csv formatted file of poses, and other metadata about the analyzed video. The csv file is then processed using a python script and graphed to show the covariation of movement between two voles. When complete, this project will save the lab hours of time which previously would have been used to hand mark each video.

<p align="center">
  <img width="460" height="300" src="Images/dlc1.gif">
</p>
<p align="center">
  <img width="460" height="300" src="Images/dlcgoal.gif">
</p>
