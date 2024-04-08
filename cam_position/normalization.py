import numpy as np

x_camera_rotation = -90
# Need to fix to an angle
y_camera_rotation = 0


# Parameter x_or_y
#   When true - x camera
#   When false - y camera

def transformCameraCoordinates(camera_data, x_or_y):
    
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

    raw_positions = camera_data

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

    return positions



if __name__ == '__main__':
    
    # Sample data: XYZ coordinates of three points
    test_data = np.array([
            [0.1561765, 0.08904364, 0.41930943],
            [0.15295053, 0.05556669, 0.41380159],
            [0.11283635, 0.02458074, 0.41529165]
        ])
    
    # Use the X-Axis
    p_x_or_y = True
    
    transformed_points = transformCameraCoordinates(test_data, p_x_or_y)
    
    print(transformed_points)
