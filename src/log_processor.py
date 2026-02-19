import pandas as pd
from datetime import datetime


def process_logs(filename):
    """
    Process a raw log CSV into hourly aggregated features and save to a new CSV.

    Reads raw log events, groups them by hour, and computes per-hour metrics
    (event counts, error/warning/info counts, error rate) used for model
    training and anomaly detection.

    Args:
        filename (str): Path to the raw log CSV file to process.

    Returns:
        str: Path to the saved processed CSV file.
    """
    df = pd.read_csv(filename)

    # Parse timestamps and floor to the nearest hour for grouping
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df['hour_timestamp'] = df["Timestamp"].dt.floor('h')

    # Create binary indicator columns for each severity level
    df['is_error'] = (df['Level'] == 'ERROR').astype(int)
    df['is_warning'] = (df['Level'] == 'WARNING').astype(int)
    df['is_info'] = (df['Level'] == 'INFO').astype(int)

    # Aggregate events by hour — count events and sum severity indicators
    aggregated = df.groupby('hour_timestamp').agg({
        'Timestamp': 'count',
        'is_error': 'sum',
        'is_warning': 'sum',
        'is_info': 'sum',
        'Source': 'nunique'
    })

    # Calculate error rate as proportion of total events
    aggregated["error_rate"] = aggregated['is_error'] / aggregated['Timestamp']

    # Rename columns to cleaner feature names
    aggregated = aggregated.rename(columns={
        'Timestamp': 'total_events',
        'is_error': 'error_count',
        'is_warning': 'warning_count',
        'is_info': 'info_count',
        'Source': 'unique_sources'
    })

    output_file_name = f"data/processed/processed_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    # Reset index so hour_timestamp is saved as a column, not the index
    aggregated = aggregated.reset_index()
    aggregated.to_csv(output_file_name, index=False)

    return output_file_name