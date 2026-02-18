import win32evtlog
import win32evtlogutil
import csv
import os
from datetime import datetime, timedelta
import configparser

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)
os.makedirs("models", exist_ok=True)

def get_info():
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    return {
        'log_type': config['detection']['log_type'],
        'collection_hours': int(config['detection']['collection_hours'])
    }

def collect_win_logs(days=None):
    config_info = get_info()
    log_type = config_info['log_type']

    if days is not None:
        time = datetime.now() - timedelta(days=days)
        collection_period = f"{days} days"
    else:
        collection_hours = config_info['collection_hours']
        time = datetime.now() - timedelta(hours=collection_hours)
        collection_period = f"{collection_hours} hour(s)"

    hand = win32evtlog.OpenEventLog(None, log_type)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    all_events = []

    while True:
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if not events:
            break
        all_events.extend(events)

    filename = f"data/raw/logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    headers = ['Timestamp', 'Level', 'Source', 'Message']

    level_map = {
        1: "ERROR",
        2: "WARNING",
        3: "INFO",
        4: "INFO",
        5: "INFO"
    }

    events_written = 0

    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for event in all_events:
                if event.TimeGenerated > time:
                    events_written += 1

                    timestamp = event.TimeGenerated.Format()
                    level = level_map.get(event.EventType, "UNKNOWN")
                    message = str(win32evtlogutil.SafeFormatMessage(event, log_type))
                    source = str(event.SourceName)

                    writer.writerow([timestamp, level, source, message])

    except Exception as e:
        print(f"Error collecting logs: {e}")
    
    print(f"Collected {events_written} events from last {collection_period} (scanned {len(all_events)} total)")