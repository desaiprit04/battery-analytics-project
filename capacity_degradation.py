
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Load the extracted discharge-cycle data
df = pd.read_csv("outputs/discharge_cycle_summary.csv")

# 2. Calculate reference capacity
reference_capacity = df["capacity_Ah"].iloc[0]

# 3. Calculate State of Health (SoH)
df["SoH_percent"] = (
    df["capacity_Ah"] / reference_capacity
) * 100

# 4. Calculate capacity retention
df["capacity_retention_percent"] = df["SoH_percent"]

# 5. Display important results
print("BATTERY CAPACITY ANALYSIS")
print("-------------------------")

print(f"Reference capacity: {reference_capacity:.4f} Ah")

print(
    f"Final capacity: "
    f"{df['capacity_Ah'].iloc[-1]:.4f} Ah"
)

print(
    f"Final relative SoH: "
    f"{df['SoH_percent'].iloc[-1]:.2f}%"
)

print(
    f"Capacity change: "
    f"{df['capacity_Ah'].iloc[-1] - reference_capacity:.4f} Ah"
)

print("\nFirst five cycles:")
print(df[[
    "discharge_cycle",
    "capacity_Ah",
    "SoH_percent"
]].head())

print("\nLast five cycles:")
print(df[[
    "discharge_cycle",
    "capacity_Ah",
    "SoH_percent"
]].tail())

# 6. Create output directory
os.makedirs("outputs", exist_ok=True)

# 7. Plot capacity degradation
# Create first graph
plt.figure(figsize=(10, 5))

plt.plot(
    df["discharge_cycle"],
    df["capacity_Ah"],
    marker="o",
    markersize=3,
    label="Discharge capacity"
)

plt.xlabel("Discharge cycle")
plt.ylabel("Capacity (Ah)")
plt.title("NASA B0005 - Battery Capacity Degradation")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("outputs/capacity_degradation.png", dpi=300)


# Create second graph
plt.figure(figsize=(10, 5))

plt.plot(
    df["discharge_cycle"],
    df["SoH_percent"],
    label="Relative capacity retention"
)

plt.axhline(
    y=80,
    linestyle="--",
    label="80% reference line"
)

plt.xlabel("Discharge cycle")
plt.ylabel("Relative capacity retention (%)")
plt.title("NASA B0005 - Relative Battery State of Health")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("outputs/battery_soh.png", dpi=300)


# Save updated dataset
df.to_csv(
    "outputs/battery_health_analysis.csv",
    index=False
)

# Display both figures
plt.show()

print("Analysis completed successfully!")

# Detailed battery health results

initial_capacity = df["capacity_Ah"].iloc[0]
final_capacity = df["capacity_Ah"].iloc[-1]

capacity_loss = initial_capacity - final_capacity

capacity_loss_percent = (
    capacity_loss / initial_capacity
) * 100

# Find first cycle below 80% relative capacity
below_80 = df[df["SoH_percent"] < 80]

print("\nBATTERY HEALTH RESULTS")
print("----------------------")

print(f"Initial capacity: {initial_capacity:.4f} Ah")
print(f"Final capacity: {final_capacity:.4f} Ah")

print(f"Capacity loss: {capacity_loss:.4f} Ah")

print(
    f"Capacity degradation: "
    f"{capacity_loss_percent:.2f}%"
)

print(
    f"Final relative SoH: "
    f"{df['SoH_percent'].iloc[-1]:.2f}%"
)

if not below_80.empty:
    print(
        "First cycle below 80% relative capacity:",
        int(below_80.iloc[0]["discharge_cycle"])
    )
else:
    print("Capacity remained above 80%.")

