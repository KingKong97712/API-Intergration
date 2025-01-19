import json
import requests
# API endpoint URL
API_URL = "http://127.0.0.1:8000/api/orders"
API_KEY = "_hiyk9bX1gf0a-xt7L5qEotPyWc9wUz7gD1bPRcftD04"
headers = {"API-Key": API_KEY}
# JSON file Path
JSON_FILE_PATH = "order.json"

def send_order():
    try:
        #J SON file read
        with open(JSON_FILE_PATH, "r") as file:
            order_data = json.load(file)
        # Request 
        response = requests.post(API_URL, headers=headers, json=order_data)
        # Response
        if response.status_code == 200:
            print("Order sent successfully!")
            print("Response:", response.json())
        else:
            print(f"Failed to send order. Status code: {response.status_code}")
            print("Response:", response.text)
    except FileNotFoundError:
        print(f"Error: The file {JSON_FILE_PATH} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {JSON_FILE_PATH} contains invalid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    send_order()
