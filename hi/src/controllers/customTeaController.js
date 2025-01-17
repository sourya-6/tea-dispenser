import CustomTeaOrder from '../models/customTeaOrderModel.js';
import { createdResponse, successResponse } from '../utils/responseHelper.js';

// Create a custom tea order

//
export const createCustomTeaOrder = async (req, res, next) => {
  try {
    const newOrder = new CustomTeaOrder(req.body);
    await newOrder.save();
    createdResponse(res, newOrder, 'Custom tea order created successfully');
  } catch (err) {
    next(err);
  }
};

// Get all custom tea orders
export const getCustomTeaOrders = async (req, res, next) => {
  try {
    const orders = await CustomTeaOrder.find();
    successResponse(res, orders);
  } catch (err) {
    next(err);
  }
};
