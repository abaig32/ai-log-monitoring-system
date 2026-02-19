from log_processor import process_logs
from log_collector import collect_win_logs
from anomaly_detector import detector
from alerting import send_email_alert, send_slack_alert
from utils import get_latest_raw_file
import os
import configparser

def get_alert_config():
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    return {
        'enable_email': config.getboolean('alerts','enable_email_notifications'),
        'enable_slack': config.getboolean('alerts','enable_slack_notifications')
    }

def main():
    print("\n" + "="*50)
    print("AI LOG MONITORING SYSTEM - ANOMALY DETECTION")
    print("="*50 + "\n")
    
    # Collect logs
    print("[1/5] Collecting Windows Logs...")
    try:
        collect_win_logs()
        print("[DEBUG] Log collection done")
    except Exception as e:
        print(f"ERROR: Logs could not be collected: {e}\n")
        return

    # Get latest raw file
    print("\n[2/5] Fetching latest raw data file...")
    try:
        latest_raw = get_latest_raw_file()
    except Exception as e:
        print(f"ERROR: Latest raw data file couldn't be fetched: {e}\n")
        return
    
    # Process logs
    print("\n[3/5] Processing logs...")
    try:
        process_logs(latest_raw)
        import pandas as pd
        df_check = pd.read_csv("data/processed/" + sorted(os.listdir("data/processed"))[-1])
    except Exception as e:
        print(f"ERROR: Logs could not be processed: {e}\n")
        return

    # Detect anomalies
    print("\n[4/5] Running anomaly detection...")
    try:
        anomaly_data = detector()
        num_anomalies = anomaly_data['is_anomaly'].sum()
        print(f"Found {num_anomalies} anomalies in {len(anomaly_data)} hour(s)")

        if num_anomalies == 0:
            print("There are no amomalies to report!")
    except Exception as e:
        print(f"ERROR: Anomalies couldn't be detected: {e}\n")
        return

    # Send alerts
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
    
    print("\n" + "="*50)
    print("Detection Cycle Complete!")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()