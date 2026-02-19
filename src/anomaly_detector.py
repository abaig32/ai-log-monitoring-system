import pandas as pd
from data_model import load_model
from utils import get_latest_model, get_latest_processed_file


def detector():
    """
    Load the latest trained model and processed log data, run anomaly detection,
    and return the results as a DataFrame with an added is_anomaly column.

    Returns:
        DataFrame: Processed log data with is_anomaly column (True/False per hour),
                   or None if no model or processed file is found.
    """
    latest_model_file = get_latest_model()

    if latest_model_file is None:
        print("There are no model files")
        return None

    latest_model = load_model(latest_model_file)

    latest_file = get_latest_processed_file()

    if latest_file is None:
        print("There are no processed files")
        return None

    df = pd.read_csv(latest_file)

    # Select the same four features the model was trained on
    features = df[["error_count", "warning_count", "total_events", "error_rate"]]

    # Isolation Forest returns -1 for anomalies and 1 for normal points
    predictions = latest_model.predict(features)
    df["is_anomaly"] = predictions == -1

    return df