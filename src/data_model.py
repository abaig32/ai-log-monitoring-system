from sklearn.ensemble import IsolationForest
import joblib
import pandas as pd

def build_isolation_forest(contamination=0.1, n_estimators=100, random_state=42):
    
    isf = IsolationForest(contamination=contamination, 
                          n_estimators=n_estimators, 
                          random_state=random_state)

    return isf

def train_model(model, data):
    model.fit(data)

    return model

def save_model(model, filepath):
    joblib.dump(model, filepath)

def load_model(filepath):
    return joblib.load(filepath)


if __name__ == "__main__":
    # Test: build a model
    model = build_isolation_forest()
    print("Model created:", model)