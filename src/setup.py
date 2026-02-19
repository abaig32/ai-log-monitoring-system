from log_collector import collect_win_logs
from log_processor import process_logs
from train_model import finished_model
from utils import get_latest_model, get_latest_raw_file


def run_initial_setup():
    collect_win_logs(days=7)
    latest_raw_file = get_latest_raw_file()
    process_logs(latest_raw_file)
    finished_model()


def main():
    print("\n" + "="*50)
    print("INITIAL SETUP - MODEL TRAINING")
    print("="*50 + "\n")

    existing_model = get_latest_model()

    if existing_model:
        print(f"Found existing model: {existing_model}")
        response = input("Do you want to retrain? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled. Using existing model.")
            return

    print("Starting initial training process...")
    print("This will collect 7 days of logs and train the model.\n")

    # Step 1: Collect
    print("[1/4] Collecting 7 days of logs...")
    collect_win_logs(days=7)

    # Step 2: Get latest
    print("\n[2/4] Finding latest raw file...")
    latest_raw_file = get_latest_raw_file()

    # Step 3: Process
    print("\n[3/4] Processing logs...")
    process_logs(latest_raw_file)

    # Step 4: Train
    print("\n[4/4] Training model...")
    finished_model()

    print("\n" + "="*50)
    print("Setup complete! Model trained successfully.")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()