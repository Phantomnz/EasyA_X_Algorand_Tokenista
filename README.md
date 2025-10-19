Algorand DePIN GPU Marketplace - Backend
========================================

This repository contains the Python Flask backend for our DePIN GPU Marketplace project, built for the EasyA x Algorand Hackathon. The backend provides a REST API to manage the registration and rental of GPU resources, with simulated integration to an Algorand smart contract.

Table of Contents
-----------------

*   [Project Overview](https://www.google.com/search?q=#project-overview)
    
*   [Getting Started](https://www.google.com/search?q=#getting-started)
    
    *   [Prerequisites](https://www.google.com/search?q=#prerequisites)
        
    *   [Installation & Setup](https://www.google.com/search?q=#installation--setup)
        
*   [API Endpoints](https://www.google.com/search?q=#api-endpoints)
    
    *   [Register a GPU](https://www.google.com/search?q=#1-register-a-gpu)
        
    *   [List Available GPUs](https://www.google.com/search?q=#2-list-available-gpus)
        
    *   [Rent a GPU](https://www.google.com/search?q=#3-rent-a-gpu)
        
    *   [Stop a GPU Rental](https://www.google.com/search?q=#4-stop-a-gpu-rental)
        
*   [Architecture Notes](https://www.google.com/search?q=#architecture-notes)
    

Project Overview
----------------

The goal is to create a decentralized physical infrastructure network (DePIN) on Algorand where users can:

1.  **Supply**: Register their own GPUs to make them available for rent.
    
2.  **Demand**: Rent GPU power from the network on a pay-per-minute basis.
    

This backend server is the central API that a frontend application would interact with to facilitate these actions. It handles the application state and orchestrates calls to the (currently simulated) on-chain smart contract.

Getting Started
---------------

Follow these instructions to get the backend server running locally.

### Prerequisites

*   Python 3.8+
    
*   pip for package management
    
*   An Algorand Sandbox running locally for testing. You can follow the [official guide to set one up](https://www.google.com/search?q=https://developer.algorand.org/docs/run-a-node/setup/install/#sandbox-and-docker).
    

### Installation & Setup

1.  \# Replace with your actual repository URLgit clone \[https://github.com/your-username/your-repo-name.git\](https://github.com/your-username/your-repo-name.git)cd your-repo-name
    
2.  Create a file named requirements.txt and add the following lines:Flaskpy-algorand-sdk
    
3.  Create a virtual environment and install the required packages.# Create a virtual environment (recommended)python -m venv venvsource venv/bin/activate # On Windows, use \`venv\\Scripts\\activate\`# Install dependenciespip install -r requirements.txt
    
4.  Open backend\_final.py and modify the Config class with your Algorand Sandbox details:class Config: ALGOD\_TOKEN = "a" \* 64 # This is the default for Sandbox ALGOD\_ADDRESS = "http://localhost:4001" # This is the default for Sandbox # DANGER: Fill this with a funded account from your Sandbox APP\_CREATOR\_MNEMONIC = "your 25-word mnemonic from a sandbox account" SMART\_CONTRACT\_ID = 12345 # Replace with your deployed App ID later
    
5.  python backend\_final.pyThe server will start and be accessible at http://localhost:5001.
    

API Endpoints
-------------

The following endpoints are available to interact with the service.

### 1\. Register a GPU

*   **POST /gpus**: Registers a new GPU to make it available for rent.
    
*   { "owner\_address": "YOUR\_ALGORAND\_ADDRESS\_HERE", "gpu\_model": "NVIDIA RTX 4090", "price\_per\_minute": 0.05}
    
*   { "status": "success", "message": "GPU registered", "gpu": { "id": 1, "owner\_address": "YOUR\_ALGORAND\_ADDRESS\_HERE", "gpu\_model": "NVIDIA RTX 4090", "price\_per\_minute": 0.05, "status": "available", "renter": null }}
    

### 2\. List Available GPUs

*   **GET /gpus**: Retrieves a list of all GPUs that are currently available for rent.
    
*   { "status": "success", "gpus": \[ { "id": 1, "owner\_address": "...", "gpu\_model": "NVIDIA RTX 4090", "price\_per\_minute": 0.05, "status": "available", "renter": null } \]}
    

### 3\. Rent a GPU

*   **POST /gpus//rent**: Initiates the rental process for a specific GPU. This simulates a non-blocking call to the smart contract.
    
*   { "renter\_address": "RENTER\_ALGORAND\_ADDRESS"}
    
*   The server accepts the request and has started the background process to call the blockchain.{ "status": "pending", "message": "GPU rental process initiated."}
    

### 4\. Stop a GPU Rental

*   **POST /gpus//stop**: Stops the rental for a specific GPU. This triggers the final payment calculation and transfer on the blockchain.
    
*   { "status": "pending", "message": "GPU rental stop process initiated."}
    

Architecture Notes
------------------

*   **Non-Blocking Calls**: To ensure the server remains responsive, simulated blockchain interactions are handled in background threads. In a production environment, this would be managed by a dedicated task queue (e.g., Celery, RQ).
    
*   **Configuration**: All sensitive and environment-specific data is stored in a central Config class, separating it from the application logic.
    
*   **Error Handling**: The API provides consistent, structured JSON error messages for bad requests and server errors.