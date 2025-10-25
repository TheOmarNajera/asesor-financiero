import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Calculator, 
  Plus, 
  Play, 
  AlertTriangle,
  CheckCircle,
  Clock,
  Brain
} from 'lucide-react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import toast from 'react-hot-toast';
import api from '../services/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Simulations = () => {
  const [simulations, setSimulations] = useState([]);
  const [currentSimulation, setCurrentSimulation] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [newScenario, setNewScenario] = useState({
    name: '',
    description: '',
    parameters: {
      revenue_change_percent: 0,
      expense_change_percent: 0,
      new_monthly_expense: 0,
      revenue_growth_rate: 0
    },
    duration_months: 12
  });

  useEffect(() => {
    loadSimulations();
  }, []);

  const loadSimulations = async () => {
    try {
      const response = await api.get('/api/simulations/history');
      setSimulations(response.data);
    } catch (error) {
      console.error('Error cargando simulaciones:', error);
    }
  };

  const createSimulation = async () => {
    if (!newScenario.name.trim()) {
      toast.error('Por favor ingresa un nombre para la simulación');
      return;
    }

    setIsRunning(true);
    try {
      const response = await api.post('/api/simulations/scenario', {
        scenario: newScenario,
        base_data_period: 'last_12_months',
        include_recommendations: true
      });

      setCurrentSimulation(response.data);
      toast.success('Simulación completada exitosamente');
      
      // Reset form
      setNewScenario({
        name: '',
        description: '',
        parameters: {
          revenue_change_percent: 0,
          expense_change_percent: 0,
          new_monthly_expense: 0,
          revenue_growth_rate: 0
        },
        duration_months: 12
      });
      setIsCreating(false);
      
    } catch (error) {
      console.error('Error ejecutando simulación:', error);
      toast.error('Error al ejecutar la simulación');
    } finally {
      setIsRunning(false);
    }
  };

  const loadSimulationResult = async (simulationId) => {
    try {
      const response = await api.get(`/api/simulations/${simulationId}`);
      setCurrentSimulation(response.data);
    } catch (error) {
      console.error('Error cargando resultado:', error);
      toast.error('Error al cargar el resultado');
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency: 'MXN'
    }).format(amount);
  };

  const getRiskColor = (risk) => {
    if (!risk) return 'text-banorte-primary bg-banorte-primary bg-opacity-10';
    switch (risk.toLowerCase()) {
      case 'alto':
        return 'text-banorte-danger bg-banorte-danger bg-opacity-10';
      case 'medio':
        return 'text-banorte-warning bg-banorte-warning bg-opacity-10';
      case 'bajo':
        return 'text-banorte-success bg-banorte-success bg-opacity-10';
      default:
        return 'text-banorte-primary bg-banorte-primary bg-opacity-10';
    }
  };

  const getRiskIcon = (risk) => {
    if (!risk) return <AlertTriangle className="h-4 w-4" />;
    switch (risk.toLowerCase()) {
      case 'alto':
        return <AlertTriangle className="h-4 w-4" />;
      case 'medio':
        return <Clock className="h-4 w-4" />;
      case 'bajo':
        return <CheckCircle className="h-4 w-4" />;
      default:
        return <AlertTriangle className="h-4 w-4" />;
    }
  };

  // Preparar datos para gráfico
  const chartData = currentSimulation ? {
    labels: currentSimulation.projected_cash_flow?.map(item => item.period) || [],
    datasets: [
      {
        label: 'Flujo de Caja Proyectado',
        data: currentSimulation.projected_cash_flow?.map(item => item.net_cash_flow) || [],
        borderColor: '#003366',
        backgroundColor: 'rgba(0, 51, 102, 0.1)',
        tension: 0.4,
      },
      {
        label: 'Balance Acumulado',
        data: currentSimulation.projected_cash_flow?.map(item => item.cumulative_balance) || [],
        borderColor: '#00AA44',
        backgroundColor: 'rgba(0, 170, 68, 0.1)',
        tension: 0.4,
      },
    ],
  } : null;

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return formatCurrency(value);
          }
        }
      }
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-banorte-primary font-display">Simulaciones What-If</h1>
          <p className="text-banorte-secondary mt-2 text-lg">Proyecta escenarios futuros y evalúa decisiones financieras</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-sm text-banorte-primary">
            <Brain className="h-4 w-4" />
            <span>IA Predictiva</span>
          </div>
          <div className="flex items-center space-x-2 text-sm text-banorte-primary">
            <div className="w-2 h-2 bg-banorte-success rounded-full animate-pulse"></div>
            <span>Sistema Activo</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Crear Nueva Simulación */}
        <div className="lg:col-span-1">
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Nueva Simulación</h3>
              <button
                onClick={() => setIsCreating(!isCreating)}
                className="btn-primary flex items-center space-x-2"
              >
                <Plus className="h-4 w-4" />
                <span>Crear</span>
              </button>
            </div>

            {isCreating && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="space-y-4"
              >
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nombre del Escenario
                  </label>
                  <input
                    type="text"
                    value={newScenario.name}
                    onChange={(e) => setNewScenario({...newScenario, name: e.target.value})}
                    className="input-field"
                    placeholder="Ej: Contratación de empleado"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Descripción
                  </label>
                  <textarea
                    value={newScenario.description}
                    onChange={(e) => setNewScenario({...newScenario, description: e.target.value})}
                    className="input-field"
                    rows={3}
                    placeholder="Describe el escenario a simular..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Cambio en Ingresos (%)
                  </label>
                  <input
                    type="number"
                    value={newScenario.parameters.revenue_change_percent}
                    onChange={(e) => setNewScenario({
                      ...newScenario, 
                      parameters: {...newScenario.parameters, revenue_change_percent: parseFloat(e.target.value)}
                    })}
                    className="input-field"
                    step="0.1"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Cambio en Gastos (%)
                  </label>
                  <input
                    type="number"
                    value={newScenario.parameters.expense_change_percent}
                    onChange={(e) => setNewScenario({
                      ...newScenario, 
                      parameters: {...newScenario.parameters, expense_change_percent: parseFloat(e.target.value)}
                    })}
                    className="input-field"
                    step="0.1"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nuevo Gasto Mensual ($)
                  </label>
                  <input
                    type="number"
                    value={newScenario.parameters.new_monthly_expense}
                    onChange={(e) => setNewScenario({
                      ...newScenario, 
                      parameters: {...newScenario.parameters, new_monthly_expense: parseFloat(e.target.value)}
                    })}
                    className="input-field"
                    step="100"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Duración (meses)
                  </label>
                  <input
                    type="number"
                    value={newScenario.duration_months}
                    onChange={(e) => setNewScenario({...newScenario, duration_months: parseInt(e.target.value)})}
                    className="input-field"
                    min="1"
                    max="24"
                  />
                </div>

                <button
                  onClick={createSimulation}
                  disabled={isRunning}
                  className="w-full btn-primary flex items-center justify-center space-x-2 disabled:opacity-50"
                >
                  {isRunning ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      <span>Ejecutando...</span>
                    </>
                  ) : (
                    <>
                      <Play className="h-4 w-4" />
                      <span>Ejecutar Simulación</span>
                    </>
                  )}
                </button>
              </motion.div>
            )}

            {/* Simulaciones Previas */}
            <div className="mt-6">
              <h4 className="text-md font-semibold text-gray-900 mb-3">Simulaciones Previas</h4>
              <div className="space-y-2">
                {simulations.map((sim) => (
                  <button
                    key={sim.id}
                    onClick={() => loadSimulationResult(sim.id)}
                    className="w-full text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors duration-200"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-900">{sim.name}</p>
                        <p className="text-xs text-gray-500">{sim.created_at}</p>
                      </div>
                      <div className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(sim.risk_level)}`}>
                        {sim.risk_level}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Resultados de Simulación */}
        <div className="lg:col-span-2">
          {currentSimulation ? (
            <div className="space-y-6">
              {/* Header del Resultado */}
              <div className="card">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900">{currentSimulation.name || 'Simulación'}</h3>
                    <p className="text-gray-600">Resultados de la simulación</p>
                  </div>
                  <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(currentSimulation.risk_level)}`}>
                    {getRiskIcon(currentSimulation.risk_level)}
                    <span>{currentSimulation.risk_level || 'No evaluado'}</span>
                  </div>
                </div>

                {/* Métricas Clave */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <p className="text-sm text-gray-600">Ingresos Proyectados</p>
                    <p className="text-lg font-semibold text-gray-900">
                      {formatCurrency(currentSimulation.key_metrics?.total_projected_income || 0)}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-600">Gastos Proyectados</p>
                    <p className="text-lg font-semibold text-gray-900">
                      {formatCurrency(currentSimulation.key_metrics?.total_projected_expenses || 0)}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-600">Flujo Neto</p>
                    <p className={`text-lg font-semibold ${
                      (currentSimulation.key_metrics?.net_projected_cash_flow || 0) >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {formatCurrency(currentSimulation.key_metrics?.net_projected_cash_flow || 0)}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-600">Balance Final</p>
                    <p className={`text-lg font-semibold ${
                      (currentSimulation.key_metrics?.final_balance || 0) >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {formatCurrency(currentSimulation.key_metrics?.final_balance || 0)}
                    </p>
                  </div>
                </div>
              </div>

              {/* Gráfico de Proyección */}
              <div className="card">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">Proyección de Flujo de Caja</h4>
                <div className="h-64">
                  <Line data={chartData} options={chartOptions} />
                </div>
              </div>

              {/* Recomendaciones */}
              <div className="card">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">Recomendaciones</h4>
                <div className="space-y-3">
                  {currentSimulation.recommendations?.map((rec, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                      <CheckCircle className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                      <p className="text-sm text-gray-700">{rec}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="card h-96 flex items-center justify-center">
              <div className="text-center">
                <Calculator className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">No hay simulación activa</h3>
                <p className="text-gray-600">Crea una nueva simulación o selecciona una anterior para ver los resultados</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Simulations;
