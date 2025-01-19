const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./database.db');

// Create tables if they don't exist
db.serialize(() => {
  db.run("CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY, customer TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)");
  db.run("CREATE TABLE IF NOT EXISTS order_items (item_id INTEGER PRIMARY KEY, order_id INTEGER, product TEXT, quantity INTEGER, FOREIGN KEY(order_id) REFERENCES Orders(order_id))");
});

// Function to save an order
const saveOrder = (order_id, customer, items) => {
    return new Promise((resolve, reject) => {
      // Check if the order already exists
      db.get("SELECT * FROM orders WHERE order_id = ?", [order_id], (err, row) => {
        if (err) return reject(err);
        if (row) {
          // Return an empty value if the order exists
          return resolve(null);
        }
        // Insert the order if it does not exist
        db.run("INSERT INTO orders (order_id, customer) VALUES (?, ?)", [order_id, customer], function(err) {
          if (err) return reject(err);
  
          // Insert order items
          const insertItemPromises = items.map(item => {
            return new Promise((resolveItem, rejectItem) => {
              db.run("INSERT INTO order_items (order_id, product, quantity) VALUES (?, ?, ?)", [order_id, item.product, item.quantity], function(err) {
                if (err) return rejectItem(err);
                resolveItem();
              });
            });
          });
  
          // Wait for all item inserts to complete
          Promise.all(insertItemPromises)
            .then(() => {
              resolve({ order_id, customer });
            })
            .catch(reject);
        });
      });
    });
  };
  

// Function to get order details by order_id
const getOrderDetails = (order_id) => {
  return new Promise((resolve, reject) => {
    db.all("SELECT * FROM orders WHERE order_id = ?", [order_id], (err, rows) => {
      if (err) return reject(err);
      if (rows.length === 0) return resolve(null);

      const order = rows[0];
      db.all("SELECT * FROM order_items WHERE order_id = ?", [order_id], (err, items) => {
        if (err) return reject(err);
        resolve({ ...order, items });
      });
    });
  });
};

module.exports = { saveOrder, getOrderDetails };
