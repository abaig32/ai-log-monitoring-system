import glob
import os 

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

def get_latest_raw_file():
    files = glob.glob("data/raw/*.csv")
    
    if not files:
        return None
    
    latest_file = max(files, key=os.path.getmtime)
    
    return latest_file