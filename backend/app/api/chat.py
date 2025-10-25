"""
Endpoints para chat inteligente con IA
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
import logging

from app.models.financial_models import ChatMessage, ChatResponse
from app.services.data_service import DataService
from app.services.gemini_service import GeminiService

logger = logging.getLogger(__name__)
router = APIRouter()

def get_data_service() -> DataService:
    return DataService()

def get_gemini_service() -> GeminiService:
    return GeminiService()

@router.post("/message")
async def send_message(
    message: ChatMessage,
    data_service: DataService = Depends(get_data_service),
    gemini_service: GeminiService = Depends(get_gemini_service)
) -> ChatResponse:
    """Enviar mensaje al asistente financiero"""
    try:
        # Preparar contexto financiero
        context = {
            "metrics": data_service.metrics.dict() if data_service.metrics else {},
            "cash_flow": [cf.dict() for cf in data_service.cash_flow_history[-3:]],
            "expense_breakdown": data_service.metrics.expense_breakdown if data_service.metrics else {},
            "revenue_breakdown": data_service.metrics.revenue_breakdown if data_service.metrics else {},
            "total_transactions": len(data_service.transactions)
        }
        
        # Procesar mensaje con IA
        response = await gemini_service.analyze_financial_question(message, context)
        
        return response
        
    except Exception as e:
        logger.error(f"Error en chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en chat: {str(e)}")

@router.get("/history")
async def get_chat_history(
    user_id: str = None,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """Obtener historial de conversación"""
    # En una implementación real, esto vendría de una base de datos
    return [
        {
            "id": 1,
            "user_message": "¿Podemos contratar un nuevo empleado?",
            "assistant_response": "Basándome en tu situación financiera actual...",
            "timestamp": "2024-01-15T10:30:00Z",
            "confidence": 0.8
        },
        {
            "id": 2,
            "user_message": "¿Cuál sería el impacto de invertir en nueva maquinaria?",
            "assistant_response": "Para evaluar esta inversión necesito analizar...",
            "timestamp": "2024-01-15T11:15:00Z",
            "confidence": 0.7
        }
    ]

@router.get("/suggestions")
async def get_suggestions(
    data_service: DataService = Depends(get_data_service)
) -> List[str]:
    """Obtener sugerencias de preguntas"""
    suggestions = [
        "¿Cómo puedo mejorar mi flujo de caja mensual?",
        "¿Qué estrategias recomienda para aumentar mis ingresos?",
        "¿Es momento de considerar un crédito para expansión?",
        "¿Cómo puedo optimizar mis gastos operativos?",
        "¿Qué productos de inversión de Banorte me recomienda?",
        "¿Cómo puedo preparar mi empresa para el crecimiento?",
        "¿Qué seguros empresariales necesito para proteger mi negocio?",
        "¿Cómo puedo mejorar mi margen de ganancia?"
    ]
    
    # Personalizar sugerencias basadas en datos disponibles
    if data_service.metrics:
        if data_service.metrics.cash_flow_trend == "negative":
            suggestions.insert(0, "¿Cómo puedo mejorar mi flujo de caja negativo?")
        elif data_service.metrics.profit_margin < 10:
            suggestions.insert(0, "¿Cómo puedo aumentar mi margen de ganancia?")
    
    return suggestions[:8]  # Máximo 8 sugerencias
