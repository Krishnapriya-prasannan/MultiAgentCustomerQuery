// backend/controllers/queryController.js
const Query = require('../models/queryModel');

const createQuery = async (req, res) => {
  try {
    const { name, email, message } = req.body;
    const newQuery = new Query({ name, email, message });
    await newQuery.save();
    res.status(201).json({ message: 'Query saved successfully' });
  } catch (error) {
    res.status(500).json({ error: 'Something went wrong' });
  }
};

module.exports = { createQuery };
