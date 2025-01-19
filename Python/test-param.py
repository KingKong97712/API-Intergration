import argparse
import requests

API_URL = "http://127.0.0.1:8000/api/orders"
API_KEY = "_hiyk9bX1gf0a-xt7L5qEotPyWc9wUz7gD1bPRcftD04"

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

# Argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="API Client to interact with the order API.")
    parser.add_argument("action", choices=["register", "get"], help="Action to perform: 'register' to POST or 'get' to GET data")
    parser.add_argument("--order_id", type=int, help="Order ID to fetch (for GET) or specify order to register")
    return parser.parse_args()

# Register Orders Request
def register_orders():
    headers = {"API-Key": API_KEY}
    response = requests.post(API_URL, headers=headers, json=order_data)
    print("Response:", response.json())

# Get Order
def get_order(order_id):
    headers = {"API-Key": API_KEY}
    response = requests.get(f"{API_URL}/{order_id}", headers=headers)
    print("Order Details:", response.json())

def main():
    args = parse_args()

    if args.action == "register":
        #If Register, POST request
        register_orders()
    elif args.action == "get" and args.order_id:
        #GET request
        get_order(args.order_id)
    else:
        print("Error: 'order_id' must be specified for the 'get' action.")

if __name__ == "__main__":
    main()