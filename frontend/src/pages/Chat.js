import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, 
  Bot, 
  User, 
  Lightbulb,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Loader2,
  Sparkles,
  MessageCircle,
  Zap,
  Target,
  Calculator
} from 'lucide-react';
import toast from 'react-hot-toast';
import api from '../services/api';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    loadSuggestions();
    // Agregar mensaje de bienvenida
        setMessages([{
          id: 1,
          type: 'assistant',
          content: '¡Buenos días! Soy Carlos Mendoza, su Asesor Financiero Senior de Banorte. He revisado la situación financiera de su empresa y estoy aquí para ayudarle a optimizar su crecimiento y rentabilidad. ¿En qué aspecto financiero le gustaría que le asesore hoy?',
          timestamp: new Date(),
          confidence: 0.9
        }]);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadSuggestions = async () => {
    try {
      const response = await api.get('/api/chat/suggestions');
      setSuggestions(response.data);
    } catch (error) {
      console.error('Error cargando sugerencias:', error);
    }
  };

  const sendMessage = async (messageText = inputMessage) => {
    if (!messageText.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: messageText,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await api.post('/api/chat/message', {
        message: messageText,
        user_id: 'demo_user'
      });

      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: response.data.response,
        recommendations: response.data.recommendations,
        visualizations: response.data.visualizations,
        confidence: response.data.confidence,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
      
      // Mostrar toast de éxito
      toast.success('Respuesta generada exitosamente');
      
    } catch (error) {
      console.error('Error enviando mensaje:', error);
      toast.error('Error al procesar tu mensaje');
      
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta de nuevo.',
        timestamp: new Date(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInputMessage(suggestion);
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('es-MX', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'text-banorte-success';
    if (confidence >= 0.6) return 'text-banorte-warning';
    return 'text-banorte-danger';
  };

  const getConfidenceIcon = (confidence) => {
    if (confidence >= 0.8) return <CheckCircle className="h-4 w-4" />;
    if (confidence >= 0.6) return <AlertCircle className="h-4 w-4" />;
    return <AlertCircle className="h-4 w-4" />;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
              <h1 className="text-4xl font-bold text-banorte-primary font-display">Asesor Financiero Banorte</h1>
              <p className="text-banorte-secondary mt-2 text-lg">Carlos Mendoza - Su consultor financiero personal</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-sm text-banorte-primary">
            <div className="w-2 h-2 bg-banorte-success rounded-full animate-pulse"></div>
            <span>IA Activa</span>
          </div>
          <div className="flex items-center space-x-2 text-sm text-banorte-primary">
            <Sparkles className="h-4 w-4" />
            <span>Powered by Gemini</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Chat Area */}
        <div className="lg:col-span-3">
          <div className="card h-[600px] flex flex-col">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              <AnimatePresence>
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`flex max-w-3xl ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                      {/* Avatar */}
                      <div className={`flex-shrink-0 ${message.type === 'user' ? 'ml-3' : 'mr-3'}`}>
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                          message.type === 'user' ? 'bg-banorte-primary' : 'bg-banorte-light border border-banorte-primary'
                        }`}>
                          {message.type === 'user' ? (
                            <User className="h-4 w-4 text-white" />
                          ) : (
                            <Bot className="h-4 w-4 text-banorte-primary" />
                          )}
                        </div>
                      </div>

                      {/* Message Content */}
                      <div className={`flex-1 ${message.type === 'user' ? 'text-right' : 'text-left'}`}>
                        <div className={`inline-block p-4 rounded-lg ${
                          message.type === 'user' 
                            ? 'bg-banorte-primary text-white' 
                            : message.isError 
                              ? 'bg-banorte-danger bg-opacity-10 text-banorte-danger border border-banorte-danger'
                              : 'bg-banorte-light text-banorte-dark border border-gray-200'
                        }`}>
                          <p className="whitespace-pre-wrap">{message.content}</p>
                          
                          {/* Recommendations */}
                          {message.recommendations && message.recommendations.length > 0 && (
                            <div className="mt-3 pt-3 border-t border-gray-200">
                              <div className="flex items-center space-x-2 mb-2">
                                <Lightbulb className="h-4 w-4 text-yellow-600" />
                                <span className="text-sm font-medium text-gray-700">Recomendaciones:</span>
                              </div>
                              <ul className="text-sm space-y-1">
                                {message.recommendations.map((rec, index) => (
                                  <li key={index} className="flex items-start space-x-2">
                                    <span className="text-gray-500">•</span>
                                    <span>{rec}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {/* Visualizations */}
                          {message.visualizations && message.visualizations.length > 0 && (
                            <div className="mt-3 pt-3 border-t border-gray-200">
                              <div className="flex items-center space-x-2 mb-2">
                                <TrendingUp className="h-4 w-4 text-blue-600" />
                                <span className="text-sm font-medium text-gray-700">Visualizaciones disponibles:</span>
                              </div>
                              <div className="flex flex-wrap gap-2">
                                {message.visualizations.map((viz, index) => (
                                  <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                                    {viz.replace('_', ' ')}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>

                        {/* Timestamp and Confidence */}
                        <div className={`flex items-center space-x-2 mt-1 text-xs text-gray-500 ${
                          message.type === 'user' ? 'justify-end' : 'justify-start'
                        }`}>
                          <span>{formatTime(message.timestamp)}</span>
                          {message.confidence && (
                            <div className={`flex items-center space-x-1 ${getConfidenceColor(message.confidence)}`}>
                              {getConfidenceIcon(message.confidence)}
                              <span>{(message.confidence * 100).toFixed(0)}%</span>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>

              {/* Loading indicator */}
              {isLoading && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex justify-start"
                >
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
                      <Bot className="h-4 w-4 text-gray-600" />
                    </div>
                    <div className="bg-gray-100 p-4 rounded-lg">
                      <div className="flex items-center space-x-2">
                        <Loader2 className="h-4 w-4 animate-spin text-gray-600" />
                        <span className="text-gray-600">Analizando tu consulta...</span>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="border-t border-gray-200 p-4">
              <div className="flex space-x-3">
                <div className="flex-1">
                  <textarea
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                        placeholder="Escriba su consulta financiera aquí..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                    rows={2}
                    disabled={isLoading}
                  />
                </div>
                <button
                  onClick={() => sendMessage()}
                  disabled={!inputMessage.trim() || isLoading}
                  className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Send className="h-4 w-4" />
                  <span>Enviar</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Suggestions Sidebar */}
        <div className="lg:col-span-1">
          <div className="card">
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-banorte-primary bg-opacity-20 rounded-lg flex items-center justify-center">
                <MessageCircle className="h-5 w-5 text-banorte-primary" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-banorte-primary font-display">Preguntas Sugeridas</h3>
                <p className="text-banorte-secondary text-sm">Haz clic para preguntar</p>
              </div>
            </div>
            <div className="space-y-3">
              {suggestions.map((suggestion, index) => (
                <motion.button
                  key={index}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  onClick={() => handleSuggestionClick(suggestion)}
                  className="w-full text-left p-3 bg-banorte-light hover:bg-banorte-primary hover:text-white rounded-lg transition-all duration-200 text-sm"
                >
                  <div className="flex items-start space-x-2">
                    <div className="w-6 h-6 bg-banorte-primary bg-opacity-20 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-xs font-bold text-banorte-primary">{index + 1}</span>
                    </div>
                    <span>{suggestion}</span>
                  </div>
                </motion.button>
              ))}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="card mt-6">
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-banorte-accent bg-opacity-20 rounded-lg flex items-center justify-center">
                <Target className="h-5 w-5 text-banorte-accent" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-banorte-primary font-display">Acciones Rápidas</h3>
                <p className="text-banorte-secondary text-sm">Herramientas útiles para tu PyME</p>
              </div>
            </div>
            <div className="space-y-3">
                  <button
                    onClick={() => handleSuggestionClick("¿Cómo puedo mejorar mi flujo de caja mensual?")}
                    className="w-full text-left p-3 text-sm text-banorte-primary bg-banorte-light hover:bg-banorte-primary hover:text-white rounded-lg transition-all duration-200 flex items-center space-x-2"
                  >
                    <TrendingUp className="h-4 w-4" />
                    <span>📊 Optimizar flujo de caja</span>
                  </button>
                  <button
                    onClick={() => handleSuggestionClick("¿Qué estrategias recomienda para aumentar mis ingresos?")}
                    className="w-full text-left p-3 text-sm text-banorte-primary bg-banorte-light hover:bg-banorte-primary hover:text-white rounded-lg transition-all duration-200 flex items-center space-x-2"
                  >
                    <Calculator className="h-4 w-4" />
                    <span>💰 Estrategias de crecimiento</span>
                  </button>
                  <button
                    onClick={() => handleSuggestionClick("¿Es momento de considerar un crédito para expansión?")}
                    className="w-full text-left p-3 text-sm text-banorte-primary bg-banorte-light hover:bg-banorte-primary hover:text-white rounded-lg transition-all duration-200 flex items-center space-x-2"
                  >
                    <Lightbulb className="h-4 w-4" />
                    <span>🏦 Opciones de financiamiento</span>
                  </button>
            </div>
            
            <div className="mt-6 pt-6 border-t border-gray-200">
              <div className="flex items-center space-x-2 text-xs text-banorte-primary">
                <Zap className="h-4 w-4" />
                <div>
                  <p className="font-medium">Powered by Azure Arm</p>
                  <p className="text-gray-500">Hack Mty 2025</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
