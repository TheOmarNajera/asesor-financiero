"""
Servicio de Google Gemini para procesamiento de lenguaje natural
y generación de análisis financiero inteligente
"""

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ google-generativeai no disponible, usando respuestas simuladas")
import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from app.models.financial_models import ChatMessage, ChatResponse, FinancialMetrics
from app.services.snowflake_service import snowflake_service

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        self.is_available = False
        
        # Verificar si Gemini está disponible
        if not GEMINI_AVAILABLE:
            logger.warning("⚠️ google-generativeai no disponible, usando respuestas simuladas")
            self.is_available = False
            return
            
        if not self.api_key:
            logger.warning("GEMINI_API_KEY no configurada, usando modo simulado")
            self.api_key = "demo_key"
        
        try:
            genai.configure(api_key=self.api_key)
            # Probar con modelos disponibles: gemini-2.0-flash (rápido y estable)
            try:
                self.model = genai.GenerativeModel('gemini-2.0-flash')
                self.is_available = True
                logger.info("✅ Gemini API configurada correctamente (gemini-2.0-flash)")
            except Exception as e1:
                logger.warning(f"gemini-2.0-flash no disponible ({e1}), intentando gemini-2.5-flash")
                # Si no funciona, intentar con gemini-2.5-flash
                try:
                    self.model = genai.GenerativeModel('gemini-2.5-flash')
                    self.is_available = True
                    logger.info("✅ Gemini API configurada correctamente (gemini-2.5-flash)")
                except Exception as e2:
                    logger.warning(f"gemini-2.5-flash no disponible ({e2}), intentando gemini-2.5-pro")
                    # Si no funciona, intentar con gemini-2.5-pro
                    try:
                        self.model = genai.GenerativeModel('gemini-2.5-pro')
                        self.is_available = True
                        logger.info("✅ Gemini API configurada correctamente (gemini-2.5-pro)")
                    except Exception as e3:
                        logger.error(f"Ningún modelo de Gemini disponible ({e3}), usando modo simulado")
                        self.is_available = False
        except Exception as e:
            logger.error(f"Error al configurar Gemini: {str(e)}")
            self.is_available = False
    
    async def analyze_financial_question(self, message: ChatMessage, context: Dict[str, Any]) -> ChatResponse:
        """Analizar pregunta financiera usando Gemini"""
        try:
            if not self.is_available:
                return await self._simulate_response(message, context)
            
            # Preparar contexto financiero
            financial_context = self._prepare_financial_context(context)
            
            # Crear prompt estructurado
            prompt = self._create_analysis_prompt(message.message, financial_context)
            
            # Generar respuesta con Gemini
            response = self.model.generate_content(prompt)
            
            # Procesar respuesta
            return self._process_gemini_response(response.text, message.message)
            
        except Exception as e:
            logger.error(f"Error en análisis con Gemini: {str(e)}")
            return await self._simulate_response(message, context)
    
    def _prepare_financial_context(self, context: Dict[str, Any]) -> str:
        """Preparar contexto financiero para el prompt"""
        context_str = "CONTEXTO FINANCIERO ACTUAL:\n\n"
        
        if 'metrics' in context and context['metrics']:
            metrics = context['metrics']
            context_str += f"• Ingresos totales: ${metrics.get('total_revenue', 0):,.2f}\n"
            context_str += f"• Gastos totales: ${metrics.get('total_expenses', 0):,.2f}\n"
            context_str += f"• Ganancia neta: ${metrics.get('net_profit', 0):,.2f}\n"
            context_str += f"• Margen de ganancia: {metrics.get('profit_margin', 0):.1f}%\n"
            context_str += f"• Tendencia de flujo de caja: {metrics.get('cash_flow_trend', 'estable')}\n\n"
        
        if 'cash_flow' in context and context['cash_flow']:
            context_str += "HISTORIAL DE FLUJO DE CAJA (últimos 3 meses):\n"
            for cf in context['cash_flow'][-3:]:
                context_str += f"• {cf['period']}: Ingresos ${cf['income']:,.2f}, Gastos ${cf['expenses']:,.2f}, Neto ${cf['net_cash_flow']:,.2f}\n"
            context_str += "\n"
        
        if 'expense_breakdown' in context and context['expense_breakdown']:
            context_str += "DESGLOSE DE GASTOS:\n"
            for category, amount in context['expense_breakdown'].items():
                context_str += f"• {category}: ${amount:,.2f}\n"
            context_str += "\n"
        
        return context_str
    
    def _create_analysis_prompt(self, question: str, financial_context: str) -> str:
        """Crear prompt estructurado para análisis financiero"""
        return f"""
        Eres Maya, Asesora Financiera de Banorte. Responde de forma CÓMIDA y NATURAL, como una conversación de chat.

        {financial_context}

        PREGUNTA: {question}

        INSTRUCCIONES:
        - Responde EN CONVERSACIÓN, NO EN FORMATO DE DOCUMENTO
        - MÁXIMO 3-4 párrafos de 2-3 líneas cada uno
        - Usa DATOS ESPECÍFICOS de su empresa (las cifras que ves arriba)
        - Sé DIRECTO y CONCRETO
        - Evita listas con bullets extensas
        - Termina con UNA pregunta simple de seguimiento

        EJEMPLO DE TONO:
        "Hola! Veo que tu empresa tiene un margen de 51.7%, eso es excelente. Para mejorar el flujo de caja en octubre que bajó a $507k, te recomiendo revisar políticas de cobranza..."

        NO HAGAS:
        - Listas numeradas extensas
        - Secciones con títulos tipo "**Análisis:"** etc
        - Mencionar que "eres Carlos Mendoza" cada vez
        - Respuestas muy largas

        Responde YA como chat, natural y corto.
        """
    
    def _process_gemini_response(self, response_text: str, original_question: str) -> ChatResponse:
        """Procesar respuesta de Gemini y estructurarla"""
        try:
            # Extraer recomendaciones del texto
            recommendations = self._extract_recommendations(response_text)
            
            # Determinar confianza basada en la completitud de la respuesta
            confidence = self._calculate_confidence(response_text, original_question)
            
            # Identificar visualizaciones sugeridas
            visualizations = self._suggest_visualizations(original_question)
            
            return ChatResponse(
                content=response_text,
                recommendations=recommendations,
                visualizations=visualizations,
                confidence=confidence
            )
            
        except Exception as e:
            logger.error(f"Error al procesar respuesta de Gemini: {str(e)}")
            return ChatResponse(
                content=response_text,
                confidence=0.7
            )
    
    def _extract_recommendations(self, text: str) -> List[str]:
        """Extraer recomendaciones del texto de respuesta"""
        recommendations = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Buscar líneas que parecen recomendaciones
            if (line.startswith(('•', '-', '*', '1.', '2.', '3.')) or 
                'recomiendo' in line.lower() or 
                'sugiero' in line.lower() or
                'deberías' in line.lower()):
                recommendations.append(line)
        
        return recommendations[:5]  # Máximo 5 recomendaciones
    
    def _calculate_confidence(self, response: str, question: str) -> float:
        """Calcular nivel de confianza de la respuesta"""
        confidence = 0.8  # Base
        
        # Aumentar confianza si la respuesta es específica
        if any(word in response.lower() for word in ['$', '%', 'meses', 'años', 'número']):
            confidence += 0.1
        
        # Disminuir confianza si hay incertidumbre
        if any(word in response.lower() for word in ['no estoy seguro', 'posiblemente', 'tal vez', 'podría ser']):
            confidence -= 0.2
        
        return min(max(confidence, 0.1), 1.0)
    
    def _suggest_visualizations(self, question: str) -> List[str]:
        """Sugerir visualizaciones basadas en la pregunta"""
        visualizations = []
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['flujo', 'cash', 'dinero', 'liquidez']):
            visualizations.append('cash_flow_chart')
        
        if any(word in question_lower for word in ['gastos', 'expenses', 'costos']):
            visualizations.append('expense_breakdown')
        
        if any(word in question_lower for word in ['ingresos', 'ventas', 'revenue']):
            visualizations.append('revenue_trend')
        
        if any(word in question_lower for word in ['proyección', 'futuro', 'simulación']):
            visualizations.append('projection_chart')
        
        return visualizations
    
    async def _simulate_response(self, message: ChatMessage, context: Dict[str, Any]) -> ChatResponse:
        """Simular respuesta cuando Gemini no está disponible"""
        question_lower = message.message.lower()
        
        if 'contratar' in question_lower or 'empleado' in question_lower:
            return ChatResponse(
                content="""Basándome en tu situación financiera actual, puedo ayudarte a evaluar la viabilidad de contratar un nuevo empleado.

**Análisis de Viabilidad:**
Para determinar si puedes contratar un nuevo empleado, necesito considerar varios factores:
- Tu flujo de caja actual y proyecciones futuras
- El costo total del empleado (salario + prestaciones + impuestos)
- El impacto en tus márgenes de ganancia
- La capacidad de generar ingresos adicionales

**Recomendaciones:**
1. Calcula el costo total del empleado (aproximadamente 1.3x el salario base)
2. Asegúrate de tener al menos 3 meses de gastos operativos en reserva
3. Considera contratar por proyecto o tiempo parcial inicialmente
4. Evalúa si el nuevo empleado puede generar ingresos adicionales

¿Te gustaría que analice un escenario específico con números concretos?""",
                recommendations=[
                    "Calcular costo total del empleado (salario + prestaciones)",
                    "Mantener reserva de 3 meses de gastos operativos",
                    "Considerar contratación gradual o por proyecto",
                    "Evaluar ROI del nuevo empleado"
                ],
                visualizations=['cash_flow_chart', 'projection_chart'],
                confidence=0.8
            )
        
        elif 'invertir' in question_lower or 'compra' in question_lower:
            return ChatResponse(
                content="""Para evaluar una inversión, necesito analizar varios aspectos de tu situación financiera.

**Factores a Considerar:**
- Impacto en el flujo de caja inmediato
- Retorno de inversión esperado
- Período de recuperación
- Alternativas de financiamiento

**Recomendaciones:**
1. Calcula el período de recuperación de la inversión
2. Evalúa diferentes opciones de financiamiento
3. Considera el impacto en tu liquidez operativa
4. Analiza escenarios optimistas y pesimistas

¿Podrías proporcionarme más detalles sobre la inversión que estás considerando?""",
                recommendations=[
                    "Calcular período de recuperación",
                    "Evaluar opciones de financiamiento",
                    "Analizar impacto en liquidez",
                    "Considerar escenarios múltiples"
                ],
                visualizations=['projection_chart', 'cash_flow_chart'],
                confidence=0.7
            )
        
        else:
            return ChatResponse(
                content="""Hola! Soy tu asesor financiero inteligente. Puedo ayudarte con:

• Análisis de viabilidad de contrataciones
• Evaluación de inversiones y compras
• Optimización de gastos
• Proyecciones financieras
• Análisis de flujo de caja

¿En qué aspecto específico de tus finanzas te gustaría que te ayude?""",
                recommendations=[
                    "Haz preguntas específicas sobre tu situación financiera",
                    "Proporciona contexto sobre tus objetivos",
                    "Menciona números concretos cuando sea posible"
                ],
                confidence=0.9
            )
    
    async def generate_simulation_analysis(self, scenario: Dict[str, Any], base_data: Dict[str, Any]) -> str:
        """Generar análisis de simulación usando Gemini"""
        try:
            if not self.is_available:
                return self._simulate_simulation_analysis(scenario, base_data)
            
            prompt = f"""
Analiza el siguiente escenario financiero para una PyME:

ESCENARIO: {scenario.get('name', 'Simulación')}
DESCRIPCIÓN: {scenario.get('description', '')}
PARÁMETROS: {json.dumps(scenario.get('parameters', {}), indent=2)}

DATOS BASE:
- Ingresos mensuales promedio: ${base_data.get('monthly_revenue', 0):,.2f}
- Gastos mensuales promedio: ${base_data.get('monthly_expenses', 0):,.2f}
- Flujo de caja neto: ${base_data.get('net_cash_flow', 0):,.2f}

Proporciona:
1. Análisis del impacto del escenario
2. Recomendaciones específicas
3. Evaluación de riesgos
4. Próximos pasos sugeridos

Responde en español de manera clara y práctica.
"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error en análisis de simulación: {str(e)}")
            return self._simulate_simulation_analysis(scenario, base_data)
    
    def _simulate_simulation_analysis(self, scenario: Dict[str, Any], base_data: Dict[str, Any]) -> str:
        """Simular análisis de simulación"""
        return f"""
**Análisis del Escenario: {scenario.get('name', 'Simulación')}**

Basándome en los datos financieros actuales, este escenario tendría el siguiente impacto:

**Impacto Financiero:**
- Cambio en flujo de caja: Variable según parámetros
- Impacto en liquidez: Requiere análisis detallado
- Riesgo financiero: Moderado a alto dependiendo de la magnitud

**Recomendaciones:**
1. Realizar análisis de sensibilidad
2. Considerar financiamiento gradual
3. Mantener reservas de emergencia
4. Monitorear métricas clave mensualmente

**Próximos Pasos:**
- Validar supuestos del escenario
- Preparar plan de contingencia
- Establecer métricas de seguimiento
"""
