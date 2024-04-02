import pickle

# Replace 'dist.pkl' with the path to your actual pickle file
pickle_file_path = 'calibration.pkl'

# Load the distortion coefficients from the pickle file
with open(pickle_file_path, 'rb') as file:
    distortion_coefficients = pickle.load(file)

# Print the distortion coefficients
print("Calibration Coefficients:")
print(distortion_coefficients)
