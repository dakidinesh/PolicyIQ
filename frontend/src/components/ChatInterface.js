import React, { useState, useRef, useEffect } from 'react';
import { questionsAPI } from '../services/api';
import './ChatInterface.css';

const ChatInterface = () => {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim() || loading) return;

    const userMessage = {
      type: 'user',
      content: question,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuestion('');
    setLoading(true);

    try {
      const response = await questionsAPI.ask(question);
      const answer = response.data;

      const assistantMessage = {
        type: 'assistant',
        content: answer.answer,
        explanation: answer.explanation,
        citations: answer.citations,
        confidenceScore: answer.confidence_score,
        manualReviewRecommended: answer.manual_review_recommended,
        reasoningSteps: answer.reasoning_steps,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        type: 'error',
        content: error.response?.data?.detail || 'An error occurred while processing your question.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>Ask a Compliance Question</h2>
        <p>Get answers from your regulatory documents with cited sources</p>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h3>Welcome to PolicyIQ</h3>
            <p>Ask questions about your regulatory documents, such as:</p>
            <ul>
              <li>"Does policy allow storing customer data outside the US?"</li>
              <li>"What does PCI-DSS require for cardholder encryption?"</li>
              <li>"What are the GDPR requirements for data breach notification?"</li>
            </ul>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.type}`}>
            {msg.type === 'user' && (
              <div className="message-content">
                <div className="message-header">
                  <strong>You</strong>
                  <span className="message-time">
                    {msg.timestamp.toLocaleTimeString()}
                  </span>
                </div>
                <div className="message-text">{msg.content}</div>
              </div>
            )}

            {msg.type === 'assistant' && (
              <div className="message-content">
                <div className="message-header">
                  <strong>PolicyIQ</strong>
                  <span className="message-time">
                    {msg.timestamp.toLocaleTimeString()}
                  </span>
                </div>
                <div className="message-text">{msg.content}</div>
                
                {msg.explanation && (
                  <div className="explanation">
                    <strong>Explanation:</strong> {msg.explanation}
                  </div>
                )}

                <div className="confidence-badge">
                  <span className={`confidence confidence-${getConfidenceLevel(msg.confidenceScore)}`}>
                    Confidence: {(msg.confidenceScore * 100).toFixed(0)}%
                  </span>
                  {msg.manualReviewRecommended && (
                    <span className="review-flag">⚠️ Manual Review Recommended</span>
                  )}
                </div>

                {msg.citations && msg.citations.length > 0 && (
                  <div className="citations">
                    <strong>Citations:</strong>
                    <ul>
                      {msg.citations.map((citation, cIdx) => (
                        <li key={cIdx}>
                          <span className="citation-doc">{citation.document_name}</span>
                          {citation.section && (
                            <span className="citation-section"> - Section: {citation.section}</span>
                          )}
                          <span className="citation-score">
                            (Relevance: {(citation.relevance_score * 100).toFixed(0)}%)
                          </span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {msg.reasoningSteps && msg.reasoningSteps.length > 0 && (
                  <details className="reasoning-steps">
                    <summary>Reasoning Steps</summary>
                    <ul>
                      {msg.reasoningSteps.map((step, sIdx) => (
                        <li key={sIdx}>{step}</li>
                      ))}
                    </ul>
                  </details>
                )}
              </div>
            )}

            {msg.type === 'error' && (
              <div className="message-content error">
                <div className="message-text">{msg.content}</div>
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="message assistant">
            <div className="message-content">
              <div className="loading">Processing your question...</div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about your regulatory documents..."
          className="chat-input"
          disabled={loading}
        />
        <button type="submit" className="chat-submit" disabled={loading || !question.trim()}>
          Send
        </button>
      </form>
    </div>
  );
};

const getConfidenceLevel = (score) => {
  if (score >= 0.8) return 'high';
  if (score >= 0.6) return 'medium';
  return 'low';
};

export default ChatInterface;
