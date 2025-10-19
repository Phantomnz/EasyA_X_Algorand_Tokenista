💻 GPU Rental Marketplace on Algorand: BitFox
=====================================

Welcome to our project for the EasyA x Algorand Hackathon! This is the backend server for a marketplace where anyone can rent out their computer's GPU power to others.

Table of Contents
-----------------

*   [What is This Project?]
    
*   [How Does It Work?]
    
*   [For Developers: Running The Project]
    
*   [What's Under The Hood?]
    

🤔 What is This Project?
------------------------

Think of it like Airbnb, but for computer power.

Lots of people have powerful graphics cards (GPUs) in their computers that sit idle most of the time. At the same time, others need access to that power for tasks like AI, scientific research, or 3D rendering, but don't want to buy an expensive machine themselves.

Our project creates a simple, secure marketplace to connect these two groups:

*   **Providers** can list their GPUs and earn money when they're not using them.
    
*   **Renters** can get affordable, on-demand access to high-performance computing.
    

We are building this on the Algorand blockchain to ensure that payments are fast, cheap, and transparent.

✨ How Does It Work?
-------------------

Our backend server acts as the "front desk" for this marketplace. It handles all the key actions a user would want to take. Here’s what you can do:

### 1\. Put a GPU up for Rent

A provider can register their GPU, setting a price per minute.

> **Technical Info:** This is done by sending a POST request to the /gpus endpoint.

### 2\. See Available GPUs

A renter can browse a list of all the GPUs that are currently available to be rented.

> **Technical Info:** This is done by sending a GET request to the /gpus endpoint.

### 3\. Rent a GPU

When a renter finds a GPU they like, they can start renting it. This kicks off a process on the blockchain to lock in the rental agreement.

> **Technical Info:** This is done by sending a POST request to the /gpus//rent endpoint.

### 4\. Stop the Rental & Pay

Once the renter is finished, they can stop the rental. The system automatically calculates the total cost based on how long they used it and handles the payment on the Algorand network.

### 5\. Investors co-own datacentre clusters

On our platform we allow fractional ownership of high performance GPU clusters (like those including the H100s that power your AIs), bringing
the compute of giants to aspiring companies for a fraction of time and a fraction of the cost.

> **Technical Info:** This is done by sending a POST request to the /gpus//stop endpoint.

🛠️ For Developers: Running The Project
---------------------------------------

If you want to run the code yourself, follow these steps.

### Prerequisites

You'll need a few things installed first:

*   Python (Version 3.8 or newer)
    
*   An Algorand Sandbox for local testing. You can get this by following the [Official Algorand Guide](https://www.google.com/search?q=https://developer.algorand.org/docs/run-a-node/setup/install/#sandbox-and-docker).
    

> **A Note for Windows Users:** The Algorand Sandbox runs best using the Windows Subsystem for Linux (WSL 2). It's a tool that lets you run a Linux environment directly on Windows. You'll need to install WSL 2 and Docker Desktop, then run the sandbox commands from the WSL terminal.

### Setup Instructions

1.  **Clone the code** from this repository.
    
2.  **Install the necessary Python packages:** pip install Flask py-algorand-sdk.
    
3.  **Configure your settings** in the backend\_final.py file. You'll need to add your Algorand Sandbox address and a funded account mnemonic.
    
4.  **Run the server** with the command: python backend\_final.py.
    

You should see it running on http://localhost:5001.

⚙️ What's Under The Hood? (Architecture Notes)
----------------------------------------------

We designed the backend with a few key principles in mind:

*   **Speedy & Responsive:** When you ask the server to do something on the blockchain (like start a rental), it accepts the request instantly and does the work in the background. This means the user doesn't have to wait.
    
*   **Clean & Organized:** All important settings (like API keys) are kept in one place, separate from the main logic. This makes the code safer and easier to update.
    
*   **Clear Communication:** If something goes wrong, the server sends back a clear, easy-to-understand error message.