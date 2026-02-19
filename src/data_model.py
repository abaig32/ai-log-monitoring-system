from sklearn.ensemble import IsolationForest
import joblib
import configparser


def load_model_config():
    """Read Isolation Forest hyperparameters from config file."""
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    return {
        'contamination': float(config['detection']['contamination']),
        'n_estimators': int(config['detection']['n_estimators']),
        'random_state': int(config['detection']['random_state'])
    }


def build_isolation_forest(contamination=None, n_estimators=None, random_state=None):
    """
    Build an Isolation Forest model using provided or config-based parameters.

    Args:
        contamination (float, optional): Expected proportion of anomalies in the data.
        n_estimators (int, optional): Number of trees in the forest.
        random_state (int, optional): Seed for reproducibility.

    Returns:
        IsolationForest: Untrained Isolation Forest model.
    """
    # Fall back to config values if no parameters are provided
    if contamination is None:
        model_config = load_model_config()
        contamination = model_config['contamination']
        n_estimators = model_config['n_estimators']
        random_state = model_config['random_state']

    isf = IsolationForest(contamination=contamination,
                          n_estimators=n_estimators,
                          random_state=random_state)

    return isf


def train_model(model, data):
    """
    Fit the model on the provided training data.

    Args:
        model (IsolationForest): Untrained model.
        data (DataFrame): Feature data to train on.

    Returns:
        IsolationForest: Trained model.
    """
    model.fit(data)
    return model


def save_model(model, filepath):
    """Serialize and save the trained model to disk."""
    joblib.dump(model, filepath)


def load_model(filepath):
    """Load and return a saved model from disk."""
    return joblib.load(filepath)