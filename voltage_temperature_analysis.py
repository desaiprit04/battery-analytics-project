
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

# Load NASA battery dataset
mat_data = scipy.io.loadmat("data/B0005.mat")
cycles = mat_data["B0005"][0, 0]["cycle"][0]

# Select first discharge operation
for operation in cycles:

    if operation["type"][0] == "discharge":
        data = operation["data"][0, 0]
        break

# Extract measurements
voltage = data["Voltage_measured"].flatten()
current = data["Current_measured"].flatten()
temperature = data["Temperature_measured"].flatten()
time = data["Time"].flatten()

# Convert time into minutes
time_minutes = (time - time[0]) / 60

# Create three separate plots
fig, axes = plt.subplots(3, 1, figsize=(10, 12))

# Voltage analysis
axes[0].plot(time_minutes, voltage)
axes[0].set_title("Battery Voltage During Discharge")
axes[0].set_ylabel("Voltage (V)")
axes[0].grid(True)

# Current analysis
axes[1].plot(time_minutes, current)
axes[1].set_title("Battery Current During Discharge")
axes[1].set_ylabel("Current (A)")
axes[1].grid(True)

# Temperature analysis
axes[2].plot(time_minutes, temperature)
axes[2].set_title("Battery Temperature During Discharge")
axes[2].set_xlabel("Time (minutes)")
axes[2].set_ylabel("Temperature (°C)")
axes[2].grid(True)

plt.tight_layout()

plt.savefig(
    "outputs/voltage_current_temperature.png",
    dpi=300
)

plt.show()

# Print measurement statistics
print("\nDISCHARGE MEASUREMENT SUMMARY")
print("-----------------------------")

print(f"Voltage range: {voltage.min():.3f} - {voltage.max():.3f} V")
print(f"Mean current: {np.mean(current):.3f} A")
print(f"Temperature range: {temperature.min():.2f} - {temperature.max():.2f} °C")
print(f"Discharge duration: {time_minutes[-1]:.2f} minutes")
