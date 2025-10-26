import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown, 
  DollarSign,
  PieChart,
  Activity,
  AlertCircle,
  CheckCircle,
  RefreshCw
} from 'lucide-react';
import { Bar, Line, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import toast from 'react-hot-toast';
import api from '../services/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const Analysis = () => {
  const [analysisData, setAnalysisData] = useState({
    profitability: null,
    cashflow: null,
    expenses: null,
    revenue: null
  });
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    loadAnalysisData();
  }, []);

  const loadAnalysisData = async () => {
    try {
      setLoading(true);
      
      const [profitabilityRes, cashflowRes, expensesRes, revenueRes] = await Promise.all([
        api.get('/api/analysis/profitability'),
        api.get('/api/analysis/cashflow'),
        api.get('/api/analysis/expenses'),
        api.get('/api/analysis/revenue')
      ]);

      setAnalysisData({
        profitability: profitabilityRes.data,
        cashflow: cashflowRes.data,
        expenses: expensesRes.data,
        revenue: revenueRes.data
      });
      
    } catch (error) {
      console.error('Error cargando análisis:', error);
      toast.error('Error al cargar datos de análisis');
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
        return <TrendingUp className="h-5 w-5 text-green-500" />;
      case 'negative':
        return <TrendingDown className="h-5 w-5 text-red-500" />;
      default:
        return <Activity className="h-5 w-5 text-gray-500" />;
    }
  };

  const tabs = [
    { id: 'overview', name: 'Resumen General', icon: BarChart3 },
    { id: 'cashflow', name: 'Flujo de Caja', icon: Activity },
    { id: 'expenses', name: 'Gastos', icon: TrendingDown },
    { id: 'revenue', name: 'Ingresos', icon: TrendingUp },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  // Preparar datos para gráficos
  const cashFlowChartData = {
    labels: analysisData.cashflow?.monthly_data?.map(item => item.period) || [],
    datasets: [
      {
        label: 'Ingresos',
        data: analysisData.cashflow?.monthly_data?.map(item => item.income) || [],
        backgroundColor: 'rgba(16, 185, 129, 0.8)',
      },
      {
        label: 'Gastos',
        data: analysisData.cashflow?.monthly_data?.map(item => item.expenses) || [],
        backgroundColor: 'rgba(239, 68, 68, 0.8)',
      },
      {
        label: 'Flujo Neto',
        data: analysisData.cashflow?.monthly_data?.map(item => item.net_cash_flow) || [],
        backgroundColor: 'rgba(59, 130, 246, 0.8)',
      },
    ],
  };

  const expenseChartData = {
    labels: Object.keys(analysisData.expenses?.category_breakdown || {}),
    datasets: [
      {
        label: 'Gastos por Categoría',
        data: Object.values(analysisData.expenses?.category_breakdown || {}),
        backgroundColor: [
          'rgba(59, 130, 246, 0.8)',
          'rgba(16, 185, 129, 0.8)',
          'rgba(245, 158, 11, 0.8)',
          'rgba(239, 68, 68, 0.8)',
          'rgba(139, 92, 246, 0.8)',
        ],
      },
    ],
  };

  const revenueChartData = {
    labels: Object.keys(analysisData.revenue?.category_breakdown || {}),
    datasets: [
      {
        label: 'Ingresos por Categoría',
        data: Object.values(analysisData.revenue?.category_breakdown || {}),
        backgroundColor: [
          'rgba(16, 185, 129, 0.8)',
          'rgba(59, 130, 246, 0.8)',
          'rgba(245, 158, 11, 0.8)',
          'rgba(139, 92, 246, 0.8)',
        ],
      },
    ],
  };

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

  const renderOverview = () => (
    <div className="space-y-6">
      {/* Métricas Principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="metric-card"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Ingresos Totales</p>
              <p className="text-xl font-bold text-gray-900">
                {formatCurrency(analysisData.profitability?.total_revenue || 0)}
              </p>
            </div>
            <DollarSign className="h-8 w-8 text-green-600" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="metric-card"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Gastos Totales</p>
              <p className="text-xl font-bold text-gray-900">
                {formatCurrency(analysisData.profitability?.total_expenses || 0)}
              </p>
            </div>
            <TrendingDown className="h-8 w-8 text-red-600" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="metric-card"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Ganancia Neta</p>
              <p className="text-xl font-bold text-gray-900">
                {formatCurrency(analysisData.profitability?.net_profit || 0)}
              </p>
            </div>
            <TrendingUp className="h-8 w-8 text-blue-600" />
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
              <p className="text-sm font-medium text-gray-600">Margen de Ganancia</p>
              <p className="text-xl font-bold text-gray-900">
                {formatPercentage(analysisData.profitability?.profit_margin || 0)}
              </p>
            </div>
            <div className="flex items-center space-x-1">
              {getTrendIcon(analysisData.profitability?.cash_flow_trend)}
            </div>
          </div>
        </motion.div>
      </div>

      {/* Gráficos de Resumen */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Flujo de Caja Mensual</h3>
          <div className="h-64">
            <Bar data={cashFlowChartData} options={chartOptions} />
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Distribución de Gastos</h3>
          <div className="h-64">
            <Doughnut data={expenseChartData} options={{
              responsive: true,
              plugins: {
                legend: {
                  position: 'bottom',
                },
              },
            }} />
          </div>
        </div>
      </div>

      {/* Insights */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Insights y Recomendaciones</h3>
        <div className="space-y-3">
          {analysisData.cashflow?.insights?.map((insight, index) => (
            <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
              <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <p className="text-sm text-gray-700">{insight}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderCashFlow = () => (
    <div className="space-y-6">
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Análisis de Flujo de Caja</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="text-center">
            <p className="text-sm text-gray-600">Total Ingresos</p>
            <p className="text-xl font-semibold text-green-600">
              {formatCurrency(analysisData.cashflow?.total_income || 0)}
            </p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-600">Total Gastos</p>
            <p className="text-xl font-semibold text-red-600">
              {formatCurrency(analysisData.cashflow?.total_expenses || 0)}
            </p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-600">Flujo Neto</p>
            <p className={`text-xl font-semibold ${
              (analysisData.cashflow?.net_cash_flow || 0) >= 0 ? 'text-green-600' : 'text-red-600'
            }`}>
              {formatCurrency(analysisData.cashflow?.net_cash_flow || 0)}
            </p>
          </div>
        </div>
        <div className="h-64">
          <Line data={cashFlowChartData} options={chartOptions} />
        </div>
      </div>
    </div>
  );

  const renderExpenses = () => (
    <div className="space-y-6">
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Análisis de Gastos</h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <h4 className="text-md font-semibold text-gray-900 mb-3">Gastos por Categoría</h4>
            <div className="h-64">
              <Doughnut data={expenseChartData} options={{
                responsive: true,
                plugins: {
                  legend: {
                    position: 'bottom',
                  },
                },
              }} />
            </div>
          </div>
          <div>
            <h4 className="text-md font-semibold text-gray-900 mb-3">Top Categorías</h4>
            <div className="space-y-3">
              {analysisData.expenses?.top_categories?.map((category, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900">{category.category}</p>
                    <p className="text-sm text-gray-600">{formatPercentage(category.percentage)}</p>
                  </div>
                  <p className="font-semibold text-gray-900">{formatCurrency(category.amount)}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderRevenue = () => (
    <div className="space-y-6">
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Análisis de Ingresos</h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <h4 className="text-md font-semibold text-gray-900 mb-3">Ingresos por Categoría</h4>
            <div className="h-64">
              <Doughnut data={revenueChartData} options={{
                responsive: true,
                plugins: {
                  legend: {
                    position: 'bottom',
                  },
                },
              }} />
            </div>
          </div>
          <div>
            <h4 className="text-md font-semibold text-gray-900 mb-3">Top Categorías</h4>
            <div className="space-y-3">
              {analysisData.revenue?.top_categories?.map((category, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900">{category.category}</p>
                  </div>
                  <p className="font-semibold text-gray-900">{formatCurrency(category.amount)}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Análisis Financiero</h1>
          <p className="text-gray-600 mt-1">Análisis detallado de tu situación financiera</p>
        </div>
        <button
          onClick={loadAnalysisData}
          className="btn-secondary flex items-center space-x-2"
        >
          <RefreshCw className="h-4 w-4" />
          <span>Actualizar</span>
        </button>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <tab.icon className="h-4 w-4" />
              <span>{tab.name}</span>
            </button>
          ))}
        </nav>
      </div>

      {/* Content */}
      {activeTab === 'overview' && renderOverview()}
      {activeTab === 'cashflow' && renderCashFlow()}
      {activeTab === 'expenses' && renderExpenses()}
      {activeTab === 'revenue' && renderRevenue()}
    </div>
  );
};

export default Analysis;
