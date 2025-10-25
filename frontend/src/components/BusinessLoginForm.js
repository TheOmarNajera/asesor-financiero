import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Lock, 
  User, 
  Eye, 
  EyeOff, 
  Building2, 
  AlertCircle,
  CheckCircle,
  Loader2,
  ArrowRight
} from 'lucide-react';
import toast from 'react-hot-toast';
import BanorteLogo from './BanorteLogo';

const BusinessLoginForm = ({ onLogin }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    companyName: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // Simular autenticación empresarial
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Validar credenciales empresariales
      if (formData.email === 'empresa@demo.com' && formData.password === 'empresa123') {
        const user = {
          id: 'emp_1',
          email: formData.email,
          companyName: formData.companyName || 'Empresa Demo',
          name: 'Usuario Empresarial',
          role: 'business',
          token: 'jwt_business_token_here'
        };
        
        localStorage.setItem('business_user', JSON.stringify(user));
        localStorage.setItem('business_token', user.token);
        
        toast.success('¡Bienvenido al Asesor PyME!');
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

  const handleRegister = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // Simular registro empresarial
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const user = {
        id: `emp_${Date.now()}`,
        email: formData.email,
        companyName: formData.companyName,
        name: 'Usuario Empresarial',
        role: 'business',
        token: 'jwt_business_token_here'
      };
      
      localStorage.setItem('business_user', JSON.stringify(user));
      localStorage.setItem('business_token', user.token);
      
      toast.success('¡Empresa registrada exitosamente!');
      onLogin(user);
    } catch (error) {
      toast.error('Error al registrar empresa');
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
            Asesor PyME Inteligente
          </h2>
          <p className="mt-2 text-sm text-banorte-accent">
            {isRegistering ? 'Registra tu empresa' : 'Acceso empresarial'}
          </p>
        </div>

        {/* Formulario */}
        <motion.form 
          className="mt-8 space-y-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          onSubmit={isRegistering ? handleRegister : handleSubmit}
        >
          <div className="card">
            <div className="space-y-6">
              {/* Nombre de la empresa */}
              <div>
                <label htmlFor="companyName" className="block text-sm font-medium text-banorte-dark mb-2">
                  Nombre de la Empresa
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Building2 className="h-5 w-5 text-banorte-accent" />
                  </div>
                  <input
                    id="companyName"
                    name="companyName"
                    type="text"
                    required
                    value={formData.companyName}
                    onChange={handleInputChange}
                    className="input-field pl-10"
                    placeholder="Mi Empresa S.A. de C.V."
                  />
                </div>
              </div>

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
                    placeholder="contacto@miempresa.com"
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
                      <span>{isRegistering ? 'Registrando...' : 'Iniciando sesión...'}</span>
                    </>
                  ) : (
                    <>
                      <ArrowRight className="h-4 w-4" />
                      <span>{isRegistering ? 'Registrar Empresa' : 'Acceder'}</span>
                    </>
                  )}
                </button>
              </div>

              {/* Cambiar entre login y registro */}
              <div className="text-center">
                <button
                  type="button"
                  onClick={() => setIsRegistering(!isRegistering)}
                  className="text-sm text-banorte-primary hover:text-banorte-secondary transition-colors duration-200"
                >
                  {isRegistering 
                    ? '¿Ya tienes cuenta? Inicia sesión' 
                    : '¿Nueva empresa? Regístrate aquí'
                  }
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
                <p className="text-banorte-dark">Email: empresa@demo.com</p>
                <p className="text-banorte-dark">Contraseña: empresa123</p>
                <p className="text-banorte-dark">Empresa: Empresa Demo</p>
              </div>
            </div>
          </div>
        </motion.form>
      </div>
    </div>
  );
};

export default BusinessLoginForm;
