import axios from 'axios';

// Create an axios instance with correct baseURL
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  timeout: 30000, // Increase timeout for visualizations
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add request/response interceptors for debugging
api.interceptors.request.use(
  config => {
    console.log('API Request:', config);
    return config;
  },
  error => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  response => {
    console.log('API Response:', response);
    return response;
  },
  error => {
    console.error('API Response Error:', error);
    return Promise.reject(error);
  }
);

// Function to generate visualization
export const generateVisualization = async (code, language) => {
  try {
    console.log(`Sending ${language} code to API:`, code);
    const response = await api.post('/api/visualize', { code, language });
    return response.data;
  } catch (error) {
    console.error('Error generating visualization:', error);
    // Return a more detailed error object
    return {
      error: error.message,
      details: error.response ? error.response.data : 'No response from server'
    };
  }
};

export default api;