import React, { useState, useEffect } from 'react';
import LoginForm from '../components/LoginForm';
import AdminPanel from './AdminPanel';

const ProtectedAdminRoute = () => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Verificar si hay un usuario autenticado
    const savedUser = localStorage.getItem('user');
    const token = localStorage.getItem('token');
    
    if (savedUser && token) {
      try {
        const userData = JSON.parse(savedUser);
        setUser(userData);
      } catch (error) {
        console.error('Error parsing user data:', error);
        localStorage.removeItem('user');
        localStorage.removeItem('token');
      }
    }
    
    setIsLoading(false);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    setUser(null);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-banorte-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-banorte-primary mx-auto mb-4"></div>
          <p className="text-banorte-primary font-medium">Verificando acceso...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <LoginForm onLogin={handleLogin} />;
  }

  return <AdminPanel onLogout={handleLogout} />;
};

export default ProtectedAdminRoute;
