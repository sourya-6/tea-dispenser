// src/utils/responseHelper.js

const successResponse = (res, data, message = 'Request was successful') => {
    res.status(200).json({
      success: true,
      message,
      data
    });
  };
  
  const createdResponse = (res, data, message = 'Resource created successfully') => {
    res.status(201).json({
      success: true,
      message,
      data
    });
  };
  
  const noContentResponse = (res, message = 'No content') => {
    res.status(204).json({
      success: true,
      message
    });
  };
  
//   module.exports = {
//     successResponse,
//     createdResponse,
//     noContentResponse
//   };
  
export{successResponse,createdResponse,noContentResponse}