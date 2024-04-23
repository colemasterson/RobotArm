
import numpy as np
import cv2
import os
import json
from scipy import stats
from collections import defaultdict

class PoseEstimator:
    def __init__(self):
        self.aruco_type = cv2.aruco.DICT_5X5_100
        self.arucoDict = cv2.aruco.getPredefinedDictionary(self.aruco_type)
        self.arucoParams = cv2.aruco.DetectorParameters()
        self.matrix_coefficients = np.array(((1.02576077e+03, 0, 3.17826827e+02),(0, 1.03079475e+03, 2.29146820e+02),(0,0,1)))
        self.distortion_coefficients = np.array((-3.24419802e-02,  9.59963589e-01,  1.32922653e-03, 1.65307029e-03, -2.71855997e+00))

    def read_images_from_directory(self, directory_path):
        """
        Reads all images from the specified directory.
        
        Parameters:
            directory_path (str): The path to the directory containing images.
            
        Returns:
            list of images read from the directory.
        """
        images = []
        for filename in os.listdir(directory_path):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(directory_path, filename)
                img = cv2.imread(img_path)
                images.append(img)
        return images

    def estimate_pose_on_images(self, images):
        """
        Estimates the pose on each image using the pose estimation function.
        
        Parameters:
            images (list): A list of images on which to perform pose estimation.
            
        Returns:
            list of tuples containing rounded tvec and rvec values for each image.
        """
        marker_estimations = defaultdict(list)

        for img in images:
            (corners, ids, rejected) = cv2.aruco.detectMarkers(img, self.arucoDict, parameters=self.arucoParams)
            
            # Verify at least one ArUco marker was detected
            if ids is not None:
                for i, corner in enumerate(corners):
                    rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, self.matrix_coefficients, self.distortion_coefficients)
                    # Print the translation and rotation vectors for each marker
                    # print(f"Marker {ids[i]}:")
                    # print(f"Translation Vector (tvec): {tvec}")
                    # print(f"Rotation Vector (rvec): {rvec}")
                    # print(f"Rotation Vector in Euler Angles: {rotation_vector_to_euler_angles(rvec)}")
                    # Append the tvec and rvec values to the list corresponding to this marker ID
                    marker_id = ids[i][0]
                    marker_estimations[marker_id].append((tvec, rvec))
        
        return marker_estimations

    def calculate_mode_per_marker(self, marker_estimations, decimals=4):
        """
        Calculates the mode of the rounded tvec and rvec values for each marker ID,
        considering each component separately and rounding to the specified number of decimals.
        This is done to remove outliers from pose estimation
        Parameters:
            marker_estimations (dict): A dictionary mapping marker IDs to lists of (tvec, rvec) tuples.
            decimals (int): The number of decimal places to round each vector component to.
            
        Returns:
            dict: A dictionary mapping marker IDs to mode of rounded tvec and rvec values.
        """
        mode_estimations = {}
        for marker_id, estimations in marker_estimations.items():
            # Convert the list of tuples into numpy arrays for easier manipulation
            tvecs = np.array([estimation[0] for estimation in estimations]).reshape(-1, 3)
            rvecs = np.array([estimation[1] for estimation in estimations]).reshape(-1, 3)

            # Round the components
            tvecs_rounded = np.round(tvecs, decimals=decimals)
            rvecs_rounded = np.round(rvecs, decimals=decimals)

            # Calculate mode for each component of rounded vectors
            mode_tvec = [stats.mode(tvecs_rounded[:, i], axis=0).mode for i in range(3)]
            mode_rvec = [stats.mode(rvecs_rounded[:, i], axis=0).mode for i in range(3)]
        
            mode_estimations[marker_id] = (mode_tvec, mode_rvec)
            
        return mode_estimations


    def rotation_vector_to_euler_angles(self, rvec):
        # Convert rotation vector to rotation matrix
        R, _ = cv2.Rodrigues(rvec)
        
        # Calculate Euler angles from the rotation matrix
        sy = np.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
        singular = sy < 1e-6
        
        if not singular:
            x = np.arctan2(R[2,1], R[2,2])
            y = np.arctan2(-R[2,0], sy)
            z = np.arctan2(R[1,0], R[0,0])
        else:
            x = np.arctan2(-R[1,2], R[1,1])
            y = np.arctan2(-R[2,0], sy)
            z = 0
        
        # Convert from radians to degrees
        x = np.degrees(x)
        y = np.degrees(y)
        z = np.degrees(z)
        
        return x, y, z
          
    def adjust_marker_data(self, marker_id, euler_angles, use_secondary_camera):
        # Convert tuple to list for mutability
        euler_angles = list(euler_angles)

        # Define the mapping from new marker IDs to original marker IDs
        id_mapping = {4: 3, 5: 2, 6: 1}
        
        # Check if the detected marker ID is one of the new ones
        if marker_id in id_mapping:
            # Map the marker ID to its corresponding original ID
            new_marker_id = id_mapping[marker_id]
            
            # Rotate the z value of the Euler angles by 180 degrees
            adjusted_euler_angles = list(euler_angles)
            adjusted_euler_angles[1] = (euler_angles[1] + 180) % 360
            #adjusted_euler_angles[0] = (euler_angles[2] + 180) % 360
            
            # Further adjust if using the secondary camera
            if use_secondary_camera:
                adjusted_euler_angles[1] = (adjusted_euler_angles[1] - 90) % 360
            
            return new_marker_id, euler_angles
        else:
            # Adjust if using the secondary camera
            if use_secondary_camera:
                euler_angles[1] = (euler_angles[1] - 90) % 360
            
            return marker_id, euler_angles

        
    def updatePos(self, s6angle):
        photo_path = "cam_position/estimation_photos/"
        use_secondary_camera = False
        print("Updating Position...")
        print(f"Current s6angle: {s6angle}")
        if s6angle > 60.0 or s6angle < -46:
            print("Servo 6 rotated towards camera y, using camera y image path(secondary).")
            use_secondary_camera = True
            photo_path += "secondary/"
        else:
            print("Using camera x image path(primary).")
            photo_path += "primary/"

        images = self.read_images_from_directory(photo_path)
        marker_estimations = self.estimate_pose_on_images(images)
        mode_estimations = self.calculate_mode_per_marker(marker_estimations)

        marker_data = {}

        for marker_id, (mode_tvec, mode_rvec) in mode_estimations.items():
            # Adjust marker ID and Euler angles if necessary
            adjusted_marker_id, adjusted_euler_angles = self.adjust_marker_data(marker_id, self.rotation_vector_to_euler_angles(np.array(mode_rvec).reshape((3, 1))), use_secondary_camera)
            
            print(f"Marker ID: {adjusted_marker_id} Mode TVEC: X={mode_tvec[0]}, Y={mode_tvec[1]}, Z={mode_tvec[2]}, Mode RVEC: X={mode_rvec[0]}, Y={mode_rvec[1]}, Z={mode_rvec[2]}")

            # Store the marker data using the stringified adjusted marker ID as key
            marker_id_str = str(adjusted_marker_id)
            marker_data[marker_id_str] = {
                "tvec": mode_tvec,
                "rvec": mode_rvec,
                "euler_angles": adjusted_euler_angles
            }
            second_cam_bool = 0
            if use_secondary_camera:
                second_cam_bool =1
            all_data = {
                "use_secondary_camera": second_cam_bool,
                **marker_data
            }
        with open('cam_position/current_position.json', 'w') as json_file:
            json.dump(all_data, json_file, indent=4)

        print('finished writing to json file')
