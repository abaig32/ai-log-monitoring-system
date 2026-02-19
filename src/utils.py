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


def cleanup_old_files(folder, keep=10):
    """
    Delete old CSV files in a folder, keeping only the most recent ones.

    Args:
        folder (str): Path to the folder to clean up.
        keep (int): Number of most recent files to keep. Defaults to 10.
    """
    files = sorted(glob.glob(f"{folder}/*.csv"), key=os.path.getmtime, reverse=True)

    for file in files[keep:]:
        os.remove(file)


def cleanup_old_models(keep=3):
    """
    Delete old model files, keeping only the most recent ones.

    Args:
        keep (int): Number of most recent models to keep. Defaults to 3.
    """
    files = sorted(glob.glob("models/*.joblib"), key=os.path.getmtime, reverse=True)

    for file in files[keep:]:
        os.remove(file)