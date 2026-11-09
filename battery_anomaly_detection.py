
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# 1. Load battery health dataset
df = pd.read_csv("outputs/battery_health_analysis.csv")

# 2. Select relevant battery features
features = [
    "capacity_Ah",
    "mean_voltage_V",
    "mean_current_A",
    "mean_temperature_C",
    "max_temperature_C",
    "duration_s"
]

X = df[features].copy()

# 3. Standardise features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Build Isolation Forest model
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

# 5. Detect unusual cycles
df["anomaly_label"] = model.fit_predict(X_scaled)

# -1 = anomaly
#  1 = normal

df["anomaly"] = df["anomaly_label"].map({
    -1: "Anomaly",
    1: "Normal"
})

# 6. Display results
print("\nBATTERY ANOMALY DETECTION")
print("-------------------------")

print(df["anomaly"].value_counts())

print("\nDetected unusual cycles:")

print(
    df.loc[
        df["anomaly"] == "Anomaly",
        [
            "discharge_cycle",
            "capacity_Ah",
            "max_temperature_C",
            "duration_s"
        ]
    ].to_string(index=False)
)

# 7. Visualise capacity and anomalies
plt.figure(figsize=(10, 5))

normal = df[df["anomaly"] == "Normal"]
anomalies = df[df["anomaly"] == "Anomaly"]

plt.scatter(
    normal["discharge_cycle"],
    normal["capacity_Ah"],
    label="Normal cycles"
)

plt.scatter(
    anomalies["discharge_cycle"],
    anomalies["capacity_Ah"],
    marker="x",
    s=80,
    label="Detected anomalies"
)

plt.xlabel("Discharge cycle")
plt.ylabel("Capacity (Ah)")
plt.title("Battery Capacity - Anomaly Detection")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "outputs/battery_anomalies.png",
    dpi=300
)

plt.show()

# 8. Save results
df.to_csv(
    "outputs/battery_anomaly_results.csv",
    index=False
)

print("\nAnomaly analysis completed!")
