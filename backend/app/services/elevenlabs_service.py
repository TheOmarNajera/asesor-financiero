"""
Servicio de ElevenLabs para síntesis de voz
Convierte respuestas del chat en audio natural usando IA
"""

import os
import logging
from typing import Optional, Dict, Any
import requests
import base64
from io import BytesIO
from elevenlabs import Voice, VoiceSettings, generate, set_api_key
from elevenlabs.api import Voices
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)

class ElevenLabsService:
    """Servicio para síntesis de voz con ElevenLabs"""
    
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.is_available = False
        
        if self.api_key:
            try:
                set_api_key(self.api_key)
                self.is_available = True
                logger.info("✅ ElevenLabs configurado correctamente")
            except Exception as e:
                logger.error(f"❌ Error configurando ElevenLabs: {e}")
                self.is_available = False
        else:
            logger.warning("⚠️ ELEVENLABS_API_KEY no configurada")
    
    def get_available_voices(self) -> list:
        """Obtener voces disponibles"""
        if not self.is_available:
            return []
        
        try:
            voices = Voices.from_api()
            return [
                {
                    'voice_id': voice.voice_id,
                    'name': voice.name,
                    'category': voice.category,
                    'description': voice.description
                }
                for voice in voices
            ]
        except Exception as e:
            logger.error(f"❌ Error obteniendo voces: {e}")
            return []
    
    def generate_speech(self, text: str, voice_id: str = None, voice_settings: Dict[str, Any] = None) -> Optional[bytes]:
        """Generar audio a partir de texto"""
        if not self.is_available:
            logger.warning("⚠️ ElevenLabs no disponible, usando modo simulado")
            return None
        
        try:
            # Configuración de voz por defecto para Carlos Mendoza (asesor Banorte)
            if not voice_id:
                voice_id = "pNInz6obpgDQGcFmaJgB"  # Voz masculina profesional
            
            if not voice_settings:
                voice_settings = VoiceSettings(
                    stability=0.75,  # Estabilidad alta para voz profesional
                    similarity_boost=0.8,  # Similaridad alta
                    style=0.2,  # Estilo conservador
                    use_speaker_boost=True  # Mejorar claridad
                )
            
            # Generar audio
            audio = generate(
                text=text,
                voice=Voice(
                    voice_id=voice_id,
                    settings=voice_settings
                ),
                model="eleven_multilingual_v2"  # Modelo multilingüe
            )
            
            logger.info(f"✅ Audio generado: {len(text)} caracteres")
            return audio
            
        except Exception as e:
            logger.error(f"❌ Error generando audio: {e}")
            return None
    
    def generate_carlos_voice(self, text: str) -> Optional[bytes]:
        """Generar voz específica para Maya (asesora Banorte)"""
        if not self.is_available:
            return None
        
        try:
            # Configuración específica para Maya
            carlos_settings = VoiceSettings(
                stability=0.8,  # Muy estable para voz profesional
                similarity_boost=0.9,  # Alta similaridad
                style=0.1,  # Estilo muy conservador
                use_speaker_boost=True
            )
            
            # Usar voz masculina profesional
            carlos_voice_id = "pNInz6obpgDQGcFmaJgB"  # Adam - voz masculina profesional
            
            # Limitar longitud para ahorrar créditos (máximo 500 caracteres)
            truncated_text = text[:500] if len(text) > 500 else text
            if len(text) > 500:
                truncated_text += "..."
                logger.warning(f"⚠️ Audio truncado para ahorrar créditos: {len(text)} → {len(truncated_text)} caracteres")
            
            audio = generate(
                text=truncated_text,
                voice=Voice(
                    voice_id=carlos_voice_id,
                    settings=carlos_settings
                ),
                model="eleven_monolingual_v1"  # Modelo más económico para español
            )
            
            logger.info(f"🎤 Voz de Maya generada: {len(text)} caracteres")
            return audio
            
        except Exception as e:
            logger.error(f"❌ Error generando voz de Maya: {e}")
            return None
    
    def generate_financial_advice_audio(self, advice_text: str) -> Optional[bytes]:
        """Generar audio para consejos financieros con tono profesional"""
        if not self.is_available:
            return None
        
        try:
            # Configuración para consejos financieros
            advice_settings = VoiceSettings(
                stability=0.85,  # Muy estable
                similarity_boost=0.85,  # Alta similaridad
                style=0.15,  # Ligeramente más expresivo
                use_speaker_boost=True
            )
            
            # Voz profesional para consejos
            advice_voice_id = "pNInz6obpgDQGcFmaJgB"  # Adam
            
            # Limitar longitud
            truncated_advice = advice_text[:500] if len(advice_text) > 500 else advice_text
            if len(advice_text) > 500:
                truncated_advice += "..."
                logger.warning(f"⚠️ Audio de consejo truncado: {len(advice_text)} → {len(truncated_advice)} caracteres")
            
            audio = generate(
                text=truncated_advice,
                voice=Voice(
                    voice_id=advice_voice_id,
                    settings=advice_settings
                ),
                model="eleven_monolingual_v1"  # Modelo más económico
            )
            
            logger.info(f"💰 Audio de consejo financiero generado")
            return audio
            
        except Exception as e:
            logger.error(f"❌ Error generando audio de consejo: {e}")
            return None
    
    def create_audio_response(self, chat_response: str, response_type: str = "general") -> Optional[Dict[str, Any]]:
        """Crear respuesta de audio completa"""
        if not self.is_available:
            return None
        
        try:
            # Seleccionar método según tipo de respuesta
            if response_type == "carlos":
                audio_data = self.generate_carlos_voice(chat_response)
            elif response_type == "advice":
                audio_data = self.generate_financial_advice_audio(chat_response)
            else:
                audio_data = self.generate_speech(chat_response)
            
            if audio_data:
                # Convertir a base64 para envío
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                
                return {
                    'audio_data': audio_base64,
                    'audio_format': 'mp3',
                    'duration_estimate': len(chat_response) * 0.1,  # Estimación aproximada
                    'voice_used': 'carlos_mendoza' if response_type == "carlos" else 'professional',
                    'text_length': len(chat_response)
                }
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error creando respuesta de audio: {e}")
            return None
    
    def get_voice_preview(self, voice_id: str, sample_text: str = "Hola, soy Maya, tu asesora financiera de Banorte") -> Optional[bytes]:
        """Generar preview de voz"""
        if not self.is_available:
            return None
        
        try:
            audio = generate(
                text=sample_text,
                voice=Voice(voice_id=voice_id),
                model="eleven_multilingual_v2"
            )
            
            return audio
            
        except Exception as e:
            logger.error(f"❌ Error generando preview: {e}")
            return None

# Instancia global del servicio
elevenlabs_service = ElevenLabsService()
