import mongoose from 'mongoose';

const teaRecipeSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    unique: true
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
  // Add other fields as needed
});

const TeaRecipe = mongoose.model('TeaRecipe', teaRecipeSchema);

export default TeaRecipe;
