import requests
import json

# Step 1: Define endpoint URL
# Default port for serving. Ensure it matches what is run on command line
url = "http://127.0.0.1:5001/invocations"

# Step 2: Define Prediction Input Payload
# In modern MLflow, dataframe records or split representation is used
payload = {
    "dataframe_records": [
        # Record 1: 10 features representing customer metrics
        [-0.5, 1.2, 0.4, -0.9, 0.1, 0.5, -0.3, 0.8, -0.1, 0.2],
        # Record 2: 10 features representing another customer
        [0.8, -0.2, 0.9, 0.1, -0.4, 0.6, 0.2, -0.5, 0.3, 0.1]
    ]
}

headers = {"Content-Type": "application/json"}

if __name__ == "__main__":
    print(f"Attempting to query local model server at: {url}...")
    
    try:
        # Send post request
        response = requests.post(url, headers=headers, json=payload)
        
        # Verify status code
        if response.status_code == 200:
            predictions = response.json()
            print("\n--- Server Response Success! ---")
            print(f"Predictions: {predictions}")
        else:
            print(f"\n[ERROR] Server returned status code {response.status_code}")
            print(f"Server response text: {response.text}")
            
    except Exception as e:
        print("\n[ERROR] Connection failed!")
        print("Please check that your MLflow model serving daemon is running.")
        print("To start it, run this command in a separate terminal:")
        print("mlflow models serve -m \"models:/CustomerChurnClassifier/Production\" --port 5001 --no-conda --env-manager=local")
        print(f"Technical details: {e}")
