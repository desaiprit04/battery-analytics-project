
import scipy.io

# Path to the NASA battery dataset
file_path = "data/B0005.mat"

# Load MATLAB file
mat_data = scipy.io.loadmat(file_path)

# Display dataset variables
print("NASA Battery Dataset")
print("--------------------")

print("\nAvailable variables:")

for key in mat_data.keys():
    if not key.startswith("__"):
        print(key)
