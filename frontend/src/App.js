import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import ProtectedBusinessRoute from './components/ProtectedBusinessRoute';
import ProtectedAdminRoute from './pages/ProtectedAdminRoute';
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat';
import Simulations from './pages/Simulations';
import Analysis from './pages/Analysis';
import FinancialDataManager from './pages/FinancialDataManager';
import AdminPanel from './pages/AdminPanel';

function App() {
  return (
    <Router>
        <div className="min-h-screen bg-banorte-white">
            <Routes>
              {/* Rutas empresariales protegidas */}
              <Route path="/" element={
                <ProtectedBusinessRoute>
                  <Dashboard />
                </ProtectedBusinessRoute>
              } />
              <Route path="/chat" element={
                <ProtectedBusinessRoute>
                  <Chat />
                </ProtectedBusinessRoute>
              } />
              <Route path="/simulations" element={
                <ProtectedBusinessRoute>
                  <Simulations />
                </ProtectedBusinessRoute>
              } />
              <Route path="/analysis" element={
                <ProtectedBusinessRoute>
                  <Analysis />
                </ProtectedBusinessRoute>
              } />
              <Route path="/data" element={
                <ProtectedBusinessRoute>
                  <FinancialDataManager />
                </ProtectedBusinessRoute>
              } />
              
              {/* Ruta de administración separada */}
              <Route path="/admin" element={<ProtectedAdminRoute />} />
            </Routes>
        <Toaster 
          position="top-right"
          toastOptions={{
            style: {
              background: '#003366',
              color: '#fff',
            },
            success: {
              style: {
                background: '#00AA44',
              },
            },
            error: {
              style: {
                background: '#CC0000',
              },
            },
          }}
        />
      </div>
    </Router>
  );
}

export default App;
