import pandas as pd
import configparser

from log_collector import collect_win_logs
from log_processor import process_logs
from anomaly_detector import detector
from alerting import send_email_alert, send_slack_alert
from utils import get_latest_raw_file, cleanup_old_files, cleanup_old_models


def get_alert_config():
    """Read alert notification settings from config file."""
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    return {
        'enable_email': config.getboolean('alerts', 'enable_email_notifications'),
        'enable_slack': config.getboolean('alerts', 'enable_slack_notifications')
    }


def main():
    """
    Run a full detection cycle: collect logs, process them, detect anomalies,
    and send alerts if any anomalies are found.
    """
    print("\n" + "="*50)
    print("AI LOG MONITORING SYSTEM - ANOMALY DETECTION")
    print("="*50 + "\n")

    # Step 1: Collect logs from Windows Event Log
    print("[1/5] Collecting Windows Logs...")
    try:
        collect_win_logs()
    except Exception as e:
        print(f"ERROR: Logs could not be collected: {e}\n")
        return

    latest_raw = get_latest_raw_file()
    if latest_raw is None:
        print("WARNING: No raw log files found.\n")
        return

    # Check if the raw file is empty
    import pandas as pd
    if pd.read_csv(latest_raw).empty:
        print("WARNING: No events collected in this time window. Try again later or increase collection_hours in config.ini.\n")
        return

    # Step 2: Get the raw file just written by the collector
    print("\n[2/5] Fetching latest raw data file...")
    try:
        latest_raw = get_latest_raw_file()
    except Exception as e:
        print(f"ERROR: Latest raw data file couldn't be fetched: {e}\n")
        return

    # Step 3: Aggregate raw events into hourly feature data
    print("\n[3/5] Processing logs...")
    try:
        process_logs(latest_raw)
    except Exception as e:
        print(f"ERROR: Logs could not be processed: {e}\n")
        return

    # Step 4: Run Isolation Forest on the processed hourly features
    print("\n[4/5] Running anomaly detection...")
    try:
        anomaly_data = detector()
        num_anomalies = anomaly_data['is_anomaly'].sum()
        print(f"Found {num_anomalies} anomalies in {len(anomaly_data)} hour(s)")

        if num_anomalies == 0:
            print("There are no anomalies to report!")
    except Exception as e:
        print(f"ERROR: Anomalies couldn't be detected: {e}\n")
        return

    # Step 5: Send alerts via enabled channels if anomalies were found
    print("\n[5/5] Sending alerts...")
    try:
        alert_config = get_alert_config()

        if num_anomalies > 0:
            if alert_config['enable_email']:
                send_email_alert(anomaly_data)
                print("Email alert sent successfully")

            if alert_config['enable_slack']:
                send_slack_alert(anomaly_data)
                print("Slack alert sent successfully")

            if not alert_config['enable_email'] and not alert_config['enable_slack']:
                print("WARNING: Anomalies detected but no alerts enabled")
        else:
            print("No anomalies detected - no alerts sent")

    except Exception as e:
        print(f"ERROR: Alerts couldn't be sent: {e}\n")
        return

    # Delete Excessive Log and Model Files
    cleanup_old_files("data/raw")
    cleanup_old_files("data/processed")
    cleanup_old_models()

    print("\n" + "="*50)
    print("Detection Cycle Complete!")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()