import express from 'express';
const router = express.Router();

// Import your controllers here
import { getTeaFrequency } from '../controllers/teaFrequencyController.js';

// Route handlers
router.get('/:customerId', getTeaFrequency);

export default router;
