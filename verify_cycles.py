
import scipy.io
import numpy as np

# Load NASA battery dataset
mat = scipy.io.loadmat("data/B0005.mat")
operations = mat["B0005"][0, 0]["cycle"][0]

selected = [47, 48, 49]
discharge_number = 0

for operation in operations:

    if operation["type"][0] != "discharge":
        continue

    discharge_number += 1

    if discharge_number not in selected:
        continue

    data = operation["data"][0, 0]

    time = data["Time"].flatten()
    voltage = data["Voltage_measured"].flatten()
    current = data["Current_measured"].flatten()
    temperature = data["Temperature_measured"].flatten()

    # Find maximum temperature
    max_temp_index = np.argmax(temperature)

    # Find minimum voltage
    min_voltage_index = np.argmin(voltage)

    # Find current closest to zero
    zero_current_index = np.argmin(np.abs(current))

    print(f"\nCYCLE {discharge_number}")
    print("-" * 30)

    print(
        f"Maximum temperature: "
        f"{temperature[max_temp_index]:.3f} °C"
    )

    print(
        f"Time at maximum temperature: "
        f"{(time[max_temp_index]-time[0])/60:.2f} min"
    )

    print(
        f"Minimum voltage: "
        f"{voltage[min_voltage_index]:.3f} V"
    )

    print(
        f"Time at minimum voltage: "
        f"{(time[min_voltage_index]-time[0])/60:.2f} min"
    )

    print(
        f"Current closest to zero: "
        f"{current[zero_current_index]:.4f} A"
    )

    print(
        f"Time at that current: "
        f"{(time[zero_current_index]-time[0])/60:.2f} min"
    )

    print(
        f"Discharge duration: "
        f"{(time[-1]-time[0])/60:.2f} min"
    )
