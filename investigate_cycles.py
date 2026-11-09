
import scipy.io
import numpy as np
import pandas as pd

mat = scipy.io.loadmat("data/B0005.mat")
cycles = mat["B0005"][0, 0]["cycle"][0]

records = []

discharge_number = 0

for operation in cycles:

    if operation["type"][0] != "discharge":
        continue

    discharge_number += 1
    data = operation["data"][0, 0]

    voltage = data["Voltage_measured"].flatten()
    current = data["Current_measured"].flatten()
    temperature = data["Temperature_measured"].flatten()

    records.append({
        "cycle": discharge_number,
        "capacity_Ah": float(data["Capacity"].squeeze()),
        "mean_voltage_V": np.mean(voltage),
        "min_voltage_V": np.min(voltage),
        "mean_current_A": np.mean(current),
        "mean_temperature_C": np.mean(temperature),
        "max_temperature_C": np.max(temperature),
        "duration_s": (
            data["Time"].flatten()[-1]
            - data["Time"].flatten()[0]
        )
    })

df = pd.DataFrame(records)

selected = df[df["cycle"].between(44, 51)]

print("\nCOMPARISON OF CYCLES 44–51")
print("--------------------------")

print(selected.round(4).to_string(index=False))
