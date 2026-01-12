import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ChatInterface from './components/ChatInterface';
import DocumentUpload from './components/DocumentUpload';
import AuditLogs from './components/AuditLogs';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="nav-container">
            <h1 className="nav-title">PolicyIQ</h1>
            <div className="nav-links">
              <Link to="/" className="nav-link">Chat</Link>
              <Link to="/upload" className="nav-link">Upload</Link>
              <Link to="/audit" className="nav-link">Audit Logs</Link>
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<ChatInterface />} />
            <Route path="/upload" element={<DocumentUpload />} />
            <Route path="/audit" element={<AuditLogs />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
