import pandas as pd
from datetime import datetime
import csv

def process_logs(filename):
    df = pd.read_csv(filename)

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df['hour_timestamp'] = df["Timestamp"].dt.floor('h')


    df['is_error'] = (df['Level'] == 'ERROR').astype(int)
    df['is_warning'] = (df['Level'] == 'WARNING').astype(int)
    df['is_info'] = (df['Level'] == 'INFO').astype(int)

    print(df['Level'].value_counts())

    aggregated = df.groupby('hour_timestamp').agg({
        'Timestamp': 'count', 
        'is_error': 'sum',
        'is_warning': 'sum',
        'is_info': 'sum',
        'Source': 'nunique'
    })

    aggregated["error_rate"] = aggregated['is_error'] / aggregated['Timestamp']

    aggregated = aggregated.rename(columns={
        'Timestamp': 'total_events',
        'is_error': 'error_count',
        'is_warning': 'warning_count',
        'is_info': 'info_count',
        'Source': 'unique_sources'
    })

    output_file_name = f"data/processed/processed_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    aggregated.to_csv(output_file_name)


if __name__ == "__main__":
    process_logs("data/raw/logs_20260212_183757.csv")
    print("Log processing complete! Check data/processed/ folder")



    



