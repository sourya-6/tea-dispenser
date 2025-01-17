import express from 'express';
import cors from 'cors';
import cookieParser from 'cookie-parser';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const app = express();

// Initialize CORS
app.use(cors({
    origin: process.env.CORS_ORIGIN,
    credentials: true
}));

// Middleware
app.use(express.json({ limit: '16kb' }));
app.use(express.urlencoded({ extended: true, limit: '16kb' }));
app.use(cookieParser());
app.use(express.static('public'));

// Routes
import teaRoutes from './routes/teaRoutes.js';
import customerRoutes from './routes/customerRoutes.js';
import customTeaRoutes from './routes/customTeaRoutes.js';
import faceEncodingRoutes from './routes/faceEncodingRoutes.js';
import teaFrequencyRoutes from './routes/teaFrequencyRoutes.js';

app.use('/api/teas', teaRoutes);
app.use('/api/customers', customerRoutes);
app.use('/api/custom-teas', customTeaRoutes);
app.use('/api/face-encodings', faceEncodingRoutes);
app.use('/api/tea-frequencies', teaFrequencyRoutes);

// Error handling middleware
// import errorHandler from './middlewares/errorHandler.js';
// app.use(errorHandler);

export {app} ;
