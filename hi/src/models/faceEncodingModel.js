import mongoose from 'mongoose';

const faceEncodingSchema = new mongoose.Schema({
  customerId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Customer',
    required: true
  },
  encoding: {
    type: [Number], // Assuming face encoding is an array of numbers
    required: true
  }
});

const FaceEncoding = mongoose.model('FaceEncoding', faceEncodingSchema);

export default FaceEncoding;
