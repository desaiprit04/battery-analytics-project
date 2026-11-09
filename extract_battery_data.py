
import scipy.io
import numpy as np
import pandas as pd
import os

# 1. Load NASA battery dataset
mat_data = scipy.io.loadmat("data/B0005.mat")
cycles = mat_data["B0005"][0, 0]["cycle"][0]

# 2. Prepare a list to store discharge-cycle information
discharge_records = []

discharge_number = 0

# 3. Extract every discharge operation
for operation_index, operation in enumerate(cycles):

    operation_type = operation["type"][0]

    if operation_type == "discharge":

        discharge_number += 1

        # Extract measurements
        data = operation["data"][0, 0]

        voltage = data["Voltage_measured"].flatten()
        current = data["Current_measured"].flatten()
        temperature = data["Temperature_measured"].flatten()
        time = data["Time"].flatten()

        # Extract cycle-level discharge capacity (Ah)
        capacity = float(data["Capacity"].squeeze())

        # Extract ambient temperature
        ambient_temp = float(
            operation["ambient_temperature"].squeeze()
        )

        # Calculate summary statistics
        record = {
            "discharge_cycle": discharge_number,
            "operation_index": operation_index + 1,
            "ambient_temperature_C": ambient_temp,
            "capacity_Ah": capacity,
            "mean_voltage_V": np.mean(voltage),
            "min_voltage_V": np.min(voltage),
            "max_voltage_V": np.max(voltage),
            "mean_current_A": np.mean(current),
            "mean_temperature_C": np.mean(temperature),
            "max_temperature_C": np.max(temperature),
            "duration_s": time[-1] - time[0],
            "measurement_points": len(time)
        }

        discharge_records.append(record)

# 4. Convert records into a Pandas DataFrame
df = pd.DataFrame(discharge_records)

# 5. Display results
print("\nDischarge Cycle Summary")
print("-----------------------")

print(df.head())

print("\nDataFrame information:")
print(df.info())

print("\nStatistical summary:")
print(df.describe())

# 6. Save extracted data
os.makedirs("outputs", exist_ok=True)

df.to_csv(
    "outputs/discharge_cycle_summary.csv",
    index=False
)

print("\nExtracted discharge cycles:", len(df))
print("CSV file saved successfully!")
