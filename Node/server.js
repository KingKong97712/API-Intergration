const express = require('express');
const bodyParser = require('body-parser');
const { authenticate } = require('./auth');
const app = express();
const PORT = process.env.PORT || 3000;
let db;
if (process.env.DB_TYPE == 'postgresql') {
    db = require('./postgresql'); // PostgreSQL include
} else {
    db = require('./db'); // SQLite include
}
const { saveOrder, getOrderDetails } = db;
// Middleware to parse JSON requests
app.use(bodyParser.json());

// API endpoint to insert orders
app.post('/api/orders', authenticate, async (req, res) => {
    const orders = req.body;  // Expecting an array of orders
    
    // Validate Input
    if (!Array.isArray(orders) || orders.length === 0) {
      return res.status(400).json({ status: 'error', message: 'Invalid input data' });
    }
    
    try {
      const savedOrders = [];
      const warningOrders = [];
      
      for (const order of orders) {
        const { order_id, customer, items } = order;
        // Validate each order individually
        if (!order_id || !customer || !Array.isArray(items) || items.length === 0) {
          return res.status(400).json({ status: 'error', message: 'Invalid order data' });
        }
        // Save the order
        const savedOrder = await saveOrder(order_id, customer, items);
        
        if (savedOrder != null) {
            savedOrders.push(order_id); 
        } else {
            warningOrders.push(`Order ID ${order_id} already exists.`); 
        }            
      }
  
      // Return a success response with all saved orders
      res.status(200).json({ status: 'success', order_ids: savedOrders, warnings: warningOrders });
    } catch (err) {
      res.status(500).json({ status: 'error', message: 'Internal server error' });
    }
  });
  

// API endpoint to retrieve orders
app.get('/api/orders/:order_id', authenticate, async (req, res) => {
  const { order_id } = req.params;
  try {
    const orderDetails = await getOrderDetails(order_id);
    if (!orderDetails) {
      return res.status(404).json({ status: 'error', message: 'Order not found' });
    }
    res.status(200).json(orderDetails);
  } catch (err) {
    res.status(500).json({ status: 'error', message: 'Internal server error' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});