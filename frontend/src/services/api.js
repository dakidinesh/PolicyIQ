import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Documents API
export const documentsAPI = {
  upload: async (file, documentType = null) => {
    const formData = new FormData();
    formData.append('file', file);
    if (documentType) {
      formData.append('document_type', documentType);
    }
    return api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  list: async () => {
    return api.get('/documents/');
  },

  get: async (documentId) => {
    return api.get(`/documents/${documentId}`);
  },

  delete: async (documentId) => {
    return api.delete(`/documents/${documentId}`);
  },
};

// Questions API
export const questionsAPI = {
  ask: async (question, context = null) => {
    return api.post('/questions/ask', {
      question,
      context,
    });
  },
};

// Audit API
export const auditAPI = {
  getLogs: async (filters = {}) => {
    return api.get('/audit/logs', { params: filters });
  },

  getLog: async (logId) => {
    return api.get(`/audit/logs/${logId}`);
  },
};

export default api;
