import mongoose from 'mongoose';

const teaFrequencySchema = new mongoose.Schema({
  customerId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Customer',
    required: true
  },
  teaId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'TeaRecipe',
    required: true
  },
  frequency: {
    type: Number,
    required: true
  }
});

const TeaFrequency = mongoose.model('TeaFrequency', teaFrequencySchema);

export default {TeaFrequency};
