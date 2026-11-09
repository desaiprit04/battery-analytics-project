
import scipy.io

# Load NASA battery dataset
mat_data = scipy.io.loadmat("data/B0005.mat")

# Access battery information
battery = mat_data["B0005"]

print("Battery data type:", type(battery))
print("Battery shape:", battery.shape)
print("Battery structure:", battery.dtype)

# Extract the cycle information
cycles = battery[0, 0]["cycle"]

print("\nTotal number of cycles:", len(cycles))

# Display the first cycle
first_cycle = cycles[0]

print("\nFirst cycle information:")
print(first_cycle.dtype)
print(first_cycle.shape)

