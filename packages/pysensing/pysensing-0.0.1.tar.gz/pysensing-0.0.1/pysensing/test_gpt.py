import numpy as np

# Generate a random 4D matrix
matrix = np.random.random((10, 10))

# Define the file name
file_name = "sample_label.npy"

# Save the matrix to .npy file
np.save(file_name, matrix)

print("Matrix saved to", file_name)