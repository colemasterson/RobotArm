
import numpy as np
import cv2
import os
from scipy import stats

ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

def read_images_from_directory(directory_path):
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

def estimate_pose_on_images(images):
    """
    Estimates the pose on each image using the pose estimation function.
    
    Parameters:
        images (list): A list of images on which to perform pose estimation.
        
    Returns:
        list of tuples containing rounded tvec and rvec values for each image.
    """
    estimations = []
    for img in images:
        # Assuming pose_estimation is a function from the provided script
        tvec, rvec = pose_estimation(img)
        rounded_tvec = np.round(tvec, 2)
        rounded_rvec = np.round(rvec, 2)
        estimations.append((rounded_tvec, rounded_rvec))
    return estimations

def calculate_mode(estimations):
    """
    Calculates the mode of each field in tvec and rvec to exclude outliers.
    
    Parameters:
        estimations (list): A list of tuples containing tvec and rvec values for each estimation.
        
    Returns:
        Tuple of mode values for tvec and rvec.
    """
    tvecs = np.array([est[0] for est in estimations])
    rvecs = np.array([est[1] for est in estimations])
    
    mode_tvec = stats.mode(tvecs, axis=0).mode[0]
    mode_rvec = stats.mode(rvecs, axis=0).mode[0]
    
    return mode_tvec, mode_rvec

def pose_estimation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[aruco_type])
    #cv2.aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_dict_type)
    arucoParams = cv2.aruco.DetectorParameters()


    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, arucoDict, parameters=arucoParams)
	#corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict,parameters=parameters)
        
    if len(corners) > 0:
        for i in range(0, len(ids)):
           
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, matrix_coefficients, distortion_coefficients)
            # Print the translation and rotation vectors for each marker
            print(f"Marker {ids[i]}:")
            print(f"Translation Vector (tvec): {tvec}")
            print(f"Rotation Vector (rvec): {rvec}")
            print(f"Roation Vector in Euler Angles: {rotation_vector_to_euler_angles(rvec)}")
            cv2.aruco.drawDetectedMarkers(frame, corners) 

            cv2.drawFrameAxes(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)  

    return frame

def rotation_vector_to_euler_angles(rvec):
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

aruco_type = "DICT_5X5_100"

arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[aruco_type])
arucoParams = cv2.aruco.DetectorParameters()


intrinsic_camera = np.array(((1.02576077e+03, 0, 3.17826827e+02),(0, 1.03079475e+03, 2.29146820e+02),(0,0,1)))
distortion = np.array((-3.24419802e-02,  9.59963589e-01,  1.32922653e-03, 1.65307029e-03, -2.71855997e+00))

# Main function to tie everything together
if __name__ == "__main__":
    directory_path = "estimation_photos"
    images = read_images_from_directory(directory_path)
    estimations = estimate_pose_on_images(images)
    mode_tvec, mode_rvec = calculate_mode(estimations)
    print("Mode TVEC:", mode_tvec)
    print("Mode RVEC:", mode_rvec)
