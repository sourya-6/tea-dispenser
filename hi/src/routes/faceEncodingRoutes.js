import express from 'express';
const router = express.Router();

// Import your controllers here
import { addFaceEncoding, getFaceEncodings } from '../controllers/faceEncodingController.js';

// Route handlers
router.post('/', addFaceEncoding);
router.get('/', getFaceEncodings);

export default router;
