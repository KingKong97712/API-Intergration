require('dotenv').config();

const { Client } = require('pg');
const client = new Client({
  user: process.env.DB_USER,       
  host: process.env.DB_HOST,         
  database: process.env.DB_DATABASE,     
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,        
  ssl: {
    rejectUnauthorized: false
  }       
});

// Connect to the database
client.connect();

// Create tables if they don't exist
const createTables = async () => {
  await client.query(`
    CREATE TABLE IF NOT EXISTS orders (
      order_id SERIAL PRIMARY KEY,
      customer TEXT NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  `);

  await client.query(`
    CREATE TABLE IF NOT EXISTS order_items (
      item_id SERIAL PRIMARY KEY,
      order_id INTEGER REFERENCES orders(order_id),
      product TEXT NOT NULL,
      quantity INTEGER NOT NULL
    );
  `);
};

// Call the function to create tables
createTables().catch(console.error);

// Function to save an order
const saveOrder = (order_id, customer, items) => {
    return new Promise(async (resolve, reject) => {
        try {
       
        const existingOrder = await client.query(
            "SELECT * FROM orders WHERE order_id = $1",
            [order_id]
        );

        if (existingOrder.rows.length > 0) {
            return resolve(null); // Return an empty value if the order exists
        }

        const res = await client.query(
            "INSERT INTO orders (order_id, customer) VALUES ($1, $2) RETURNING *",
            [order_id, customer]
        );
        
        for (const item of items) {
            await client.query(
            "INSERT INTO order_items (order_id, product, quantity) VALUES ($1, $2, $3)",
            [order_id, item.product, item.quantity]
            );
        }

        resolve(res.rows[0]);  // Returning the inserted order
        } catch (err) {
        reject(err);
        }
    });
};
  

// Function to get order details by order_id
const getOrderDetails = (order_id) => {
  return new Promise(async (resolve, reject) => {
    try {
      // Query the Orders table
      const res = await client.query(
        "SELECT * FROM orders WHERE order_id = $1",
        [order_id]
      );
      const order = res.rows[0];

      if (!order) {
        return resolve(null);  // Return null if order not found
      }

      // Query the Order_Items table
      const itemsRes = await client.query(
        "SELECT * FROM order_items WHERE order_id = $1",
        [order_id]
      );
      const items = itemsRes.rows;

      resolve({ ...order, items });
    } catch (err) {
      reject(err);
    }
  });
};

module.exports = { saveOrder, getOrderDetails };
