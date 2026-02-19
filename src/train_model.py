from data_model import build_isolation_forest, train_model, save_model
import pandas as pd
from datetime import datetime
from utils import get_latest_processed_file


def finished_model():
    """
    Build, train, and save an Isolation Forest model using the latest processed log data.

    Loads the most recent processed CSV, extracts the relevant features,
    trains the model, and saves it to the models directory with a timestamp.

    Returns:
        IsolationForest: Trained model, or None if no processed file is found.
    """
    file = get_latest_processed_file()

    if file is None:
        print("The processed data file cannot be found, try using the log_collector and log_processor")
        return None

    df = pd.read_csv(file)

    # Select the four features the model trains and predicts on
    features = df[['error_count', 'warning_count', 'total_events', 'error_rate']]

    model = build_isolation_forest()
    trained_model = train_model(model, features)

    # Save model with timestamp to preserve history and avoid overwriting
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_model(trained_model, f"models/trained_model_{timestamp}.joblib")

    return trained_model