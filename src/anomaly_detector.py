import pandas as pd 
from data_model import load_model
from utils import get_latest_model, get_latest_processed_file

def detector():
    latest_model_file = get_latest_model()

    if latest_model_file is None:
        print("There are no model files")
        return None
    
    latest_model = load_model(latest_model_file)

    latest_file = get_latest_processed_file()
    
    if latest_file == None:
        print("There are no processed files")
        return None

    df = pd.read_csv(latest_file)

    features = df[["error_count", "warning_count", "total_events", "error_rate"]]

    predictions = latest_model.predict(features)

    df["is_anomaly"] = predictions == -1

    return df