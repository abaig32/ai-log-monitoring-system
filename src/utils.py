import glob
import os


def get_latest_model():
    """
    Find and return the path to the most recently modified model file.

    Returns:
        str: Path to the latest .joblib model file, or None if no models exist.
    """
    files = glob.glob("models/*.joblib")

    if not files:
        return None

    latest_file = max(files, key=os.path.getmtime)

    return latest_file


def get_latest_processed_file():
    """
    Find and return the path to the most recently modified processed log file.

    Returns:
        str: Path to the latest processed CSV file, or None if none exist.
    """
    files = glob.glob("data/processed/*.csv")

    if not files:
        return None

    latest_file = max(files, key=os.path.getmtime)

    return latest_file


def get_latest_raw_file():
    """
    Find and return the path to the most recently modified raw log file.

    Returns:
        str: Path to the latest raw CSV file, or None if none exist.
    """
    files = glob.glob("data/raw/*.csv")

    if not files:
        return None

    latest_file = max(files, key=os.path.getmtime)

    return latest_file