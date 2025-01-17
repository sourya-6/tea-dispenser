import express from 'express';
const router = express.Router();

import { createCustomTeaOrder, getCustomTeaOrders } from '../controllers/customTeaController.js';

// Route handlers
router.post('/', createCustomTeaOrder);
router.get('/', getCustomTeaOrders);

export default router;
