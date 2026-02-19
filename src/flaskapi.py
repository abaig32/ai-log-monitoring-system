from flask import Flask, jsonify
from anomaly_detector import detector
from setup import run_initial_setup
from utils import get_latest_model

app = Flask(__name__)


@app.route('/setup', methods=['POST'])
def setup():
    """Run the initial setup pipeline — collects 7 days of logs, processes them, and trains the model."""
    run_initial_setup()

    return jsonify({'status': 'success'})


@app.route('/status', methods=['GET'])
def status():
    """Return the path of the latest trained model, or None if no model exists."""
    latest_model = get_latest_model()

    return jsonify({'model': latest_model})


@app.route('/detect', methods=['POST'])
def detect():
    """Run anomaly detection on the latest processed logs and return results as JSON."""
    results = detector()

    if results is None:
        return jsonify({'error': 'Detection failed - no model or processed file found'}), 400

    return jsonify(results.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)