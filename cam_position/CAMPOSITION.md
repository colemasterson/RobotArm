# Project Directory Overview

This document provides a top-level overview of the files and directories within the `cam_position` directory.

## Directories

### `aruco_markers`
- Temporary storage location for the ArUco markers generated in `generate.py`.

### `calis`
- Storage location for the calibration images used in `calibration.py`.

### `estimation_photos`
- Storage location for images taken after an arm movement, and are then used in the `poseEstimateFolder.py`. Images are captured in widgets such as `../ui/ServoContolsTab` and `../ui/CreateMacroSequence` and stored here, for each camera.

## Files

### `__init__.py`
- Used for referencing in the module.

### `backup_position.json`
- Backup json storing position data for use in cases where markers cannot be detected by the arm.

### `calibration.pkl`
- Pickle file contained serialized data of calibration information pertaining to the cameras used in this project. Generated upon successful execution of `calibration.py`.

### `calibration.py`
- Script used to calibrate the cameras for use in pose estimation. Outputs 3 pickle files: `calibration.pkl` (calibration values), `cameraMatrix.pkl` (contains the camera matrix information), and `dist.pkl` (distortion matrix of the camera).

### `cameraMatrix.pkl`
- Pickle file containing the camera matrix obtained in `calibration.py`.

### `current_position.json`
- Output of the `estimatePoseFolder.py` script. Contains 3 values for each marker detected: 
 1. The translation vector (tvec) of the marker in x,y,z coordinates.
 2. The rotation vector (rvec) of the marker.
 3. The euler angles (euler_angles) of the marker calculated within the `estimatePoseFolder.py` script. 

### `detect.py`
- Unused in the project, but part of the process when identifying the location of an ArUco marker in the frame.

### `dist.pkl`
- Pickle file containing the distorion coefficients of the camera.

### `estimatePoseFolder.py`
- Main script for detecting ArUco markers, calculating the estimated pose of the markers, and returning them to the user in a json file `current_position.json`.

### `generate.py`
- Generates an arUco marker based on the specified arUco marker type, size, and ID.

### `normalization.py`
- Normalizes the data retrieved from `current_position.json` for use in the 3D model.

### `poseEstimation.py`
- Unused in the project, but part of the process when identifying the estimated pose of an ArUco marker in the frame.
