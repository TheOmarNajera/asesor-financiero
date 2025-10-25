import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Lock, 
  User, 
  Eye, 
  EyeOff, 
  Shield, 
  AlertCircle,
  CheckCircle,
  Loader2
} from 'lucide-react';
import toast from 'react-hot-toast';
import BanorteLogo from './BanorteLogo';

const LoginForm = ({ onLogin }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // Simular autenticación
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Validar credenciales (en producción sería con API real)
      if (formData.email === 'admin@banorte.com' && formData.password === 'admin123') {
        const user = {
          id: '1',
          email: formData.email,
          name: 'Administrador Banorte',
          role: 'admin',
          token: 'jwt_token_here'
        };
        
        localStorage.setItem('user', JSON.stringify(user));
        localStorage.setItem('token', user.token);
        
        toast.success('¡Bienvenido al panel de administración!');
        onLogin(user);
      } else {
        toast.error('Credenciales incorrectas');
      }
    } catch (error) {
      toast.error('Error al iniciar sesión');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen bg-banorte-white flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <BanorteLogo className="mx-auto h-16 w-auto" />
          <h2 className="mt-6 text-3xl font-bold text-banorte-primary font-display">
            Panel de Administración
          </h2>
          <p className="mt-2 text-sm text-banorte-accent">
            Acceso seguro para administradores
          </p>
        </div>

        {/* Formulario */}
        <motion.form 
          className="mt-8 space-y-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          onSubmit={handleSubmit}
        >
          <div className="card">
            <div className="space-y-6">
              {/* Email */}
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-banorte-dark mb-2">
                  Correo Electrónico
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <User className="h-5 w-5 text-banorte-accent" />
                  </div>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    required
                    value={formData.email}
                    onChange={handleInputChange}
                    className="input-field pl-10"
                    placeholder="admin@banorte.com"
                  />
                </div>
              </div>

              {/* Password */}
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-banorte-dark mb-2">
                  Contraseña
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-banorte-accent" />
                  </div>
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={formData.password}
                    onChange={handleInputChange}
                    className="input-field pl-10 pr-10"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5 text-banorte-accent" />
                    ) : (
                      <Eye className="h-5 w-5 text-banorte-accent" />
                    )}
                  </button>
                </div>
              </div>

              {/* Botón de envío */}
              <div>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="btn-primary w-full flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span>Iniciando sesión...</span>
                    </>
                  ) : (
                    <>
                      <Shield className="h-4 w-4" />
                      <span>Acceder</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Credenciales de prueba */}
          <div className="bg-banorte-light p-4 rounded-lg border border-banorte-primary border-opacity-20">
            <div className="flex items-start space-x-3">
              <AlertCircle className="h-5 w-5 text-banorte-primary mt-0.5 flex-shrink-0" />
              <div className="text-sm">
                <p className="font-medium text-banorte-primary mb-1">Credenciales de prueba:</p>
                <p className="text-banorte-dark">Email: admin@banorte.com</p>
                <p className="text-banorte-dark">Contraseña: admin123</p>
              </div>
            </div>
          </div>
        </motion.form>
      </div>
    </div>
  );
};

export default LoginForm;
