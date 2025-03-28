


/**
* Class representing an API error.
* @extends Error
*/
export class ApiError extends Error {
 /**
  * Create an API error.
  * @param {string} message - The error message.
  * @param {number} status - The HTTP status code.
  * @param {string} [code='API_ERROR'] - The error code.
  */
 constructor(message, status, code = 'API_ERROR') {
   super(message);
   /**
    * The HTTP status code.
    * @type {number}
    */
   this.status = status;
   /**
    * The error code.
    * @type {string}
    */
   this.code = code;
   /**
    * The name of the error.
    * @type {string}
    */
   this.name = 'ApiError';
 }
}


export const API_STATUS = {
  IDLE: 'idle',
  LOADING: 'loading',
  SUCCESS: 'success',
  ERROR: 'error',
  UNAVAILABLE: 'unavailable'
};

export const ERROR_CODES = {
  NETWORK_ERROR: 'NETWORK_ERROR',
  API_DOWN: 'API_DOWN',
  UNAUTHORIZED: 'UNAUTHORIZED',
  FORBIDDEN: 'FORBIDDEN',
  NOT_FOUND: 'NOT_FOUND',
  RATE_LIMIT: 'RATE_LIMIT',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  SERVER_ERROR: 'SERVER_ERROR',
  UNKNOWN_ERROR: 'UNKNOWN_ERROR'
};

export const getErrorFromStatus = (status, message = '') => {
  switch (status) {
    case 400:
      return new ApiError(message || 'Bad Request', status, ERROR_CODES.VALIDATION_ERROR);
    case 401:
      return new ApiError(message || 'Unauthorized', status, ERROR_CODES.UNAUTHORIZED);
    case 403:
      return new ApiError(message || 'Forbidden', status, ERROR_CODES.FORBIDDEN);
    case 404:
      return new ApiError(message || 'Not Found', status, ERROR_CODES.NOT_FOUND);
    case 429:
      return new ApiError(message || 'Too Many Requests', status, ERROR_CODES.RATE_LIMIT);
    case 500:
      return new ApiError(message || 'Internal Server Error', status, ERROR_CODES.SERVER_ERROR);
    case 503:
      return new ApiError(message || 'Service Unavailable', status, ERROR_CODES.API_DOWN);
    default:
      return new ApiError(message || 'Unknown Error', status, ERROR_CODES.UNKNOWN_ERROR);
  }
};

