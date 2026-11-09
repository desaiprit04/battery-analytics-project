
import scipy.io

# Load dataset
mat_data = scipy.io.loadmat("data/B0005.mat")

# Access cycle information
battery = mat_data["B0005"]
cycles = battery[0, 0]["cycle"][0]

print("Total operations:", len(cycles))
print("\nFirst 10 operations:")
print("--------------------")

for i in range(10):

    operation = cycles[i]

    operation_type = operation["type"][0]
    ambient_temp = operation["ambient_temperature"][0][0]

    print(
        f"Operation {i + 1}: "
        f"Type = {operation_type}, "
        f"Ambient temperature = {ambient_temp} °C"
    )
