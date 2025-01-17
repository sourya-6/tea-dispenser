import mongoose from 'mongoose';

const customTeaOrderSchema = new mongoose.Schema({
  customerId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Customer',
    required: true
  },
  milkAmount: {
    type: Number,
    required: true
  },
  waterAmount: {
    type: Number,
    required: true
  },
  teaPowderAmount: {
    type: Number,
    required: true
  },
  Temperature:{
    type:Number,
    default:200//just an example we can change the temp
  },
  Timing:{
    type:Number,
    // default:500
  },
  Sugar:{
    type:Number,
    required:true
  }


  // Add other fields as needed
});

const CustomTeaOrder = mongoose.model('CustomTeaOrder', customTeaOrderSchema);

export default CustomTeaOrder;
