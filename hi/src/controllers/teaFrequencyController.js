import TeaFrequency from '../models/teaFrequencyModel.js';

// Get tea frequency for a specific customer
export const getTeaFrequency = async (req, res, next) => {
  try {
    const teaFrequency = await TeaFrequency.findOne({ customerId: req.params.customerId });
    if (!teaFrequency) return res.status(404).json({ success: false, message: 'Tea frequency data not found' });
    res.status(200).json({ success: true, data: teaFrequency });
  } catch (err) {
    next(err);
  }
};
