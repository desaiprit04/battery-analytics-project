# Battery Analytics and Anomaly Detection

A Python-based exploratory battery analytics project using the NASA B0005 lithium-ion battery cycling dataset. The project examines discharge-cycle behaviour, capacity degradation, relative State of Health (SoH), and statistically unusual cycles.

**Project scope:** This is an educational, exploratory analysis of a single-cell cycling dataset. It is not a validated battery fault-detection system and does not represent grid-scale battery energy storage system (BESS) operational data.

## Project Objectives

- Extract and organise discharge-cycle measurements.
- Examine capacity changes across discharge cycles.
- Calculate relative capacity retention as an indicative SoH measure.
- Visualise voltage, current, and temperature during discharge.
- Explore unusual cycle behaviour using Isolation Forest.
- Investigate selected flagged cycles using their underlying measurements.
- Document assumptions and limitations of statistical anomaly detection.

## Dataset

This project uses the NASA B0005 lithium-ion battery dataset (`B0005.mat`).

The dataset contains charge and discharge operations. This project extracts the discharge operations for cycle-level analysis.

### Dataset Download

The original dataset can be downloaded from the following sources:

- [NASA Battery Data Set (ZIP)](https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip)
- [NASA Prognostics Center of Excellence (PCoE) Data Repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/)

### Setup Instructions

1. Download the NASA Battery Data Set ZIP archive.
2. Extract the downloaded archive.
3. Locate the file named `B0005.mat`.
4. Copy `B0005.mat` into the `data/` directory of this project.

The expected location is:

```text
data/B0005.mat
```

**Note:** The original dataset is not included in this GitHub repository. The `.mat` file is excluded through `.gitignore` and must be downloaded separately. Please consult the original NASA dataset terms before redistributing the raw data.

### Dataset Citation

Saha, B. and Goebel, K. (2007). *Battery Data Set*. NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, CA.

## Analyses Performed

### 1. Discharge-Cycle Extraction

The extraction workflow reads the MATLAB `.mat` structure and creates a cycle-level CSV summary.

The extracted dataset contains **168 discharge cycles** with features such as:

- Discharge capacity (Ah)
- Mean, minimum, and maximum measured voltage (V)
- Mean measured current (A)
- Mean and maximum measured temperature (°C)
- Discharge duration (s)
- Number of measurement points
- Ambient temperature (°C)

**Output:**

`outputs/discharge_cycle_summary.csv`

### 2. Capacity Degradation and Relative SoH

Capacity is analysed across discharge cycles. Relative SoH is calculated using the first recorded discharge capacity as the reference:

```python
SoH_percent = (capacity_Ah / first_discharge_capacity_Ah) * 100
```

This represents **relative capacity retention**, not a manufacturer-rated SoH value or a complete battery health diagnosis.

**Key results:**

- Initial discharge capacity: approximately 1.8565 Ah
- Final discharge capacity: approximately 1.3251 Ah
- Final relative capacity retention: approximately 71.38%
- Capacity degradation relative to the first recorded cycle: approximately 28.62%
- First cycle below 80% relative capacity retention: Cycle 101

**Outputs:**

- `outputs/capacity_degradation.png`
- `outputs/battery_soh.png`
- `outputs/battery_health_analysis.csv`

### 3. Voltage, Current, and Temperature Profiles

The project visualises measured voltage, current, and temperature against elapsed discharge time for an example discharge cycle.

The analysis helps examine the relationship between electrical behaviour, temperature changes, and discharge progression.

Negative current values are observed during discharge, following the dataset's measurement convention.

**Output:**

`outputs/voltage_current_temperature.png`

### 4. Initial Anomaly Detection

An Isolation Forest model is applied to cycle-level operating features, including:

- Capacity
- Mean voltage
- Mean current
- Mean temperature
- Maximum temperature
- Discharge duration

The model uses a contamination setting of 0.05.

The initial model identified 9 statistically unusual cycles out of 168 discharge cycles.

**Output:**

- `outputs/battery_anomalies.png`
- `outputs/battery_anomaly_results.csv`

The contamination value is a modelling assumption, not a measured fault rate.

### 5. Trend-Adjusted Anomaly Detection

A second approach calculates deviations from rolling-median trends before applying Isolation Forest.

This helps explore unusual behaviour relative to nearby cycles rather than relying only on raw feature values.

The trend-adjusted approach also identified 9 statistically unusual cycles, although the flagged cycles differed from those identified by the initial model.

**Outputs:**

- `outputs/battery_anomalies_v2.png`
- `outputs/battery_anomaly_results_v2.csv`

### 6. Investigation of Selected Cycles

