Algorand DePIN GPU Marketplace - BackendThis repository contains the Python Flask backend for our DePIN GPU Marketplace project, built for the EasyA x Algorand Hackathon. The backend provides a REST API to manage the registration and rental of GPU resources, with simulated integration to an Algorand smart contract.Table of ContentsProject OverviewGetting StartedPrerequisitesInstallation & SetupAPI EndpointsRegister a GPUList Available GPUsRent a GPUStop a GPU RentalArchitecture NotesProject OverviewThe goal is to create a decentralized physical infrastructure network (DePIN) on Algorand where users can:Supply: Register their own GPUs to make them available for rent.Demand: Rent GPU power from the network on a pay-per-minute basis.This backend server is the central API that a frontend application would interact with to facilitate these actions. It handles the application state and orchestrates calls to the (currently simulated) on-chain smart contract.Getting StartedFollow these instructions to get the backend server running locally.PrerequisitesPython 3.8+pip for package managementAn Algorand Sandbox running locally for testing. You can follow the official guide to set one up.Note for Windows Users: The Algorand Sandbox uses Docker and bash scripts (./sandbox). The recommended way to run this on Windows is by using the Windows Subsystem for Linux (WSL 2).Install WSL 2 from your terminal: wsl --install.Install Docker Desktop for Windows and ensure it is configured to use the WSL 2 backend.Run all commands for the Sandbox setup from within your WSL 2 terminal.Installation & SetupClone the Repository# Replace with your actual repository URL
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
Create requirements.txtCreate a file named requirements.txt and add the following lines:Flask
py-algorand-sdk
Install DependenciesCreate a virtual environment and install the required packages.# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
Configure the ServerOpen backend_final.py and modify the Config class with your Algorand Sandbox details:class Config:
    ALGOD_TOKEN = "a" * 64 # This is the default for Sandbox
    ALGOD_ADDRESS = "http://localhost:4001" # This is the default for Sandbox
    # DANGER: Fill this with a funded account from your Sandbox
    APP_CREATOR_MNEMONIC = "your 25-word mnemonic from a sandbox account" 
    SMART_CONTRACT_ID = 12345 # Replace with your deployed App ID later
Run the Serverpython backend_final.py
The server will start and be accessible at http://localhost:5001.API EndpointsThe following endpoints are available to interact with the service.1. Register a GPUPOST /gpus: Registers a new GPU to make it available for rent.Request Body (JSON):{
  "owner_address": "YOUR_ALGORAND_ADDRESS_HERE",
  "gpu_model": "NVIDIA RTX 4090",
  "price_per_minute": 0.05
}
Success Response (201 Created):{
  "status": "success",
  "message": "GPU registered",
  "gpu": {
    "id": 1,
    "owner_address": "YOUR_ALGORAND_ADDRESS_HERE",
    "gpu_model": "NVIDIA RTX 4090",
    "price_per_minute": 0.05,
    "status": "available",
    "renter": null
  }
}
2. List Available GPUsGET /gpus: Retrieves a list of all GPUs that are currently available for rent.Success Response (200 OK):{
  "status": "success",
  "gpus": [
    {
      "id": 1,
      "owner_address": "...",
      "gpu_model": "NVIDIA RTX 4090",
      "price_per_minute": 0.05,
      "status": "available",
      "renter": null
    }
  ]
}
3. Rent a GPUPOST /gpus/<int:gpu_id>/rent: Initiates the rental process for a specific GPU. This simulates a non-blocking call to the smart contract.Request Body (JSON):{
  "renter_address": "RENTER_ALGORAND_ADDRESS"
}
Success Response (202 Accepted):The server accepts the request and has started the background process to call the blockchain.{
  "status": "pending",
  "message": "GPU rental process initiated."
}
4. Stop a GPU RentalPOST /gpus/<int:gpu_id>/stop: Stops the rental for a specific GPU. This triggers the final payment calculation and transfer on the blockchain.Success Response (202 Accepted):{
  "status": "pending",
  "message": "GPU rental stop process initiated."
}
Architecture NotesNon-Blocking Calls: To ensure the server remains responsive, simulated blockchain interactions are handled in background threads. In a production environment, this would be managed by a dedicated task queue (e.g., Celery, RQ).Configuration: All sensitive and environment-specific data is stored in a central Config class, separating it from the application logic.Error Handling: The API provides consistent, structured JSON error messages for bad requests and server errors.