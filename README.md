# Robot Arm Control

## Running the Project

### Installing Dependencies
In the root directory of the project, run the command:
```
pip install -r requirements.txt
```
### Running the Application
In the root directory of the project, run the command:
```
python -m ui.myapp
```

### Description

#### Project Overview

The Robot Arm Control project is one sponsored by Dr. Won from South Dakota State University's Department of Electrical Engineering & Computer Science. The project consists of a graphical user interface (GUI) for controlling a robotic arm (LewanSoul xArm) with a pre-existing Python application programming interface (API). The GUI integrates cameras to capture real-time visual data and employs ArUco markers for accurate pose estimation of the arm. From the pose estimation, a 3D model of the arm’s current state is generated in the GUI. The control interface allows for basic robotic movements to rotate each motor, or “servo”, of the arm and object manipulation, but it also allows for more complex movements called “macros”. The pose estimation data of the ArUco markers will have potential future use in AI and machine learning applications by graduate students.

#### Here is a breakdown of the main directories of the project, with notes about the purpose of some of the main files:

##### arm_control

This directory’s files contain code for API’s used by the graphical user interface (GUI) for controlling the robot arm.

##### cam_position

This directory’s files contain code for extracting the pose estimation data (translation vector/rotation vectors) of the ArUco markers attached to the arm from camera frames. Three different cameras are used in this project on the robot arm frame/platform– one for the X, Y, and Z axis of the frame.

##### machine_learning

This directory is currently empty– intended for potential future contributors of the project to use for AI purposes.

##### model

The model directory contains code for creating a 3D model widget based off the ArUco position data extracted from the cam_position module..

##### ui

This contains all the PyQt5 files/widgets used to make the GUI. myapp.py is the driver program for the UI.
