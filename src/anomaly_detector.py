import pandas as pd 
import glob
import os 
from data_model import load_model

def get_latest_model():
    files = glob.glob("models/*.joblib")

    if not files:
        return None
    
    latest_file = max(files, key=os.path.getmtime)

    return latest_file

def get_latest_processed_file():
    files = glob.glob("data/processed/*.csv")
    
    if not files:
        return None
    
    latest_file = max(files, key=os.path.getmtime)
    
    return latest_file

def detector():
    latest_model_file = get_latest_model()

    if latest_model_file == None:
        return "There are no model files"
    
    latest_model = load_model(latest_model_file)

    latest_file = get_latest_processed_file()
    
    if latest_file == None:
        return "There are no processed files"

    df = pd.read_csv(latest_file)

    features = df[["error_count", "warning_count", "total_events", "error_rate"]]

    predictions = latest_model.predict(features)

    df["is_anomaly"] = predictions == -1

    return df
