
import scipy.io
import matplotlib.pyplot as plt

# Load NASA battery dataset
mat = scipy.io.loadmat("data/B0005.mat")
operations = mat["B0005"][0, 0]["cycle"][0]

# Select discharge cycles 47, 48 and 49
selected_cycles = [47, 48, 49]

discharge_number = 0
cycle_data = {}

for operation in operations:

    if operation["type"][0] != "discharge":
        continue

    discharge_number += 1

    if discharge_number not in selected_cycles:
        continue

    data = operation["data"][0, 0]

    time = data["Time"].flatten()
    time_minutes = (time - time[0]) / 60

    cycle_data[discharge_number] = {
        "time": time_minutes,
        "voltage": data["Voltage_measured"].flatten(),
        "current": data["Current_measured"].flatten(),
        "temperature": data["Temperature_measured"].flatten()
    }

# Create three comparison graphs
fig, axes = plt.subplots(3, 1, figsize=(11, 12))

for cycle_number, measurements in cycle_data.items():

    label = f"Cycle {cycle_number}"

    axes[0].plot(
        measurements["time"],
        measurements["voltage"],
        label=label
    )

    axes[1].plot(
        measurements["time"],
        measurements["current"],
        label=label
    )

    axes[2].plot(
        measurements["time"],
        measurements["temperature"],
        label=label
    )

axes[0].set_title("Voltage Comparison")
axes[0].set_ylabel("Voltage (V)")
axes[0].grid(True)
axes[0].legend()

axes[1].set_title("Current Comparison")
axes[1].set_ylabel("Current (A)")
axes[1].grid(True)
axes[1].legend()

axes[2].set_title("Temperature Comparison")
axes[2].set_xlabel("Time (minutes)")
axes[2].set_ylabel("Temperature (°C)")
axes[2].grid(True)
axes[2].legend()

plt.tight_layout()

plt.savefig(
    "outputs/cycle_47_48_49_comparison.png",
    dpi=300
)

plt.show()

print("Profile comparison completed.")
