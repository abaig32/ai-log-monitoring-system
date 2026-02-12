import win32evtlog
import win32evtlogutil
import csv
import os
from datetime import datetime,timedelta

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)
os.makedirs("models", exist_ok=True)

def collect_win_logs(log_type):
    time = datetime.now() - timedelta(hours=1)
    hand = win32evtlog.OpenEventLog(None, log_type)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    events = win32evtlog.ReadEventLog(hand,flags,0)

    filename = f"data/raw/logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    headers = ['Timestamp', 'Level', 'Source', 'Message']

    level_map = {
    1: "ERROR",
    2: "WARNING",
    3: "INFO",
    4: "INFO",
    5: "INFO"
    }

    try:
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for event in events:
                if event.TimeGenerated > time:

                    timestamp = event.TimeGenerated.Format()
                    level = level_map.get(event.EventType, "UNKNOWN")
                    message = str(win32evtlogutil.SafeFormatMessage(event, log_type))
                    source = str(event.SourceName)

                    writer.writerow([timestamp, level, source, message])

    except Exception as e:
        print(f"Error collecting logs: {e}")


if __name__ == "__main__":
    collect_win_logs('System')
    print("Log collection complete! Check data/raw/ folder")

    

    

    
