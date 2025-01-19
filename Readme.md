# API Development and Integration

This project implements an API with the following functionality:
1. **Create an Order** - POST request to add orders with validation and persistence.
2. **Retrieve Order Details** - GET request to fetch order details by `order_id`.
3. **Authentication** - Simple static API key authentication to protect endpoints.
4. **Raspberry Pi Integration** - Python script to simulate sending orders to the API.

## Project Structure

api_project/
│
├── Node           # API Server (Node.js)
├── Python         # API Server & API Requests (Python)
├── RaspberryPi    # Raspberry Pi Integration
└── Readme.md      # Project User Guide

## Requirements

- Python v3.10.4
- Node v23.0.0
- SQLite (or PostgreSQL) as the database

## Installation

### Step 1: Install Python Dependencies
Navigate to the Python directory and install the necessary dependencies:
```bash
cd Python
pip install -r requirements.txt
```
### Step 2: Install Node Dependencies
Navigate to the Node directory and install the necessary dependencies:
```bash
cd Node
npm install
```
## Setting environment variables `.env`

### Python
    Create a .env file for the Python application with the following variables:
        - API_KEY: Static API key for authentication.
        - DATABASE_TYPE: Set to True for SQLite, False for PostgreSQL.
    Example:
        API_KEY=_hiyk9bX1gf0a-xt7L5qEotPyWc9wUz7gD1bPRcftD04
        DATABASE_TYPE=True  # Set to False for PostgreSQL
### Node
    Create a .env file for the Node application with the following variables:
        - API_KEY: Static API key for authentication.
        - PORT: The port the Node server will run on (default: 8080). 
        - DB_TYPE: Set to postgresql for PostgreSQL or sqlite for SQLite.
        - If using PostgreSQL: DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, and DB_NAME for connection details.
    Example:
        API_KEY=_hiyk9bX1gf0a-xt7L5qEotPyWc9wUz7gD1bPRcftD04
        PORT=8000
        DB_TYPE=postgresql
        DB_HOST=localhost
        DB_PORT=5432
        DB_USER=your_username
        DB_PASSWORD=your_password
        DB_NAME=your_database_name    

## Running the API

### Step 1: Start the Server

#### Python Case:
To start the FastAPI server, run the following command in the Python directory:
```bash
cd Python
uvicorn main:app --reload
```

#### Node Case:
To start the Node.js server, run the following command in the Node directory:
```bash
cd Node
node server.js 
#or
npm start
```

### Step 2: Run the Script to Test the API

#### Create and Retrieve Orders:
Run the test.py script to create and retrieve orders:
```bash
cd Python
python test.py
```

#### Using Parameters for Actions:
- Create an order:
```bash
cd Python
python test-param.py register
```
- Retrieve an order by order_id:
```bash
cd Python
python test-param.py get --order_id 123
```
## Raspberry Pi Integration
To simulate sending orders to the API from a Raspberry Pi, run the following script in the RaspberryPi directory:
```bash
cd RaspberryPi
python sender_order.py
```

## Tools
- DB Browser (SQLite): Use DB Browser to browse the SQLite database
    Download Here: [https://sqlitebrowser.org/dl/]
- PostgreSQL Setup: You can use online services to set up a PostgreSQL server
    [https://console.aiven.io/]
- pgAdmin4: Use pgAdmin4 to view and manage your PostgreSQL database.
    [https://www.pgadmin.org/download/pgadmin-4-windows/]
    