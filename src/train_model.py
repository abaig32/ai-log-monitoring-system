from data_model import build_isolation_forest, train_model, save_model
import pandas as pd 
from datetime import datetime
from anomaly_detector import get_latest_processed_file

def finished_model():
    file = get_latest_processed_file()

    if file is None:
        print("The processed data file cannot be found, try using the log_collector and log_processor")
        return None

    df = pd.read_csv(file)

    features = df[['error_count', 'warning_count', 'total_events', 'error_rate']]

    model = build_isolation_forest()
    trained_model = train_model(model, features)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_model(trained_model, f"models/trained_model_{timestamp}.joblib")

    return trained_model





