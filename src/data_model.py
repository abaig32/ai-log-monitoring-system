from sklearn.ensemble import IsolationForest
import joblib
import pandas as pd 
import configparser

def load_model_config():
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    return {
        'contamination': float(config['detection']['contamination']),
        'n_estimators': int(config['detection']['n_estimators']),
        'random_state': int(config['detection']['random_state'])
    }

model_config = load_model_config()

def build_isolation_forest(contamination=model_config['contamination'], n_estimators=model_config['n_estimators'], random_state=model_config['random_state']):

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
