# Battery Analytics and Anomaly Detection

A Python-based exploratory battery analytics project using the NASA B0005 lithium-ion battery cycling dataset. The project examines discharge-cycle behaviour, capacity degradation, relative State of Health (SoH), and statistically unusual cycles.

> \\\\\\\\\\\\\\\*\\\\\\\\\\\\\\\*Project scope:\\\\\\\\\\\\\\\*\\\\\\\\\\\\\\\* This is an educational, exploratory analysis of a single-cell cycling dataset. It is not a validated battery fault-detection system and does not represent grid-scale battery energy storage system (BESS) operational data.

## Project objectives

* Extract and organise discharge-cycle measurements.
* Examine capacity change across discharge cycles.
* Calculate relative capacity retention as an indicative SoH measure.
* Visualise voltage, current, and temperature during discharge.
* Explore unusual cycle behaviour with Isolation Forest.
* Investigate selected flagged cycles using their underlying measurements.
* Document assumptions and limitations of statistical anomaly detection.

## Dataset

The analysis uses the NASA B0005 battery dataset (`B0005.mat`).

Place the dataset file in the `data/` directory:

```text
data/B0005.mat
```

The dataset contains charge and discharge operations. This project extracts the discharge operations for cycle-level analysis.

**Dataset attribution:** NASA Ames Prognostics Center of Excellence (PCoE), battery aging dataset. Please consult the original NASA dataset page and its terms before redistributing the raw data. This repository should contain the analysis code and documentation; do not upload the raw `.mat` file unless redistribution is permitted.



Download the dataset:

NASA Battery Data Set (ZIP)
Link: https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip

NASA PCoE Data Set Repository
Link: https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/





Setup Instructions



Download the Battery Data Set ZIP archive using the link above.



Extract the downloaded archive and locate B0005.mat in the extracted files.



Copy B0005.mat into this project's data/ directory.



Make sure the file structure looks like this:



battery-analytics-project/

├── data/

│   └── B0005.mat

├── outputs/

├── README.md

└── requirements.txt



Note: The original dataset is not included in this GitHub repository. The .mat file is excluded through .gitignore and must be downloaded separately.



Dataset citation:



Saha, B. and Goebel, K. (2007). Battery Data Set. NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, CA.





## Analyses performed

### 1\. Discharge-cycle extraction

The extraction workflow reads the MATLAB `.mat` structure and creates a cycle-level CSV summary. The extracted dataset contains 168 discharge cycles and features such as:

* Discharge capacity (Ah)
* Mean, minimum, and maximum measured voltage (V)
* Mean measured current (A)
* Mean and maximum measured temperature (°C)
* Discharge duration (s)
* Number of measurement points
* Ambient temperature (°C)

Output:

```text
outputs/discharge\\\\\\\\\\\\\\\_cycle\\\\\\\\\\\\\\\_summary.csv
```

### 2\. Capacity degradation and relative SoH

Capacity is plotted across discharge cycles. Relative SoH is calculated using the first recorded discharge capacity as the reference:

```python
SoH\\\\\\\\\\\\\\\_percent = capacity\\\\\\\\\\\\\\\_Ah / first\\\\\\\\\\\\\\\_discharge\\\\\\\\\\\\\\\_capacity\\\\\\\\\\\\\\\_Ah \\\\\\\\\\\\\\\* 100
```

This is **relative capacity retention**, not a manufacturer-rated SoH value or a complete battery health diagnosis.

Expected outputs:

```text
outputs/capacity\\\\\\\\\\\\\\\_degradation.png
outputs/battery\\\\\\\\\\\\\\\_soh.png
outputs/battery\\\\\\\\\\\\\\\_health\\\\\\\\\\\\\\\_analysis.csv
```

### 3\. Voltage, current, and temperature profiles

The project visualises measured voltage, current, and temperature against elapsed discharge time for an example discharge cycle.

Expected output:

```text
outputs/voltage\\\\\\\\\\\\\\\_current\\\\\\\\\\\\\\\_temperature.png
```

The sign of measured current follows the dataset's convention; negative current values are observed during discharge.

### 4\. Initial anomaly detection

An Isolation Forest model is applied to cycle-level operating features, including capacity, voltage, current, temperature, and duration. The model uses a contamination setting of 0.05.

Expected output:

```text
outputs/battery\\\\\\\\\\\\\\\_anomalies.png
```

The contamination value is a modelling assumption. It is not a measured fault rate.

### 5\. Trend-adjusted anomaly detection

A second approach calculates deviations from rolling-median trends before applying Isolation Forest. This helps explore unusual behaviour relative to nearby cycles rather than relying only on raw feature values.

Expected outputs:

```text
outputs/battery\\\\\\\\\\\\\\\_anomalies\\\\\\\\\\\\\\\_v2.png
outputs/battery\\\\\\\\\\\\\\\_anomaly\\\\\\\\\\\\\\\_results\\\\\\\\\\\\\\\_v2.csv
```

### 6\. Investigation of selected cycles

Selected neighbouring cycles (including cycles 47, 48, and 49) are compared using their cycle summaries and raw measurement profiles. The verification workflow checks the exact timestamps of maximum temperature and minimum voltage.

This investigation found that cycle 48 had a higher maximum measured temperature and lower minimum voltage than the adjacent cycles. These differences make it worth investigating, but they do **not** establish that the battery had a fault.



## Repository structure



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

## Requirements

* Python 3.10 or later is recommended.
* NumPy
* Pandas
* SciPy
* Matplotlib
* scikit-learn

Install dependencies from the project root:

```bash
python -m pip install -r requirements.txt
```

If you do not yet have a `requirements.txt`, create one containing:

```text
numpy
pandas
scipy
matplotlib
scikit-learn
```

## Running the project on Windows

Open a terminal in the project root. If you use the project's virtual environment in Windows Command Prompt:

```cmd
.venv\\\\\\\\\\\\\\\\Scripts\\\\\\\\\\\\\\\\python.exe extract\\\\\\\\\\\\\\\_battery\\\\\\\\\\\\\\\_data.py
.venv\\\\\\\\\\\\\\\\Scripts\\\\\\\\\\\\\\\\python.exe capacity\\\\\\\\\\\\\\\_degradation.py
.venv\\\\\\\\\\\\\\\\Scripts\\\\\\\\\\\\\\\\python.exe voltage\\\\\\\\\\\\\\\_temperature\\\\\\\\\\\\\\\_analysis.py
.venv\\\\\\\\\\\\\\\\Scripts\\\\\\\\\\\\\\\\python.exe battery\\\\\\\\\\\\\\\_anomaly\\\\\\\\\\\\\\\_detection.py
.venv\\\\\\\\\\\\\\\\Scripts\\\\\\\\\\\\\\\\python.exe battery\\\\\\\\\\\\\\\_anomaly\\\\\\\\\\\\\\\_detection\\\\\\\\\\\\\\\_v2.py
```

Run the optional cycle-investigation scripts if they are present:

```cmd
.venv\\\\\\\\\\\\\\\\Scripts\\\\\\\\\\\\\\\\python.exe investigate\\\\\\\\\\\\\\\_cycles.py
.venv\\\\\\\\\\\\\\\\Scripts\\\\\\\\\\\\\\\\python.exe compare\\\\\\\\\\\\\\\_discharge\\\\\\\\\\\\\\\_profiles.py
.venv\\\\\\\\\\\\\\\\Scripts\\\\\\\\\\\\\\\\python.exe verify\\\\\\\\\\\\\\\_cycles.py
```

Run commands from the repository root so that relative paths such as `data/B0005.mat` and `outputs/` resolve correctly.

## Key findings and interpretation

* The extraction workflow produced 168 discharge-cycle summaries.
* Capacity decreases over the analysed sequence, with local variations between cycles.
* Relative SoH is referenced to the first recorded discharge capacity.
* Isolation Forest identifies statistically unusual cycles according to the selected features and contamination assumption.
* Trend-adjusted analysis changes which cycles are flagged because it evaluates deviations from local rolling trends.
* Cycle 48 showed a higher maximum temperature (40.712 °C) and lower minimum voltage (2.605 V) than cycles 47 and 49 in the investigated measurements.

These are observations from this dataset and analysis configuration, not proof of a physical fault, degradation mechanism, or unsafe condition.

## Limitations

* The analysis uses the NASA B0005 cell-cycling dataset, not grid-scale BESS field-operation data.
* Relative SoH is based on the first recorded discharge capacity, not a verified manufacturer-rated capacity.
* Isolation Forest is an unsupervised model; there are no confirmed fault labels in this workflow.
* The contamination parameter affects how many observations are flagged.
* Rolling-median residuals depend on the chosen window and can be less reliable near the beginning and end of the sequence.
* Statistical anomalies require engineering investigation and validation before they can be interpreted as faults.
* The project is exploratory and has not been validated for production or safety-critical use.

## Future improvements

* Add automated tests and data-quality checks.
* Compare anomaly results across several contamination settings and rolling-window sizes.
* Evaluate additional features and alternative anomaly-detection methods.
* Add a reproducible summary report and clearer plot annotations.
* Extend the analysis to appropriately licensed, real-world BESS operational datasets.

## Author

**\[Your Name]**  
M.Sc. Information and Electrical Engineering student, Hochschule Wismar

This project was developed as a self-directed learning project to build practical skills in Python-based battery data analysis.