Selected neighbouring cycles, including Cycles 47, 48, and 49, are compared using their cycle summaries and raw measurement profiles.

The investigation checks the timing of maximum temperature and minimum voltage.

Cycle 48 showed:

- Maximum measured temperature: approximately 40.712 °C
- Minimum measured voltage: approximately 2.605 V

Compared with the adjacent cycles, Cycle 48 had a higher maximum temperature and a lower minimum voltage.

These differences make the cycle worth investigating, but they do **not** establish that the battery experienced a fault.

**Output:**

`outputs/cycle_47_48_49_comparison.png`

## Key Findings and Interpretation

- The extraction workflow produced 168 discharge-cycle summaries.
- Capacity decreased over the analysed sequence, with local variations between cycles.
- Final relative capacity retention was approximately 71.38% compared with the first recorded discharge capacity.
- Isolation Forest identified statistically unusual cycles according to the selected features and contamination assumption.
- Trend-adjusted analysis changed which cycles were flagged because it evaluated deviations from local rolling trends.
- Cycle 48 showed a higher maximum temperature and lower minimum voltage than Cycles 47 and 49 in the investigated measurements.

These observations are specific to this dataset and analysis configuration. They are not proof of a physical fault, degradation mechanism, or unsafe condition.

## Repository Structure

```text
battery-analytics-project/
|
|-- data/
|   |-- B0005.mat (download separately; not included in Git)
|
|-- outputs/
|   |-- battery_anomalies.png
|   |-- battery_anomalies_v2.png
|   |-- battery_anomaly_results.csv
|   |-- battery_anomaly_results_v2.csv
|   |-- battery_health_analysis.csv
|   |-- battery_soh.png
|   |-- capacity_degradation.png
|   |-- cycle_47_48_49_comparison.png
|   |-- discharge_cycle_summary.csv
|   |-- voltage_current_temperature.png
|
|-- notebooks/
|
|-- battery_anomaly_detection.py
|-- battery_anomaly_detection_v2.py
|-- capacity_degradation.py
|-- compare_discharge_profiles.py
|-- explore_battery.py
|-- extract_battery_data.py
|-- inspect_battery.py
|-- inspect_cycles.py
|-- inspect_discharge.py
|-- investigate_cycles.py
|-- verify_cycles.py
|-- voltage_temperature_analysis.py
|
|-- requirements.txt
|-- README.md
|-- .gitignore
```

**Note:** The `data/` directory and `B0005.mat` file are not tracked in Git. Download the dataset separately as described above.

## Requirements

- Python 3.10 or later
- NumPy
- Pandas
- SciPy
- Matplotlib
- scikit-learn

Install the required dependencies using:

```cmd
python -m pip install -r requirements.txt
```

## Running the Project on Windows

Open a terminal in the project root directory.

If you have not created a virtual environment yet, you can create one using:

```cmd
py -m venv .venv
```

Activate the environment:

```cmd
.venv\Scripts\activate
```

Install the dependencies:

```cmd
python -m pip install -r requirements.txt
```

Run the main analysis scripts in the following order:

```cmd
python extract_battery_data.py
python capacity_degradation.py
python voltage_temperature_analysis.py
python battery_anomaly_detection.py
python battery_anomaly_detection_v2.py
python compare_discharge_profiles.py
```

Optional investigation scripts:

```cmd
python investigate_cycles.py
python verify_cycles.py
```

Run commands from the repository root so that relative paths such as `data/B0005.mat` and `outputs/` resolve correctly.

## Limitations

- The analysis uses the NASA B0005 cell-cycling dataset, not grid-scale BESS field-operation data.
- Relative SoH is based on the first recorded discharge capacity, not a verified manufacturer-rated capacity.
- Isolation Forest is an unsupervised model; there are no confirmed fault labels in this workflow.
- The contamination parameter affects how many observations are flagged.
- Rolling-median residuals depend on the chosen window and can be less reliable near the beginning and end of the sequence.
- Statistical anomalies require engineering investigation and validation before they can be interpreted as faults.
- The project is exploratory and has not been validated for production or safety-critical use.

## Future Improvements

- Add automated tests and data-quality checks.
- Compare anomaly results across several contamination settings and rolling-window sizes.
- Evaluate additional features and alternative anomaly-detection methods.
- Add a reproducible summary report and clearer plot annotations.
- Extend the analysis to appropriately licensed, real-world BESS operational datasets.

## Author

**[Prit Desai]**  
M.Sc. Information and Electrical Engineering student, Hochschule Wismar

This project was developed as a self-directed learning project to build practical skills in Python-based battery data analysis.
