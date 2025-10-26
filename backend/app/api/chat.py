"""
Endpoints para chat inteligente con IA
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Dict, Any, List, Optional
import logging

from app.models.financial_models import ChatMessage, ChatResponse
from app.services.data_service import DataService
from app.services.gemini_service import GeminiService
from app.services.elevenlabs_service import elevenlabs_service

logger = logging.getLogger(__name__)
router = APIRouter()

def get_data_service(empresa_id: Optional[str] = Header(None, alias="X-Empresa-ID")) -> DataService:
    """Dependency para obtener el servicio de datos con empresa_id del header"""
    empresa = empresa_id or "E001"
    return DataService(empresa_id=empresa)

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
        
        # Generar audio con ElevenLabs si está disponible (opcional - no bloquear si falla)
        if elevenlabs_service.is_available and response.content:
            try:
                audio_response = elevenlabs_service.create_audio_response(
                    response.content, 
                    response_type="carlos"  # Voz específica de Maya (usar 'carlos' para manter el voice_id correcto)
                )
                if audio_response:
                    response.audio_data = audio_response
            except Exception as audio_error:
                # Si hay error en audio (cuota, etc), no falla el chat completo
                logger.warning(f"No se pudo generar audio: {str(audio_error)}")
        
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
    
    return suggestions

@router.post("/audio")
async def generate_audio_response(
    message: ChatMessage,
    data_service: DataService = Depends(get_data_service),
    gemini_service: GeminiService = Depends(get_gemini_service)
) -> Dict[str, Any]:
    """Generar respuesta de audio para el chat"""
    try:
        if not elevenlabs_service.is_available:
            raise HTTPException(status_code=503, detail="Servicio de audio no disponible")
        
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
        
        # Generar audio
        audio_response = elevenlabs_service.create_audio_response(
            response.content, 
            response_type="carlos"
        )
        
        if not audio_response:
            raise HTTPException(status_code=500, detail="Error generando audio")
        
        return {
            "success": True,
            "audio_data": audio_response,
            "text_response": response.content,
            "confidence": response.confidence,
            "voice_used": "carlos_mendoza"
        }
        
    except Exception as e:
        logger.error(f"Error generando audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generando audio: {str(e)}")

@router.get("/voices")
async def get_available_voices() -> Dict[str, Any]:
    """Obtener voces disponibles de ElevenLabs"""
    try:
        voices = elevenlabs_service.get_available_voices()
        return {
            "success": True,
            "voices": voices,
            "service_available": elevenlabs_service.is_available
        }
    except Exception as e:
        logger.error(f"Error obteniendo voces: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo voces: {str(e)}")
