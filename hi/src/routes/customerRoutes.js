import express from 'express';
const router = express.Router();

import { getCustomerById, createCustomer, updateCustomer, deleteCustomer } from '../controllers/customerController.js';

// Route handlers
router.get('/:id', getCustomerById);
router.post('/', createCustomer);
router.put('/:id', updateCustomer);
router.delete('/:id', deleteCustomer);

export default router;
