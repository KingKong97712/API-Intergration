require('dotenv').config();

const API_KEY = process.env.API_KEY;

// Middleware to authenticate API requests
const authenticate = (req, res, next) => {
  const apiKey = req.headers['api-key'];
  if (apiKey === API_KEY) {
    return next();
  }
  return res.status(403).json({ status: 'error', message: 'Invalid API key' });
};

module.exports = { authenticate };
