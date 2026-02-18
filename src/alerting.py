import smtplib
from email.mime.text import MIMEText
from anomaly_detector import detector
import configparser

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

    try:
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    anomalies = detector()
    if anomalies is not None:
        send_email_alert(anomalies)