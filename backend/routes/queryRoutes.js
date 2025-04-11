// backend/routes/queryRoutes.js
const express = require('express');
const router = express.Router();
const { createQuery } = require('../controllers/queryController');

router.post('/', createQuery);

module.exports = router;
