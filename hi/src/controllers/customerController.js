import Customer from '../models/customerModel.js';
import { successResponse, createdResponse } from '../utils/responseHelper.js';

// Get customer by ID

export const getCustomerById = async (req, res, next) => {
  const{name,email}=req.body
console.log(name)
console.log(email)
  try {
    const customer = await Customer.findById(req.params.id);
    if (!customer) return res.status(404).json({ success: false, message: 'Customer not found' });
    successResponse(res, customer);
  } catch (err) {
    next(err);
  }
};

// Create a new customer
export const createCustomer = async (req, res, next) => {
  try {
    const newCustomer = new Customer(req.body);
    await newCustomer.save();
    createdResponse(res, newCustomer, 'Customer created successfully');
  } catch (err) {
    next(err);
  }
};

// Update an existing customer
export const updateCustomer = async (req, res, next) => {
  try {
    const updatedCustomer = await Customer.findByIdAndUpdate(req.params.id, req.body, { new: true });
    if (!updatedCustomer) return res.status(404).json({ success: false, message: 'Customer not found' });
    successResponse(res, updatedCustomer, 'Customer updated successfully');
  } catch (err) {
    next(err);
  }
};

// Delete a customer
export const deleteCustomer = async (req, res, next) => {
  try {
    const deletedCustomer = await Customer.findByIdAndDelete(req.params.id);
    if (!deletedCustomer) return res.status(404).json({ success: false, message: 'Customer not found' });
    res.status(204).send();
  } catch (err) {
    next(err);
  }
};
