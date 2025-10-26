import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  DollarSign, 
  TrendingUp, 
  TrendingDown, 
  AlertCircle,
  ArrowUpRight,
  ArrowDownRight,
  Activity,
  RefreshCw,
  Zap,
  Target,
  Shield
} from 'lucide-react';
import { Line, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import api from '../services/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [cashFlowData, setCashFlowData] = useState(null);
  const [expenseData, setExpenseData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Cargar métricas principales
      const profitabilityResponse = await api.get('/api/analysis/profitability');
      setMetrics(profitabilityResponse.data);
      
      // Cargar datos de flujo de caja
      const cashFlowResponse = await api.get('/api/analysis/cashflow');
      setCashFlowData(cashFlowResponse.data);
      
      // Cargar datos de gastos
      const expenseResponse = await api.get('/api/analysis/expenses');
      setExpenseData(expenseResponse.data);
      
    } catch (error) {
      console.error('Error cargando datos del dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency: 'MXN'
    }).format(amount);
  };

  const formatPercentage = (value) => {
    return `${value.toFixed(1)}%`;
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'positive':
        return <ArrowUpRight className="h-5 w-5 text-financial-income" />;
      case 'negative':
        return <ArrowDownRight className="h-5 w-5 text-financial-expense" />;
      default:
        return <Activity className="h-5 w-5 text-banorte-primary" />;
    }
  };

  const getTrendColor = (trend) => {
    switch (trend) {
      case 'positive':
        return 'text-financial-income';
      case 'negative':
        return 'text-financial-expense';
      default:
        return 'text-banorte-primary';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-banorte-primary mx-auto mb-4"></div>
          <p className="text-banorte-primary font-medium">Cargando datos financieros...</p>
        </div>
      </div>
    );
  }

  // Preparar datos para gráficos
  const cashFlowChartData = {
    labels: cashFlowData?.monthly_data?.map(item => item.period) || [],
    datasets: [
      {
        label: 'Flujo de Caja Neto',
        data: cashFlowData?.monthly_data?.map(item => item.net_cash_flow) || [],
        borderColor: '#003366',
        backgroundColor: 'rgba(0, 51, 102, 0.1)',
        tension: 0.4,
        fill: true,
      },
    ],
  };

  const expenseChartData = {
    labels: Object.keys(expenseData?.category_breakdown || {}),
    datasets: [
      {
        label: 'Gastos por Categoría',
        data: Object.values(expenseData?.category_breakdown || {}),
        backgroundColor: [
          '#003366',
          '#0066CC',
          '#FF6600',
          '#00AA44',
          '#CC0000',
          '#FF9900',
        ],
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          font: {
            family: 'Inter',
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return formatCurrency(value);
          },
          font: {
            family: 'Inter',
          },
        },
        grid: {
          color: 'rgba(0, 51, 102, 0.1)',
        },
      },
      x: {
        ticks: {
          font: {
            family: 'Inter',
          },
        },
        grid: {
          color: 'rgba(0, 51, 102, 0.1)',
        },
      },
    },
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-banorte-primary font-display">Dashboard Financiero</h1>
          <p className="text-banorte-secondary mt-2 text-lg">Resumen de tu situación financiera actual</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-sm text-banorte-primary">
            <div className="w-2 h-2 bg-banorte-success rounded-full animate-pulse"></div>
            <span>Datos actualizados</span>
          </div>
          <button
            onClick={loadDashboardData}
            className="btn-secondary flex items-center space-x-2"
          >
            <RefreshCw className="h-4 w-4" />
            <span>Actualizar</span>
          </button>
        </div>
      </div>

      {/* Métricas principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="metric-card metric-card-income"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-financial-income mb-1">Ingresos Totales</p>
              <p className="text-xl font-bold text-financial-income">
                {formatCurrency(metrics?.total_revenue || 0)}
              </p>
            </div>
            <div className="w-12 h-12 bg-financial-income bg-opacity-20 rounded-lg flex items-center justify-center">
              <DollarSign className="h-6 w-6 text-financial-income" />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="metric-card metric-card-expense"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-financial-expense mb-1">Gastos Totales</p>
              <p className="text-xl font-bold text-financial-expense">
                {formatCurrency(metrics?.total_expenses || 0)}
              </p>
            </div>
            <div className="w-12 h-12 bg-financial-expense bg-opacity-20 rounded-lg flex items-center justify-center">
              <TrendingDown className="h-6 w-6 text-financial-expense" />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="metric-card metric-card-profit"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-financial-profit mb-1">Ganancia Neta</p>
              <p className="text-xl font-bold text-financial-profit">
                {formatCurrency(metrics?.net_profit || 0)}
              </p>
            </div>
            <div className="w-12 h-12 bg-financial-profit bg-opacity-20 rounded-lg flex items-center justify-center">
              <TrendingUp className="h-6 w-6 text-financial-profit" />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="metric-card"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-banorte-primary mb-1">Margen de Ganancia</p>
              <p className="text-xl font-bold text-banorte-primary">
                {formatPercentage(metrics?.profit_margin || 0)}
              </p>
            </div>
            <div className="flex items-center space-x-1">
              {getTrendIcon(metrics?.cash_flow_trend)}
              <span className={`text-sm font-medium ${getTrendColor(metrics?.cash_flow_trend)}`}>
                {metrics?.cash_flow_trend === 'positive' ? 'Positiva' : 
                 metrics?.cash_flow_trend === 'negative' ? 'Negativa' : 'Estable'}
              </span>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Gráficos */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Flujo de Caja */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="card"
        >
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-xl font-semibold text-banorte-primary font-display">Flujo de Caja</h3>
              <p className="text-banorte-secondary text-sm">Últimos 12 meses</p>
            </div>
            <div className="flex items-center space-x-2 text-sm text-banorte-primary">
              <div className="w-2 h-2 bg-banorte-primary rounded-full"></div>
              <span>Tendencia {cashFlowData?.trend === 'positive' ? 'Positiva' : 
                         cashFlowData?.trend === 'negative' ? 'Negativa' : 'Estable'}</span>
            </div>
          </div>
          <div className="h-80">
            <Line data={cashFlowChartData} options={chartOptions} />
          </div>
          <div className="mt-6 grid grid-cols-2 gap-4 text-sm">
            <div className="bg-banorte-light p-3 rounded-lg">
              <p className="text-banorte-secondary">Flujo promedio mensual</p>
              <p className="font-semibold text-banorte-primary">{formatCurrency(cashFlowData?.average_monthly_flow || 0)}</p>
            </div>
            <div className="bg-banorte-light p-3 rounded-lg">
              <p className="text-banorte-secondary">Total período</p>
              <p className="font-semibold text-banorte-primary">{formatCurrency(cashFlowData?.net_cash_flow || 0)}</p>
            </div>
          </div>
        </motion.div>

        {/* Gastos por Categoría */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
          className="card"
        >
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-xl font-semibold text-banorte-primary font-display">Gastos por Categoría</h3>
              <p className="text-banorte-secondary text-sm">Distribución actual</p>
            </div>
            <div className="flex items-center space-x-2 text-sm text-banorte-primary">
              <div className="w-2 h-2 bg-banorte-accent rounded-full"></div>
              <span>{Object.keys(expenseData?.category_breakdown || {}).length} categorías</span>
            </div>
          </div>
          <div className="h-80">
            <Doughnut data={expenseChartData} options={{
              responsive: true,
              plugins: {
                legend: {
                  position: 'bottom',
                  labels: {
                    usePointStyle: true,
                    font: {
                      family: 'Inter',
                    },
                  },
                },
              },
            }} />
          </div>
          <div className="mt-6 grid grid-cols-2 gap-4 text-sm">
            <div className="bg-banorte-light p-3 rounded-lg">
              <p className="text-banorte-secondary">Total de gastos</p>
              <p className="font-semibold text-banorte-primary">{formatCurrency(expenseData?.total_expenses || 0)}</p>
            </div>
            <div className="bg-banorte-light p-3 rounded-lg">
              <p className="text-banorte-secondary">Categorías principales</p>
              <p className="font-semibold text-banorte-primary">{expenseData?.top_categories?.length || 0}</p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Insights y Alertas */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
        className="card"
      >
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-10 h-10 bg-banorte-primary bg-opacity-20 rounded-lg flex items-center justify-center">
            <Target className="h-5 w-5 text-banorte-primary" />
          </div>
          <div>
            <h3 className="text-xl font-semibold text-banorte-primary font-display">Insights y Recomendaciones</h3>
            <p className="text-banorte-secondary text-sm">Análisis inteligente de tu situación financiera</p>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {cashFlowData?.insights?.map((insight, index) => (
            <div key={index} className="flex items-start space-x-3 p-4 bg-banorte-light rounded-lg border-l-4 border-banorte-primary">
              <AlertCircle className="h-5 w-5 text-banorte-primary mt-0.5 flex-shrink-0" />
              <p className="text-sm text-banorte-dark">{insight}</p>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Estado del Sistema */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="card-banorte"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-white bg-opacity-20 rounded-lg flex items-center justify-center">
              <Shield className="h-5 w-5 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-semibold text-black font-display">Estado del Sistema</h3>
              <p className="text-black text-sm">Todos los servicios funcionando correctamente</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Zap className="h-4 w-4 text-white" />
              <span className="text-black text-sm">Azure Arm</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-banorte-success rounded-full animate-pulse"></div>
              <span className="text-white text-sm">Online</span>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;
