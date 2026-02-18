import smtplib
from email.mime.text import MIMEText
from anomaly_detector import detector
import configparser
import requests

def format_anomaly_report(anomaly_df):
    anomalies = anomaly_df[anomaly_df['is_anomaly'] == True]
    
    if len(anomalies) == 0:
        return "No anomalies detected."
    
    report = f"Found {len(anomalies)} anomalies out of {len(anomaly_df)} hours:\n\n"
    
    for idx, row in anomalies.iterrows():
        report += f"Time: {row['hour_timestamp']}\n"
        report += f"  Total Events: {row['total_events']}\n"
        report += f"  Errors: {row['error_count']}\n"
        report += f"  Warnings: {row['warning_count']}\n"
        report += f"  Error Rate: {row['error_rate']:.2%}\n\n"
    
    return report


def load_email_config():
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    
    return {
        'smtp_server': config['email']['smtp_server'],
        'smtp_port': int(config['email']['smtp_port']),
        'sender_email': config['email']['sender_email'],
        'password': config['email']['password'],
        'receiver_email': config['email']['receiver_email']
    }


def send_email_alert(anomaly_data):
   try:
        email_config = load_email_config()
        sender_email = email_config['sender_email']
        receiver_email = email_config['receiver_email']
        password = email_config['password']
        subject = "Anomaly Detection Alert!"
        body = format_anomaly_report(anomaly_data)

        msg = MIMEText(body)
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        print("Email has been successfully sent!")
   except Exception as e:
       print(f"Email can't be sent because {e}")

def load_slack_config():
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    return {'webhook_url': config['slack']['webhook_url']}
    

def send_slack_alert(anomaly_data):
    try:
        slack_config = load_slack_config()

        webhook_url = slack_config['webhook_url']
        message = format_anomaly_report(anomaly_data)

        payload = {"text": message}
        response = requests.post(webhook_url, json=payload)

        if response.status_code != 200:
            raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
        else:
            print("Slack alert sent successfully!")
    except Exception as e:
        print(f"Failed to send Slack alert: {e}")