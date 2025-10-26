import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Plus, 
  Edit, 
  Trash2, 
  DollarSign,
  TrendingUp,
  TrendingDown,
  Calendar,
  Tag,
  Save,
  X,
  Filter,
  Search,
  Download,
  Upload
} from 'lucide-react';
import toast from 'react-hot-toast';
import api from '../services/api';

const FinancialDataManager = () => {
  const [transactions, setTransactions] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingTransaction, setEditingTransaction] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [isLoading, setIsLoading] = useState(false);

  const [newTransaction, setNewTransaction] = useState({
    description: '',
    amount: '',
    type: 'expense',
    category: '',
    date: new Date().toISOString().split('T')[0],
    notes: ''
  });

  // Cargar transacciones del backend
  useEffect(() => {
    loadTransactions();
  }, []);

  const loadTransactions = async () => {
    setIsLoading(true);
    try {
      const response = await api.get('/api/transactions/?limit=10');
      // Mapear datos del backend al formato del frontend
      const mappedTransactions = response.data.map(t => ({
        id: t.id || t.transaction_id,
        description: t.description,
        amount: t.amount,
        type: t.transaction_type || t.type, // Mapear transaction_type a type
        category: t.category,
        date: t.date || t.transaction_date,
        notes: t.notes || ''
      }));
      setTransactions(mappedTransactions);
    } catch (error) {
      console.error('Error cargando transacciones:', error);
      toast.error('Error cargando transacciones');
    } finally {
      setIsLoading(false);
    }
  };

  const filteredTransactions = transactions.filter(transaction => {
    const matchesSearch = transaction.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         transaction.category.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterType === 'all' || transaction.type === filterType;
    return matchesSearch && matchesFilter;
  });

  const handleAddTransaction = async () => {
    if (!newTransaction.description || !newTransaction.amount || !newTransaction.category) {
      toast.error('Por favor completa todos los campos obligatorios');
      return;
    }

    setIsLoading(true);
    try {
      // Mapear a formato del backend
      const categoryMapping = {
        'Ventas': 'sales',
        'Marketing': 'marketing',
        'Personal': 'personnel',
        'Equipo': 'equipment',
        'Servicios': 'utilities',
        'Gastos Operativos': 'operating_expenses',
        'Otros': 'other'
      };

      const transaction = {
        date: newTransaction.date,
        amount: parseFloat(newTransaction.amount),
        description: newTransaction.description,
        category: categoryMapping[newTransaction.category] || 'other',
        transaction_type: newTransaction.type === 'income' ? 'income' : 'expense'
      };

      await api.post('/api/transactions/', transaction);
      toast.success('Transacción agregada exitosamente');
      setShowAddForm(false);
      setNewTransaction({
        description: '',
        amount: '',
        type: 'expense',
        category: '',
        date: new Date().toISOString().split('T')[0],
        notes: ''
      });
      // Recargar transacciones
      loadTransactions();
    } catch (error) {
      console.error('Error agregando transacción:', error);
      toast.error('Error agregando transacción');
    } finally {
      setIsLoading(false);
    }
  };

  const handleEditTransaction = (transaction) => {
    setEditingTransaction(transaction);
    setNewTransaction({
      description: transaction.description,
      amount: transaction.amount.toString(),
      type: transaction.type,
      category: transaction.category,
      date: transaction.date,
      notes: transaction.notes || ''
    });
    setShowAddForm(true);
  };

  const handleUpdateTransaction = () => {
    if (!newTransaction.description || !newTransaction.amount || !newTransaction.category) {
      toast.error('Por favor completa todos los campos obligatorios');
      return;
    }

    const updatedTransaction = {
      ...editingTransaction,
      ...newTransaction,
      amount: parseFloat(newTransaction.amount)
    };

    setTransactions(transactions.map(t => t.id === editingTransaction.id ? updatedTransaction : t));
    setEditingTransaction(null);
    setShowAddForm(false);
    setNewTransaction({
      description: '',
      amount: '',
      type: 'expense',
      category: '',
      date: new Date().toISOString().split('T')[0],
      notes: ''
    });
    toast.success('Transacción actualizada exitosamente');
  };

  const handleDeleteTransaction = (id) => {
    setTransactions(transactions.filter(t => t.id !== id));
    toast.success('Transacción eliminada exitosamente');
  };

  const handleInputChange = (e) => {
    setNewTransaction({
      ...newTransaction,
      [e.target.name]: e.target.value
    });
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency: 'MXN'
    }).format(amount);
  };

  const getTotalIncome = () => {
    return transactions.filter(t => t.type === 'income').reduce((sum, t) => sum + t.amount, 0);
  };

  const getTotalExpenses = () => {
    return transactions.filter(t => t.type === 'expense').reduce((sum, t) => sum + t.amount, 0);
  };

  const getNetProfit = () => {
    return getTotalIncome() - getTotalExpenses();
  };

  const categories = [
    'Ventas', 'Servicios', 'Gastos Operativos', 'Marketing', 
    'Recursos Humanos', 'Tecnología', 'Impuestos', 'Otros'
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-banorte-primary font-display">Gestión de Datos Financieros</h1>
          <p className="text-banorte-accent mt-2">Administra tus ingresos y gastos empresariales</p>
        </div>
        <button
          onClick={() => setShowAddForm(true)}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus className="h-4 w-4" />
          <span>Agregar Transacción</span>
        </button>
      </div>

      {/* Resumen financiero */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="metric-card metric-card-income">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-financial-income mb-1">Total Ingresos</p>
              <p className="text-2xl font-bold text-financial-income">
                {formatCurrency(getTotalIncome())}
              </p>
            </div>
            <TrendingUp className="h-8 w-8 text-financial-income" />
          </div>
        </div>

        <div className="metric-card metric-card-expense">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-financial-expense mb-1">Total Gastos</p>
              <p className="text-2xl font-bold text-financial-expense">
                {formatCurrency(getTotalExpenses())}
              </p>
            </div>
            <TrendingDown className="h-8 w-8 text-financial-expense" />
          </div>
        </div>

        <div className="metric-card metric-card-profit">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-financial-profit mb-1">Ganancia Neta</p>
              <p className="text-2xl font-bold text-financial-profit">
                {formatCurrency(getNetProfit())}
              </p>
            </div>
            <DollarSign className="h-8 w-8 text-financial-profit" />
          </div>
        </div>
      </div>

      {/* Filtros y búsqueda */}
      <div className="card">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-banorte-accent" />
              <input
                type="text"
                placeholder="Buscar transacciones..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-banorte-primary focus:border-transparent w-full"
              />
            </div>
          </div>
          <div className="flex gap-2">
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-banorte-primary focus:border-transparent"
            >
              <option value="all">Todos</option>
              <option value="income">Ingresos</option>
              <option value="expense">Gastos</option>
            </select>
            <button className="btn-secondary flex items-center space-x-2">
              <Download className="h-4 w-4" />
              <span>Exportar</span>
            </button>
          </div>
        </div>
      </div>

      {/* Tabla de transacciones */}
      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-banorte-light">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-banorte-primary uppercase tracking-wider">
                  Descripción
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-banorte-primary uppercase tracking-wider">
                  Tipo
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-banorte-primary uppercase tracking-wider">
                  Categoría
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-banorte-primary uppercase tracking-wider">
                  Monto
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-banorte-primary uppercase tracking-wider">
                  Fecha
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-banorte-primary uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredTransactions.map((transaction) => (
                <tr key={transaction.id} className="hover:bg-banorte-light transition-colors duration-200">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-banorte-dark">
                        {transaction.description}
                      </div>
                      {transaction.notes && (
                        <div className="text-sm text-banorte-accent">
                          {transaction.notes}
                        </div>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      transaction.type === 'income' 
                        ? 'text-green-600 bg-green-100' 
                        : 'text-red-600 bg-red-100'
                    }`}>
                      {transaction.type === 'income' ? 'Ingreso' : 'Gasto'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-banorte-accent">
                    {transaction.category}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <span className={transaction.type === 'income' ? 'text-financial-income' : 'text-financial-expense'}>
                      {formatCurrency(transaction.amount)}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-banorte-accent">
                    {new Date(transaction.date).toLocaleDateString('es-MX')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => handleEditTransaction(transaction)}
                        className="p-1 rounded text-banorte-primary hover:bg-banorte-primary hover:bg-opacity-10"
                        title="Editar"
                      >
                        <Edit className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteTransaction(transaction.id)}
                        className="p-1 rounded text-red-600 hover:bg-red-100"
                        title="Eliminar"
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

      {/* Modal para agregar/editar transacción */}
      {showAddForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-lg p-6 w-full max-w-md mx-4"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-banorte-primary">
                {editingTransaction ? 'Editar Transacción' : 'Agregar Transacción'}
              </h3>
              <button
                onClick={() => {
                  setShowAddForm(false);
                  setEditingTransaction(null);
                  setNewTransaction({
                    description: '',
                    amount: '',
                    type: 'expense',
                    category: '',
                    date: new Date().toISOString().split('T')[0],
                    notes: ''
                  });
                }}
                className="p-1 rounded text-banorte-accent hover:bg-banorte-light"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-banorte-dark mb-1">
                  Descripción *
                </label>
                <input
                  type="text"
                  name="description"
                  value={newTransaction.description}
                  onChange={handleInputChange}
                  className="input-field"
                  placeholder="Ej. Venta de productos"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-banorte-dark mb-1">
                    Tipo *
                  </label>
                  <select
                    name="type"
                    value={newTransaction.type}
                    onChange={handleInputChange}
                    className="input-field"
                  >
                    <option value="income">Ingreso</option>
                    <option value="expense">Gasto</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-banorte-dark mb-1">
                    Monto *
                  </label>
                  <input
                    type="number"
                    name="amount"
                    value={newTransaction.amount}
                    onChange={handleInputChange}
                    className="input-field"
                    placeholder="0.00"
                    step="0.01"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-banorte-dark mb-1">
                  Categoría *
                </label>
                <select
                  name="category"
                  value={newTransaction.category}
                  onChange={handleInputChange}
                  className="input-field"
                >
                  <option value="">Seleccionar categoría</option>
                  {categories.map(category => (
                    <option key={category} value={category}>{category}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-banorte-dark mb-1">
                  Fecha
                </label>
                <input
                  type="date"
                  name="date"
                  value={newTransaction.date}
                  onChange={handleInputChange}
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-banorte-dark mb-1">
                  Notas
                </label>
                <textarea
                  name="notes"
                  value={newTransaction.notes}
                  onChange={handleInputChange}
                  className="input-field resize-none"
                  rows="3"
                  placeholder="Notas adicionales..."
                />
              </div>
            </div>

            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={() => {
                  setShowAddForm(false);
                  setEditingTransaction(null);
                  setNewTransaction({
                    description: '',
                    amount: '',
                    type: 'expense',
                    category: '',
                    date: new Date().toISOString().split('T')[0],
                    notes: ''
                  });
                }}
                className="btn-secondary"
              >
                Cancelar
              </button>
              <button
                onClick={editingTransaction ? handleUpdateTransaction : handleAddTransaction}
                className="btn-primary flex items-center space-x-2"
              >
                <Save className="h-4 w-4" />
                <span>{editingTransaction ? 'Actualizar' : 'Guardar'}</span>
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default FinancialDataManager;
