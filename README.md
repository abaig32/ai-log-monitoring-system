# AI Log Monitoring System

An automated tool that monitors your Windows Event Logs, learns what normal activity looks like, and alerts you when something unusual is detected.

---

## How It Works

The system collects logs from your Windows machine, processes them into hourly summaries, and uses a machine learning model to detect unusual patterns. If anything suspicious is found, it can send you an alert via email or Slack.

---

## Project Structure

```
AI Log Monitoring System/
│
├── src/
│   ├── log_collector.py      # Collects logs from Windows Event Log
│   ├── log_processor.py      # Processes raw logs into hourly summaries
│   ├── data_model.py         # Builds and manages the AI model
│   ├── train_model.py        # Trains the model on collected log data
│   ├── anomaly_detector.py   # Runs anomaly detection
│   ├── alerting.py           # Sends email and Slack alerts
│   ├── run_detection.py      # Runs a full detection cycle
│   ├── setup.py              # Initial setup and model training
│   ├── flaskapi.py           # Flask API for remote access
│   └── utils.py              # Shared utility functions
│
├── config/
│   └── config.ini            # All settings (log type, alerts, email, Slack)
│
├── data/
│   ├── raw/                  # Raw collected log files
│   └── processed/            # Processed hourly log summaries
│
├── models/                   # Saved trained models
├── requirements.txt          # Python dependencies
└── Dockerfile                # Docker configuration for the Flask API
```

---

## Requirements

- Windows 10 or later
- Python 3.11 or later
- An internet connection (for email/Slack alerts)

---

## Installation

**1. Clone the repository:**
```
git clone https://github.com/yourusername/ai-log-monitoring-system.git
```

**2. Navigate into the project folder:**
```
cd ai-log-monitoring-system
```

**3. Create and activate a virtual environment:**
```
python -m venv .venv
.venv\Scripts\activate
```

**4. Install dependencies:**
```
pip install -r requirements.txt
```

---

## Configuration

All settings are stored in `config/config.ini`. Open this file and fill in your details before running the system.

```ini
[detection]
log_type = System              ; Windows log to monitor (System, Application, Security)
collection_hours = 1           ; How many hours of logs to collect per detection run
contamination = 0.05           ; Expected proportion of anomalies (0.05 = 5%)
n_estimators = 100             ; Number of trees in the model
random_state = 42              ; Seed for reproducibility

[alerts]
enable_email_notifications = true
enable_slack_notifications = false

[email]
smtp_server = smtp.gmail.com
smtp_port = 587
sender_email = you@gmail.com
password = your_app_password
receiver_email = recipient@gmail.com

[slack]
webhook_url = https://hooks.slack.com/services/your/webhook/url
```

> **Note:** For Gmail, you will need to generate an App Password rather than using your regular password. You can do this in your Google Account under Security → 2-Step Verification → App Passwords.

---

## Usage

### Step 1 — Initial Setup (run once)

This collects 7 days of logs and trains the model on your normal activity patterns.

```
python src/setup.py
```

This will take a few minutes. Once complete you will see:
```
Setup complete! Model trained successfully.
```

### Step 2 — Run Detection

This collects the latest logs, runs the model, and sends alerts if anomalies are found.

```
python src/run_detection.py
```

You can run this manually whenever you want, or schedule it using Windows Task Scheduler to run automatically.

---

### Step 3 — Schedule Automatic Detection (Recommended)

To have the system run automatically every hour using Windows Task Scheduler:

1. Open **Task Scheduler** (search for it in the Start menu)
2. Click **Create Basic Task** in the right panel
3. Give it a name e.g. `AI Log Monitor` and click Next
4. Set the trigger to **Daily**, click Next
5. Set the start time, click Next
6. Select **Repeat task every 1 hour** for a duration of **Indefinitely**
7. Select **Start a Program** and click Next
8. In the **Program/Script** field, enter the path to your Python executable e.g:
```
    C:\Users\YourName\Desktop\AI Log Monitoring System\.venv\Scripts\python.exe
```
9. In the **Add arguments** field, enter:
```
    src/run_detection.py
```
10. In the **Start in** field, enter the path to your project folder e.g:
```
    C:\Users\YourName\Desktop\AI Log Monitoring System
```
11. Click **Finish**

The system will now automatically collect logs and check for anomalies every hour, sending alerts whenever something unusual is detected.

## API Endpoints

The system also includes a Flask API for remote access. Start it with:

```
python src/flaskapi.py
```

The API will be available at `http://localhost:5000`.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/status` | GET | Check if a trained model exists |
| `/setup` | POST | Run initial setup and train the model |
| `/detect` | POST | Run a detection cycle and return results |

**Example response from `/detect`:**
```json
[
    {
        "hour_timestamp": "2026-02-18 17:00:00",
        "total_events": 4,
        "error_count": 0,
        "warning_count": 0,
        "info_count": 4,
        "error_rate": 0.0,
        "is_anomaly": false
    }
]
```

---

## Troubleshooting

**"There are no model files"** — You need to run `setup.py` before running detection.

**"Collected 0 events"** — Check that `log_type` in `config.ini` matches a valid Windows log name (System, Application, or Security).

**Email alerts not sending** — Make sure you are using a Gmail App Password, not your regular password. Also check that `enable_email_notifications = true` in config.

**Slack alerts not sending** — Double check your webhook URL is correct and that `enable_slack_notifications = true` in config.
