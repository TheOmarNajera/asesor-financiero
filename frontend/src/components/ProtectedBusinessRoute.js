import React, { useState, useEffect } from 'react';
import BusinessLoginForm from './BusinessLoginForm';
import Layout from './Layout';
import Dashboard from '../pages/Dashboard';
import Chat from '../pages/Chat';
import Simulations from '../pages/Simulations';
import Analysis from '../pages/Analysis';
import FinancialDataManager from '../pages/FinancialDataManager';

const ProtectedBusinessRoute = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Verificar si hay un usuario empresarial autenticado
    const savedUser = localStorage.getItem('business_user');
    const token = localStorage.getItem('business_token');
    
    if (savedUser && token) {
      try {
        const userData = JSON.parse(savedUser);
        setUser(userData);
      } catch (error) {
        console.error('Error parsing business user data:', error);
        localStorage.removeItem('business_user');
        localStorage.removeItem('business_token');
      }
    }
    
    setIsLoading(false);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('business_user');
    localStorage.removeItem('business_token');
    setUser(null);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-banorte-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-banorte-primary mx-auto mb-4"></div>
          <p className="text-banorte-primary font-medium">Verificando acceso empresarial...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <BusinessLoginForm onLogin={handleLogin} />;
  }

  // Si está autenticado, mostrar el layout con las páginas empresariales
  return (
    <Layout onLogout={handleLogout} user={user}>
      {children}
    </Layout>
  );
};

export default ProtectedBusinessRoute;
