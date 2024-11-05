import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import Upload from './components/Upload'; // This should be your upload component
import Chat from './components/Chat';

const App = () => {
  return (
      <Router>
          <Routes>
              <Route path="/" element={<Upload />} />
              <Route path="/chat/:documentId" element={<Chat />} />
          </Routes>
      </Router>
  );
};

export default App;