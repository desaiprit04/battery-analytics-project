
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# 1. Load battery data
df = pd.read_csv("outputs/battery_health_analysis.csv")

# 2. Select features
features = [
    "capacity_Ah",
    "max_temperature_C",
    "duration_s",
    "mean_voltage_V"
]

# 3. Calculate local rolling-median baseline
# Window of 11 cycles, centred on each observation

residual_columns = []

for feature in features:

    baseline = (
        df[feature]
        .rolling(window=11, center=True, min_periods=5)
        .median()
    )

    residual_name = feature + "_residual"

    df[residual_name] = df[feature] - baseline

    residual_columns.append(residual_name)

# 4. Prepare residual features
X = df[residual_columns].copy()

# 5. Standardise residuals
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 6. Train Isolation Forest
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

df["anomaly_label_v2"] = model.fit_predict(X_scaled)

# 7. Identify unusual cycles
anomalies = df[df["anomaly_label_v2"] == -1]

print("\nTREND-ADJUSTED ANOMALY DETECTION")
print("--------------------------------")

print("Total cycles:", len(df))
print("Detected unusual cycles:", len(anomalies))

print("\nUnusual cycle details:")

print(
    anomalies[
        [
            "discharge_cycle",
            "capacity_Ah",
            "capacity_Ah_residual",
            "max_temperature_C",
            "max_temperature_C_residual",
            "duration_s_residual"
        ]
    ].to_string(index=False)
)

# 8. Plot capacity residuals
plt.figure(figsize=(11, 5))

plt.scatter(
    df["discharge_cycle"],
    df["capacity_Ah_residual"],
    label="Other cycles"
)

plt.scatter(
    anomalies["discharge_cycle"],
    anomalies["capacity_Ah_residual"],
    marker="x",
    s=90,
    label="Flagged unusual cycles"
)

plt.axhline(0, linestyle="--")

plt.xlabel("Discharge cycle")
plt.ylabel("Capacity deviation from local median (Ah)")
plt.title("Battery Capacity - Trend-Adjusted Anomaly Detection")

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    "outputs/battery_anomalies_v2.png",
    dpi=300
)

plt.show()

# 9. Save results
df.to_csv(
    "outputs/battery_anomaly_results_v2.csv",
    index=False
)

print("\nImproved anomaly analysis completed!")
