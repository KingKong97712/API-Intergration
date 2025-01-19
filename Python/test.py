import os
import requests
from dotenv import load_dotenv
#API_KEY Read from .env File
load_dotenv()

API_URL = "http://127.0.0.1:8000/api/orders"
API_KEY = os.getenv("API_KEY")

order_data = [
    {
        "order_id": 123,
        "customer": "John Doe",
        "items": [
            {"product": "Mug", "quantity": 2},
            {"product": "Pen", "quantity": 3}
        ]
    },
    {
        "order_id": 6565,
        "customer": "AFD Doe",
        "items": [
            {"product": "JUE", "quantity": 5},
            {"product": "PIP", "quantity": 8}
        ]
    }
]

headers = {"API-Key": API_KEY}
# SaveOrder Request & Response
response = requests.post(API_URL, headers=headers, json=order_data)
print("Response:", response.json())
print("Staus:", response.json()['status'])
print("OrderID:", response.json()['order_ids'])
print("Warning:", response.json()['warnings'])
# Order Details Request & Response
response = requests.get(f"{API_URL}/123", headers=headers)
print("Order Details:", response.json())
