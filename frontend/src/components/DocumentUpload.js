import React, { useState, useEffect } from 'react';
import { documentsAPI } from '../services/api';
import './DocumentUpload.css';

const DocumentUpload = () => {
  const [file, setFile] = useState(null);
  const [documentType, setDocumentType] = useState('');
  const [uploading, setUploading] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [uploadStatus, setUploadStatus] = useState(null);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const response = await documentsAPI.list();
      setDocuments(response.data);
    } catch (error) {
      console.error('Error loading documents:', error);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setUploadStatus(null);
    } else {
      setUploadStatus({ type: 'error', message: 'Please select a PDF file' });
      setFile(null);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setUploadStatus(null);

    try {
      await documentsAPI.upload(file, documentType || null);
      setUploadStatus({
        type: 'success',
        message: 'Document uploaded successfully! Processing...',
      });
      setFile(null);
      setDocumentType('');
      document.getElementById('file-input').value = '';
      
      // Reload documents list
      setTimeout(() => {
        loadDocuments();
      }, 1000);
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: error.response?.data?.detail || 'Error uploading document',
      });
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (documentId) => {
    if (!window.confirm('Are you sure you want to delete this document?')) {
      return;
    }

    try {
      await documentsAPI.delete(documentId);
      loadDocuments();
    } catch (error) {
      alert('Error deleting document: ' + (error.response?.data?.detail || error.message));
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return '#28a745';
      case 'processing':
        return '#ffc107';
      case 'failed':
        return '#dc3545';
      default:
        return '#6c757d';
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-section">
        <h2>Upload Regulatory Documents</h2>
        <p>Upload PDF documents such as GDPR, SOC2, PCI-DSS, or internal policies</p>

        <form onSubmit={handleUpload} className="upload-form">
          <div className="form-group">
            <label htmlFor="file-input">Select PDF File</label>
            <input
              id="file-input"
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              disabled={uploading}
              required
            />
            {file && (
              <div className="file-info">
                Selected: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
              </div>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="document-type">Document Type (Optional)</label>
            <select
              id="document-type"
              value={documentType}
              onChange={(e) => setDocumentType(e.target.value)}
              disabled={uploading}
            >
              <option value="">Select type...</option>
              <option value="GDPR">GDPR</option>
              <option value="SOC2">SOC2</option>
              <option value="PCI-DSS">PCI-DSS</option>
              <option value="Internal Policy">Internal Policy</option>
              <option value="Other">Other</option>
            </select>
          </div>

          {uploadStatus && (
            <div className={`status-message ${uploadStatus.type}`}>
              {uploadStatus.message}
            </div>
          )}

          <button
            type="submit"
            className="upload-button"
            disabled={!file || uploading}
          >
            {uploading ? 'Uploading...' : 'Upload Document'}
          </button>
        </form>
      </div>

      <div className="documents-section">
        <h2>Uploaded Documents</h2>
        {documents.length === 0 ? (
          <p className="no-documents">No documents uploaded yet.</p>
        ) : (
          <div className="documents-list">
            {documents.map((doc) => (
              <div key={doc.id} className="document-card">
                <div className="document-info">
                  <h3>{doc.filename}</h3>
                  <div className="document-meta">
                    <span className="document-type">
                      {doc.document_type || 'Unspecified'}
                    </span>
                    <span
                      className="document-status"
                      style={{ color: getStatusColor(doc.status) }}
                    >
                      {doc.status}
                    </span>
                  </div>
                  <div className="document-details">
                    <span>Chunks: {doc.chunks_count}</span>
                    <span>
                      Uploaded: {new Date(doc.uploaded_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                <button
                  className="delete-button"
                  onClick={() => handleDelete(doc.id)}
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentUpload;
