import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Calculator, 
  TrendingUp,
  Building2,
  Menu,
  X,
  Home,
  Brain,
  Zap,
  Shield,
  Users
} from 'lucide-react';
import { useState } from 'react';
import BanorteLogo from './BanorteLogo';

const Layout = ({ children, onLogout, user }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/', icon: Home },
    { name: 'Chat Inteligente', href: '/chat', icon: Brain },
    { name: 'Simulaciones', href: '/simulations', icon: Calculator },
    { name: 'Análisis', href: '/analysis', icon: TrendingUp },
    { name: 'Mis Datos', href: '/data', icon: Building2 },
  ];

  return (
        <div className="flex h-screen bg-banorte-white">
      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-72 bg-white shadow-banorte-lg transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0`}>
        {/* Header del Sidebar */}
        <div className="flex items-center justify-between h-20 px-6 border-b border-gray-200 bg-banorte-gradient">
          <BanorteLogo showText={true} />
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden p-2 rounded-md text-banorte-white hover:bg-banorte-white hover:bg-opacity-20 transition-colors duration-200"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        {/* Navegación */}
        <nav className="mt-8 px-4">
          <ul className="space-y-2">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <li key={item.name}>
                  <Link
                    to={item.href}
                    className={`sidebar-item ${isActive ? 'sidebar-item-active' : ''}`}
                    onClick={() => setSidebarOpen(false)}
                  >
                    <item.icon className="h-5 w-5 mr-3" />
                    {item.name}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

            {/* Información del usuario */}
            {user && (
              <div className="mt-8 px-4">
                <div className="bg-banorte-light p-4 rounded-lg border border-gray-200">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-banorte-primary rounded-full flex items-center justify-center">
                      <Building2 className="h-5 w-5 text-white" />
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-banorte-primary">Empresa: {user.empresa_id || user.id}</p>
                      <p className="text-xs text-banorte-accent">Sesión activa</p>
                    </div>
                  </div>
                  <button
                    onClick={onLogout}
                    className="w-full mt-3 text-xs text-banorte-primary hover:text-banorte-secondary transition-colors duration-200"
                  >
                    Cerrar Sesión
                  </button>
                </div>
              </div>
            )}

            {/* Footer del Sidebar */}
            <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200 bg-banorte-light">
              <div className="flex items-center space-x-2 text-xs text-banorte-primary">
                <Zap className="h-4 w-4" />
                <div>
                  <p className="font-medium">Powered by Azure Arm</p>
                  <p className="text-gray-500">Hack Mty 2025</p>
                </div>
              </div>
            </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden lg:ml-0">
        {/* Top bar */}
        <header className="bg-white shadow-sm border-b border-gray-200 lg:hidden">
          <div className="flex items-center justify-between h-16 px-4">
            <button
              onClick={() => setSidebarOpen(true)}
              className="p-2 rounded-md text-banorte-primary hover:bg-banorte-light transition-colors duration-200"
            >
              <Menu className="h-6 w-6" />
            </button>
            <div className="flex items-center space-x-3">
              <Building2 className="h-8 w-8 text-banorte-primary" />
              <h1 className="text-xl font-bold text-banorte-primary font-display">Asesor PyME</h1>
            </div>
            <div className="w-10"></div>
          </div>
        </header>

            {/* Page content */}
            <main className="flex-1 overflow-x-hidden overflow-y-auto bg-banorte-white custom-scrollbar">
          <div className="container mx-auto px-6 py-8">
            {children}
          </div>
        </main>
      </div>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
};

export default Layout;
