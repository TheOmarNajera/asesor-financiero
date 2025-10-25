import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Users, 
  Shield, 
  Settings, 
  LogOut,
  Plus,
  Edit,
  Trash2,
  Search,
  Filter,
  Download,
  Eye,
  EyeOff,
  CheckCircle,
  XCircle,
  AlertTriangle,
  UserCheck,
  UserX,
  Clock,
  Calendar
} from 'lucide-react';
import toast from 'react-hot-toast';
import BanorteLogo from '../components/BanorteLogo';

const AdminPanel = ({ onLogout }) => {
  const [activeTab, setActiveTab] = useState('users');
  const [users, setUsers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [showAddUser, setShowAddUser] = useState(false);
  const [newUser, setNewUser] = useState({
    name: '',
    email: '',
    role: 'user',
    status: 'active'
  });

  // Datos de ejemplo
  useEffect(() => {
    setUsers([
      {
        id: 1,
        name: 'María González',
        email: 'maria.gonzalez@empresa.com',
        role: 'admin',
        status: 'active',
        lastLogin: '2024-10-25T10:30:00Z',
        createdAt: '2024-01-15T09:00:00Z'
      },
      {
        id: 2,
        name: 'Carlos Rodríguez',
        email: 'carlos.rodriguez@empresa.com',
        role: 'user',
        status: 'active',
        lastLogin: '2024-10-24T16:45:00Z',
        createdAt: '2024-02-20T11:30:00Z'
      },
      {
        id: 3,
        name: 'Ana Martínez',
        email: 'ana.martinez@empresa.com',
        role: 'user',
        status: 'inactive',
        lastLogin: '2024-10-20T14:20:00Z',
        createdAt: '2024-03-10T08:15:00Z'
      },
      {
        id: 4,
        name: 'Luis Hernández',
        email: 'luis.hernandez@empresa.com',
        role: 'user',
        status: 'active',
        lastLogin: '2024-10-25T09:15:00Z',
        createdAt: '2024-04-05T13:45:00Z'
      }
    ]);
  }, []);

  const filteredUsers = users.filter(user =>
    user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleAddUser = () => {
    if (!newUser.name || !newUser.email) {
      toast.error('Por favor completa todos los campos');
      return;
    }

    const user = {
      id: users.length + 1,
      ...newUser,
      lastLogin: null,
      createdAt: new Date().toISOString()
    };

    setUsers([...users, user]);
    setNewUser({ name: '', email: '', role: 'user', status: 'active' });
    setShowAddUser(false);
    toast.success('Usuario agregado exitosamente');
  };

  const handleDeleteUser = (userId) => {
    setUsers(users.filter(user => user.id !== userId));
    toast.success('Usuario eliminado exitosamente');
  };

  const handleToggleStatus = (userId) => {
    setUsers(users.map(user => 
      user.id === userId 
        ? { ...user, status: user.status === 'active' ? 'inactive' : 'active' }
        : user
    ));
    toast.success('Estado del usuario actualizado');
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('es-MX', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'text-green-600 bg-green-100';
      case 'inactive':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getRoleColor = (role) => {
    switch (role) {
      case 'admin':
        return 'text-banorte-primary bg-banorte-primary bg-opacity-10';
      case 'user':
        return 'text-banorte-accent bg-banorte-accent bg-opacity-10';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="min-h-screen bg-banorte-white">
      {/* Header */}
      <div className="bg-banorte-gradient shadow-banorte-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-4">
              <BanorteLogo showText={true} />
              <div>
                <h1 className="text-2xl font-bold text-banorte-white font-display">
                  Panel de Administración
                </h1>
                <p className="text-banorte-white text-opacity-80">
                  Gestión de usuarios y configuración del sistema
                </p>
              </div>
            </div>
            <button
              onClick={onLogout}
              className="btn-secondary flex items-center space-x-2"
            >
              <LogOut className="h-4 w-4" />
              <span>Cerrar Sesión</span>
            </button>
          </div>
        </div>
      </div>

      {/* Navegación de pestañas */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {[
              { id: 'users', name: 'Usuarios', icon: Users },
              { id: 'settings', name: 'Configuración', icon: Settings },
              { id: 'security', name: 'Seguridad', icon: Shield }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-banorte-primary text-banorte-primary'
                    : 'border-transparent text-banorte-accent hover:text-banorte-primary hover:border-gray-300'
                }`}
              >
                <tab.icon className="h-4 w-4" />
                <span>{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Contenido principal */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'users' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            {/* Barra de herramientas */}
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-banorte-accent" />
                  <input
                    type="text"
                    placeholder="Buscar usuarios..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-banorte-primary focus:border-transparent"
                  />
                </div>
                <button className="btn-secondary flex items-center space-x-2">
                  <Filter className="h-4 w-4" />
                  <span>Filtrar</span>
                </button>
              </div>
              <div className="flex items-center space-x-3">
                <button className="btn-secondary flex items-center space-x-2">
                  <Download className="h-4 w-4" />
                  <span>Exportar</span>
                </button>
                <button
                  onClick={() => setShowAddUser(true)}
                  className="btn-primary flex items-center space-x-2"
                >
                  <Plus className="h-4 w-4" />
                  <span>Agregar Usuario</span>
                </button>
              </div>
            </div>

            {/* Tabla de usuarios */}
            <div className="card overflow-hidden">
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-banorte-light">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-banorte-primary uppercase tracking-wider">
                        Usuario
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-banorte-primary uppercase tracking-wider">
                        Rol
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-banorte-primary uppercase tracking-wider">
                        Estado
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-banorte-primary uppercase tracking-wider">
                        Último Acceso
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-banorte-primary uppercase tracking-wider">
                        Acciones
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {filteredUsers.map((user) => (
                      <tr key={user.id} className="hover:bg-banorte-light transition-colors duration-200">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="flex-shrink-0 h-10 w-10">
                              <div className="h-10 w-10 rounded-full bg-banorte-primary bg-opacity-20 flex items-center justify-center">
                                <Users className="h-5 w-5 text-banorte-primary" />
                              </div>
                            </div>
                            <div className="ml-4">
                              <div className="text-sm font-medium text-banorte-dark">
                                {user.name}
                              </div>
                              <div className="text-sm text-banorte-accent">
                                {user.email}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getRoleColor(user.role)}`}>
                            {user.role === 'admin' ? 'Administrador' : 'Usuario'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(user.status)}`}>
                            {user.status === 'active' ? 'Activo' : 'Inactivo'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-banorte-accent">
                          {user.lastLogin ? formatDate(user.lastLogin) : 'Nunca'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <div className="flex items-center space-x-2">
                            <button
                              onClick={() => handleToggleStatus(user.id)}
                              className={`p-1 rounded ${
                                user.status === 'active' 
                                  ? 'text-red-600 hover:bg-red-100' 
                                  : 'text-green-600 hover:bg-green-100'
                              }`}
                              title={user.status === 'active' ? 'Desactivar' : 'Activar'}
                            >
                              {user.status === 'active' ? <UserX className="h-4 w-4" /> : <UserCheck className="h-4 w-4" />}
                            </button>
                            <button className="p-1 rounded text-banorte-primary hover:bg-banorte-primary hover:bg-opacity-10">
                              <Edit className="h-4 w-4" />
                            </button>
                            <button
                              onClick={() => handleDeleteUser(user.id)}
                              className="p-1 rounded text-red-600 hover:bg-red-100"
                            >
                              <Trash2 className="h-4 w-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </motion.div>
        )}

        {activeTab === 'settings' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div className="card">
              <h3 className="text-lg font-semibold text-banorte-primary mb-4">
                Configuración del Sistema
              </h3>
              <p className="text-banorte-accent">
                Panel de configuración en desarrollo...
              </p>
            </div>
          </motion.div>
        )}

        {activeTab === 'security' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div className="card">
              <h3 className="text-lg font-semibold text-banorte-primary mb-4">
                Configuración de Seguridad
              </h3>
              <p className="text-banorte-accent">
                Panel de seguridad en desarrollo...
              </p>
            </div>
          </motion.div>
        )}
      </div>

      {/* Modal para agregar usuario */}
      {showAddUser && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-lg p-6 w-full max-w-md mx-4"
          >
            <h3 className="text-lg font-semibold text-banorte-primary mb-4">
              Agregar Nuevo Usuario
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-banorte-dark mb-1">
                  Nombre Completo
                </label>
                <input
                  type="text"
                  value={newUser.name}
                  onChange={(e) => setNewUser({...newUser, name: e.target.value})}
                  className="input-field"
                  placeholder="Ej. Juan Pérez"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-banorte-dark mb-1">
                  Correo Electrónico
                </label>
                <input
                  type="email"
                  value={newUser.email}
                  onChange={(e) => setNewUser({...newUser, email: e.target.value})}
                  className="input-field"
                  placeholder="juan.perez@empresa.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-banorte-dark mb-1">
                  Rol
                </label>
                <select
                  value={newUser.role}
                  onChange={(e) => setNewUser({...newUser, role: e.target.value})}
                  className="input-field"
                >
                  <option value="user">Usuario</option>
                  <option value="admin">Administrador</option>
                </select>
              </div>
            </div>
            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={() => setShowAddUser(false)}
                className="btn-secondary"
              >
                Cancelar
              </button>
              <button
                onClick={handleAddUser}
                className="btn-primary"
              >
                Agregar Usuario
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default AdminPanel;
