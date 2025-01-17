// src/middlewares/errorHandler.js

const errorHandler = (err, req, res, next) => {
    console.error(err.stack);
  
    // Check for specific error types or set a generic message
    const statusCode = err.statusCode || 500;
    const message = err.message || 'Internal Server Error';
  
    res.status(statusCode).json({
      success: false,
      error: message
    });
  };
  
//   module.exports = errorHandler;
  
  export{errorHandler}