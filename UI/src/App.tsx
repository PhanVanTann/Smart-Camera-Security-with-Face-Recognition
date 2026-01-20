import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { CameraMonitor } from './pages/CameraMonitor';
import { Residents } from './pages/Residents';


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/camera-monitor" element={<CameraMonitor />} />
        <Route path="/residents" element={<Residents />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
