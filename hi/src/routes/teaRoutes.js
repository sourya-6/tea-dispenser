import express from 'express';
const router = express.Router();

import { getAllTeas, getTeaById, createTea, updateTea, deleteTea } from '../controllers/teaController.js';

// Route handlers
router.get('/', getAllTeas);
router.get('/:id', getTeaById);
router.post('/', createTea);
router.put('/:id', updateTea);
router.delete('/:id', deleteTea);

export default router;
