"""
Asesor PyME Inteligente - Servidor MCP Principal
Servidor FastAPI que proporciona análisis financiero inteligente usando Google Gemini
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from app.api import analysis, simulations, chat, transactions
from app.services.data_service import DataService
from app.services.gemini_service import GeminiService
from app.models.financial_models import FinancialData, SimulationRequest, ChatMessage

# Cargar variables de entorno (busca en el directorio actual primero)
load_dotenv()  # Busca .env en el directorio actual (backend)

# Servicios globales
data_service = None
gemini_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializar servicios al startup"""
    global data_service, gemini_service
    
    try:
        print("🚀 Iniciando servicios...")
        
        # Inicializar servicios
        data_service = DataService()
        gemini_service = GeminiService()
        
        print("📊 Cargando datos financieros...")
        # Cargar datos iniciales
        await data_service.load_financial_data()
        
        print("✅ Servicios inicializados correctamente")
        
    except Exception as e:
        print(f"❌ Error durante la inicialización: {str(e)}")
        # Continuar sin datos si hay error
        data_service = None
        gemini_service = None
    
    yield
    
    # Cleanup al shutdown
    if data_service:
        await data_service.close()

# Crear aplicación FastAPI
app = FastAPI(
    title="Asesor PyME Inteligente",
    description="Servidor MCP para análisis financiero inteligente con IA",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080", "http://172.20.10.10:3000", "http://172.20.10.10"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(analysis.router, prefix="/api/analysis", tags=["Análisis Financiero"])
app.include_router(simulations.router, prefix="/api/simulations", tags=["Simulaciones"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat Inteligente"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["Transacciones"])

@app.get("/")
async def root():
    """Endpoint raíz con información del servidor"""
    return {
        "message": "Asesor PyME Inteligente - Servidor MCP",
        "version": "1.0.0",
        "status": "active",
        "features": [
            "Análisis financiero inteligente",
            "Simulaciones What-If",
            "Chat conversacional con IA",
            "Proyecciones y recomendaciones"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "data_service": data_service is not None,
            "gemini_service": gemini_service is not None
        }
    }

@app.get("/api/data/summary")
async def get_data_summary():
    """Obtener resumen de datos financieros disponibles"""
    if not data_service:
        raise HTTPException(status_code=503, detail="Servicio de datos no disponible")
    
    try:
        summary = await data_service.get_data_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener resumen: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )
