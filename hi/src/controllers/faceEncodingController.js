import FaceEncoding from '../models/faceEncodingModel.js';
import { ApiError } from '../utils/apiError.js';

//steps required:-
//scanning face and check with the previous urls 
//if exist give them the recent data and the maximum used data
//if not exist ask the user to fill the details-amount of milk,water ,sugar ,teapowder,temp(default needs to be there)
//



// Add a new face encoding
export const addFaceEncoding = async (req, res, next) => {
  try {
    const newFaceEncoding = new FaceEncoding(req.body);
    await newFaceEncoding.save();
    // res.status(201).json({ success: true, message: 'Face encoding added successfully' });
    throw new ApiError(201,"Face encoding added successfully")
  } catch (err) {
    next(err);
  }
};

// Get all face encodings
export const getFaceEncodings = async (req, res, next) => {
  try {
    const faceEncodings = await FaceEncoding.find();
    res.status(200).json({ success: true, data: faceEncodings });
  } catch (err) {
    next(err);
  }
};
