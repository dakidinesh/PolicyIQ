import React, { useState, useEffect } from 'react';
import { auditAPI } from '../services/api';
import './AuditLogs.css';

const AuditLogs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedLog, setSelectedLog] = useState(null);
  const [filters, setFilters] = useState({
    minConfidence: '',
    startDate: '',
    endDate: '',
  });

  useEffect(() => {
    loadLogs();
  }, []);

  const loadLogs = async () => {
    setLoading(true);
    try {
      const params = {};
      if (filters.minConfidence) {
        params.min_confidence = parseFloat(filters.minConfidence);
      }
      if (filters.startDate) {
        params.start_date = filters.startDate;
      }
      if (filters.endDate) {
        params.end_date = filters.endDate;
      }

      const response = await auditAPI.getLogs(params);
      setLogs(response.data);
    } catch (error) {
      console.error('Error loading audit logs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (field, value) => {
    setFilters((prev) => ({ ...prev, [field]: value }));
  };

  const applyFilters = () => {
    loadLogs();
  };

  const getConfidenceColor = (score) => {
    if (score >= 0.8) return '#28a745';
    if (score >= 0.6) return '#ffc107';
    return '#dc3545';
  };

  return (
    <div className="audit-container">
      <div className="audit-header">
        <h2>Audit Logs</h2>
        <p>View all interactions and their audit trail</p>
      </div>

      <div className="audit-filters">
        <div className="filter-group">
          <label>Min Confidence:</label>
          <input
            type="number"
            min="0"
            max="1"
            step="0.1"
            value={filters.minConfidence}
            onChange={(e) => handleFilterChange('minConfidence', e.target.value)}
            placeholder="0.0 - 1.0"
          />
        </div>
        <div className="filter-group">
          <label>Start Date:</label>
          <input
            type="date"
            value={filters.startDate}
            onChange={(e) => handleFilterChange('startDate', e.target.value)}
          />
        </div>
        <div className="filter-group">
          <label>End Date:</label>
          <input
            type="date"
            value={filters.endDate}
            onChange={(e) => handleFilterChange('endDate', e.target.value)}
          />
        </div>
        <button className="filter-button" onClick={applyFilters}>
          Apply Filters
        </button>
      </div>

      {loading ? (
        <div className="loading">Loading audit logs...</div>
      ) : logs.length === 0 ? (
        <div className="no-logs">No audit logs found.</div>
      ) : (
        <div className="logs-list">
          {logs.map((log) => (
            <div
              key={log.id}
              className="log-card"
              onClick={() => setSelectedLog(selectedLog?.id === log.id ? null : log)}
            >
              <div className="log-header">
                <div className="log-timestamp">
                  {new Date(log.timestamp).toLocaleString()}
                </div>
                <div
                  className="log-confidence"
                  style={{ color: getConfidenceColor(log.confidence_score) }}
                >
                  Confidence: {(log.confidence_score * 100).toFixed(0)}%
                </div>
              </div>
              <div className="log-question">{log.question}</div>
              <div className="log-answer-preview">
                {log.answer.substring(0, 150)}...
              </div>
              {log.manual_review_recommended && (
                <div className="review-badge">⚠️ Manual Review Recommended</div>
              )}

              {selectedLog?.id === log.id && (
                <div className="log-details">
                  <div className="detail-section">
                    <h4>Full Answer:</h4>
                    <p>{log.answer}</p>
                  </div>

                  {log.citations && log.citations.length > 0 && (
                    <div className="detail-section">
                      <h4>Citations:</h4>
                      <ul>
                        {log.citations.map((citation, idx) => (
                          <li key={idx}>
                            {citation.document_name}
                            {citation.section && ` - ${citation.section}`}
                            <span className="citation-score">
                              ({(citation.relevance_score * 100).toFixed(0)}%)
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {log.reasoning_steps && log.reasoning_steps.length > 0 && (
                    <div className="detail-section">
                      <h4>Reasoning Steps:</h4>
                      <ol>
                        {log.reasoning_steps.map((step, idx) => (
                          <li key={idx}>{step}</li>
                        ))}
                      </ol>
                    </div>
                  )}

                  {log.llm_prompt && (
                    <details className="detail-section">
                      <summary>LLM Prompt</summary>
                      <pre>{log.llm_prompt}</pre>
                    </details>
                  )}

                  {log.llm_response && (
                    <details className="detail-section">
                      <summary>LLM Response</summary>
                      <pre>{JSON.stringify(log.llm_response, null, 2)}</pre>
                    </details>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AuditLogs;
