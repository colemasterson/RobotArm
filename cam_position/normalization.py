import numpy as np
import json

x_camera_rotation = -90
# Need to fix to an angle
y_camera_rotation = 180

# Parameter x_or_y
#   When true - x camera
#   When false - y camera

file_path = 'cam_position/current_position.json'
backup_file_path = 'cam_position/backup_position.json'

def getPositionData():
    try:
        # Open the JSON file for reading
        with open(file_path, 'r') as file:
            # Parse the JSON file and convert it into a Python dictionary
            data = json.load(file)

        if not all(marker in data for marker in ['1', '2', '3']):
            print("Not all markers detected, loading backup data.")
            with open(backup_file_path, 'r') as file:
                data = json.load(file)

        # Initialize the camera position arrays
        camera_tvecs = []
        camera_rvecs = []

        # Order the keys as per requirement
        keys_order = ['1', '2', '3']

        for key in keys_order:
            marker = data.get(key)
            if marker is not None:  # Check if the marker exists
                # Append the entire tvec as a list to the camera_tvecs
                camera_tvecs.append(marker['tvec'])
                # Convert rvec to a tuple and append to the camera_rvecs
                camera_rvecs.append(tuple(marker['euler_angles']))

    except FileNotFoundError:
        print(f"No file found at '{file_path}'. Please check the file path.")
        return [], []  # Return empty lists in case of error
    except json.JSONDecodeError:
        print("Error decoding JSON. Please check the file content.")
        return [], []  # Return empty lists in case of error
    
    
    list_of_tuples = [tuple(lst) for lst in camera_tvecs]

    # Create a NumPy array from the list of tuples
    camera_tvecs = np.array(list_of_tuples, dtype=object)

    return camera_tvecs, camera_rvecs

def transformCameraCoordinates(camera_position_data, x_or_y):
    
    rotation_needed = 0
    
    if x_or_y == True:
        rotation_needed = x_camera_rotation
    else:
        rotation_needed = y_camera_rotation
    
    def rotate_points(points, degrees, x_axis=0, y_axis=0, z_axis=0):
        """
        Rotates a set of points around the specified axes (x, y, z) by a given angle.
        
        Parameters:
        - points: An array of points to rotate.
        - degrees: The rotation angle in degrees.
        - x_axis, y_axis, z_axis: Flags indicating which axis to rotate around (1 for true, 0 for false).
        
        Returns:
        - The rotated points as a numpy array.
        """
        theta = np.radians(degrees)  # Convert degrees to radians
        
        # Rotation matrices around the x, y, and z axes
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(theta), -np.sin(theta) * x_axis],
            [0, np.sin(theta) * x_axis, np.cos(theta)]
        ])
        
        Ry = np.array([
            [np.cos(theta), 0, np.sin(theta) * y_axis],
            [0, 1, 0],
            [-np.sin(theta) * y_axis, 0, np.cos(theta)]
        ])
        
        Rz = np.array([
            [np.cos(theta), -np.sin(theta) * z_axis, 0],
            [np.sin(theta) * z_axis, np.cos(theta), 0],
            [0, 0, 1]
        ])
        
        # Apply the rotation
        if x_axis:
            points = points @ Rx
        if y_axis:
            points = points @ Ry
        if z_axis:
            points = points @ Rz
            
        return points

    raw_positions = camera_position_data
    
    x_data = np.array([
            [0.1561765, 0.08904364, 0.41930943],
            [0.15295053, 0.05556669, 0.41380159],
            [0.11283635, 0.02458074, 0.41529165]
        ])

    # Min-Max Normalization
    min_max_normalized_positions = (raw_positions - raw_positions.min()) / (raw_positions.max() - raw_positions.min())

    # Z-Score Normalization (Standardization)
    mean = raw_positions.mean()
    std = raw_positions.std()
    z_score_normalized_data = (raw_positions - mean) / std

    # Move the coordinates to the origin
    # ---------------------------------------
    # Choose the first point as the reference to translate all points
    translation_reference = z_score_normalized_data[0]

    # Translate all points so the first point becomes the origin
    positions = z_score_normalized_data - translation_reference

    # def rotate_points(points, degrees, x_axis=0, y_axis=0, z_axis=0)
    positions = rotate_points(positions, rotation_needed, 1, 0, 0)

    # if x_or_y == True:
    #     # def rotate_points(points, degrees, x_axis=0, y_axis=0, z_axis=0)
    #     positions = rotate_points(positions, rotation_needed, 1, 0, 0)
    # else:
    #     # def rotate_points(points, degrees, x_axis=0, y_axis=0, z_axis=0)
    #     positions = rotate_points(positions, rotation_needed, 1, 0, 0)

    return positions



if __name__ == '__main__':
    
    tvecs, rvecs = getPositionData()

    # Use the X-Axis
    p_x_or_y = True
    
    transformed_points = transformCameraCoordinates(tvecs, p_x_or_y)
    
    # print("Transformed Points: \n", np.array(transformed_points))
    # print("Euler Angles: ", "\n", rvecs)

    
    # # Do on X camera points
    # x_data = np.array([
    #         [0.1561765, 0.08904364, 0.41930943],
    #         [0.15295053, 0.05556669, 0.41380159],
    #         [0.11283635, 0.02458074, 0.41529165]
    #     ])
    
    # # Use the X-Axis
    # p_x_or_y = True
    
    # transformed_points = transformCameraCoordinates(x_data, p_x_or_y)
    
    # print("X-Camera Transformed Points\n", transformed_points)
    
    # Do on Y camera points
    # y_data = np.array([
    #     [0.14846807, 0.0959883, 0.40869124],
    #     [0.14351266, 0.06353426, 0.40816555],
    #     [0.15223124, 0.01297262, 0.41260389]
    # ])
    
    # Use the Y-Axis
    # p_x_or_y = False
    
    # transformed_points = transformCameraCoordinates(y_data, p_x_or_y)
    
    # print("Y-Camera Transformed Points\n", transformed_points)

#  (0., 0., 0.) 
#  (0.03288238,  0.0034883, -0.21535375)  
#  (0.02497109, -0.02596299, -0.55086326) 

# ( 0.,         0.,          0.        )
# (-0.03288238, 0.21535375,  0.0034883 )
# ( 0.02497109, 0.55086326, -0.02596299)
