import TeaRecipe from '../models/teaRecipeModel.js';
import { successResponse, createdResponse } from '../utils/responseHelper.js';

// Get all teas
export const getAllTeas = async (req, res, next) => {
  try {
    const teas = await TeaRecipe.find();
    
    successResponse(res, teas);
  } catch (err) {
    next(err); // Pass errors to the error handling middleware
  }
};

// Get tea by ID
export const getTeaById = async (req, res, next) => {
  try {
    const tea = await TeaRecipe.findById(req.params.id);
    console.log(tea)
    if (!tea) return res.status(404).json({ success: false, message: 'Tea not found' });
    successResponse(res, tea);
  } catch (err) {
    next(err);
  }
};

// Create a new tea
export const createTea = async (req, res, next) => {
  try {
    const newTea = new TeaRecipe(req.body);
    await newTea.save();
    createdResponse(res, newTea, 'Tea created successfully');
  } catch (err) {
    next(err);
  }
};

// Update an existing tea
export const updateTea = async (req, res, next) => {
  try {
    const updatedTea = await TeaRecipe.findByIdAndUpdate(req.params.id, req.body, { new: true });
    if (!updatedTea) return res.status(404).json({ success: false, message: 'Tea not found' });
    successResponse(res, updatedTea, 'Tea updated successfully');
  } catch (err) {
    next(err);
  }
};

// Delete a tea
export const deleteTea = async (req, res, next) => {
  try {
    const deletedTea = await TeaRecipe.findByIdAndDelete(req.params.id);
    if (!deletedTea) return res.status(404).json({ success: false, message: 'Tea not found' });
    res.status(204).send();
  } catch (err) {
    next(err);
  }
};
