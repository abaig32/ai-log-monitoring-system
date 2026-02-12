Folders:

src/ - Contains all your Python source code files (the 8 .py files listed above)
data/ - Stores all log data

data/raw/ - Stores raw, unprocessed logs collected from Windows Event Log (CSV files named by timestamp)
data/processed/ - Stores cleaned and processed logs ready for ML training/detection (CSV files with extracted features)


models/ - Stores trained machine learning models (saved Isolation Forest models as .pkl or .joblib files)
config/ - Contains configuration files (config.ini with all settings)

src/ files:

log_collector.py - Connects to Windows Event Log using pywin32, extracts logs (timestamp, event ID, source, message), saves raw data to data/raw/ as CSV files
log_processor.py - Reads raw CSV logs from data/raw/, cleans and normalizes the data, extracts features needed for ML (e.g., event frequency, error rates, time-based features), saves processed data to data/processed/
data_model.py - Contains the ML model logic - defines how to build the Isolation Forest model, has functions to train the model, returns trained model object
train_model.py - Orchestration script that: loads processed data → calls data_model.py to build and train the model → saves the trained model to models/ folder
anomaly_detector.py - Loads a trained model from models/, takes new processed log data as input, runs inference to detect anomalies, returns which logs are anomalous
run_detection.py - Main detection loop that: calls log_collector → calls log_processor → calls anomaly_detector → if anomalies found, calls alerting
alerting.py - Sends alerts via email and Slack when anomalies are detected, formats alert messages with anomaly details
flaskapi.py - REST API for the application (endpoints to trigger detection, view anomalies, check system status), used for deployment

Other files:

config/config.ini - Configuration settings (log collection frequency, retention policy, alert thresholds, email/Slack credentials, model parameters)
.gitignore - Tells git what files to ignore (venv, data files, model files, secrets)
requirements.txt - Lists all Python dependencies (pywin32, scikit-learn, flask, pandas, etc.)
Dockerfile - Instructions to containerize the application
README.md - Project documentation


# AI Log Monitoring System
**Work in Progress** - Building an anomaly detection system for Windows Event Logs

Currently implementing: Log collection and processing