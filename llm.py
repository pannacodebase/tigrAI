import requests

# Replace with your IBM Cloud API Key
API_KEY = ""

# Step 1: Get the Bearer token
def get_bearer_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Step 2: Make the API request to Watsonx AI
def call_watsonx_ai(token):
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "input": "I would like to know about this material: steel. I need more information on tensile. Give me 5 short sentences on steel.",
        "model_id": "ibm/granite-13b-chat-v2",
        "project_id": "ca6a4785-a89e-49cd-87e7-2a1346b94c01",
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 900,
            "min_new_tokens": 50,
            "decoding_method": "sample",
            "repetition_penalty": 2
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Main script
if __name__ == "__main__":
    token = get_bearer_token(API_KEY)
    if token:
        result = call_watsonx_ai(token)
        if result:
            print("Response from Watsonx AI:")
            print(result)
