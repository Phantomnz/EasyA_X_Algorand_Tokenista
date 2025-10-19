from flask import Flask, jsonify, request
from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction
import time
import threading

# --- Best Practice 1: Configuration Management ---
# Configuration is separated from application logic.
class Config:
    # In a real app, use environment variables (os.getenv)
    ALGOD_TOKEN = "a" * 64 # Replace with your Algod API token
    ALGOD_ADDRESS = "http://localhost:4001" # Replace with your Algod node address
    APP_CREATOR_MNEMONIC = "your 25-word mnemonic here" # DANGER: Use a secrets manager in production!
    SMART_CONTRACT_ID = 12345 # Replace with your deployed App ID

# --- Application Factory ---
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Algorand client from config
    algod_client = algod.AlgodClient(app.config["ALGOD_TOKEN"], app.config["ALGOD_ADDRESS"])
    
    # --- In-memory database for hackathon MVP ---
    gpus = {}
    gpu_id_counter = 1

    # --- Best Practice 2: Non-blocking Operations (Simulated Background Tasks) ---
    def _execute_blockchain_call(task, *args):
        """A wrapper to run a 'slow' function in a background thread."""
        print(f"Handing off task '{task.__name__}' to a background thread.")
        thread = threading.Thread(target=task, args=args)
        thread.start()

    def actual_start_rental_contract(gpu_id, renter_address):
        """This would contain the real, slow algosdk logic."""
        print(f"BACKGROUND TASK: Starting rental for GPU {gpu_id}...")
        # Simulating a network call and transaction signing
        time.sleep(2) 
        # In real code:
        # creator_key = mnemonic.to_private_key(app.config["APP_CREATOR_MNEMONIC"])
        # params = algod_client.suggested_params()
        # ... build and send app call transaction ...
        print(f"BACKGROUND TASK: Blockchain call for GPU {gpu_id} complete.")
        # Here you would update the DB with the transaction result.
    
    def actual_stop_rental_contract(gpu_id):
        """This would contain the real, slow algosdk logic."""
        print(f"BACKGROUND TASK: Stopping rental for GPU {gpu_id}...")
        time.sleep(2)
        print(f"BACKGROUND TASK: Blockchain call for GPU {gpu_id} complete.")


    # --- Best Practice 3: Centralized Error Handling ---
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"status": "error", "message": "Resource not found"}), 404

    @app.errorhandler(400)
    def bad_request_error(error):
        # The description can be programmatically set when we call abort()
        message = error.description or "Bad request"
        return jsonify({"status": "error", "message": message}), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"status": "error", "message": "Internal server error"}), 500

    # --- API Endpoints ---
    @app.route("/gpus", methods=["POST"])
    def register_gpu():
        nonlocal gpu_id_counter
        data = request.get_json()
        
        # --- Best Practice 3: Input Validation ---
        required_fields = ["owner_address", "gpu_model", "price_per_minute"]
        if not data or not all(key in data for key in required_fields):
            return bad_request_error(type('BadRequest', (Exception,), {'description': 'Missing required fields.'})())
        if not isinstance(data["price_per_minute"], (int, float)) or data["price_per_minute"] <= 0:
            return bad_request_error(type('BadRequest', (Exception,), {'description': 'price_per_minute must be a positive number.'})())
        
        gpu_id = gpu_id_counter
        gpus[gpu_id] = {
            "id": gpu_id,
            "owner_address": data["owner_address"],
            "gpu_model": data["gpu_model"],
            "price_per_minute": data["price_per_minute"],
            "status": "available",
            "renter": None
        }
        gpu_id_counter += 1
        return jsonify({"status": "success", "message": "GPU registered", "gpu": gpus[gpu_id]}), 201

    @app.route("/gpus", methods=["GET"])
    def list_gpus():
        available_gpus = [gpu for gpu in gpus.values() if gpu["status"] == "available"]
        return jsonify({"status": "success", "gpus": available_gpus}), 200

    @app.route("/gpus/<int:gpu_id>/rent", methods=["POST"])
    def rent_gpu(gpu_id):
        if gpu_id not in gpus:
            return not_found_error(404)
        
        gpu = gpus[gpu_id]
        if gpu["status"] == "rented":
            return bad_request_error(type('BadRequest', (Exception,), {'description': 'GPU is already rented.'})())

        data = request.get_json()
        if not data or "renter_address" not in data:
            return bad_request_error(type('BadRequest', (Exception,), {'description': 'Missing renter_address.'})())

        # Update state immediately for responsiveness
        gpu["status"] = "renting_initiated"
        gpu["renter"] = data["renter_address"]
        
        # --- Best Practice 2: Offload slow task ---
        _execute_blockchain_call(actual_start_rental_contract, gpu_id, data["renter_address"])
        
        # Return 202 Accepted to indicate the process has started
        return jsonify({"status": "pending", "message": "GPU rental process initiated."}), 202

    @app.route("/gpus/<int:gpu_id>/stop", methods=["POST"])
    def stop_rental(gpu_id):
        if gpu_id not in gpus:
            return not_found_error(404)

        gpu = gpus[gpu_id]
        if gpu["status"] == "available":
            return bad_request_error(type('BadRequest', (Exception,), {'description': 'GPU is not currently rented.'})())
            
        # Offload the slow blockchain task
        _execute_blockchain_call(actual_stop_rental_contract, gpu_id)

        # Update state and make it available again
        gpu["status"] = "available"
        gpu["renter"] = None
        
        return jsonify({"status": "pending", "message": "GPU rental stop process initiated."}), 202

    return app

# --- Main execution ---
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)