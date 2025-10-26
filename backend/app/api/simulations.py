"""
Endpoints para simulaciones financieras What-If
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta

from app.models.financial_models import SimulationRequest, SimulationResult, SimulationScenario
from app.services.data_service import DataService
from app.services.gemini_service import GeminiService

logger = logging.getLogger(__name__)
router = APIRouter()

def get_data_service(empresa_id: Optional[str] = Header(None, alias="X-Empresa-ID")) -> DataService:
    """Dependency para obtener el servicio de datos con empresa_id del header"""
    empresa = empresa_id or "E001"
    return DataService(empresa_id=empresa)

def get_gemini_service() -> GeminiService:
    return GeminiService()

@router.post("/scenario")
async def create_simulation(
    request: SimulationRequest,
    data_service: DataService = Depends(get_data_service),
    gemini_service: GeminiService = Depends(get_gemini_service)
) -> SimulationResult:
    """Crear nueva simulación financiera"""
    try:
        # Obtener datos base
        base_data = {
            "monthly_revenue": data_service.metrics.total_revenue / 12 if data_service.metrics else 0,
            "monthly_expenses": data_service.metrics.total_expenses / 12 if data_service.metrics else 0,
            "net_cash_flow": (data_service.metrics.total_revenue - data_service.metrics.total_expenses) / 12 if data_service.metrics else 0
        }
        
        # Ejecutar simulación
        simulation_data = await _run_simulation(request.scenario, base_data, request.scenario.duration_months)
        
        # Generar análisis con IA
        analysis = await gemini_service.generate_simulation_analysis(request.scenario.dict(), base_data)
        
        # Calcular métricas clave
        key_metrics = _calculate_key_metrics(simulation_data)
        
        # Generar recomendaciones
        recommendations = _generate_recommendations(simulation_data, request.scenario)
        
        # Evaluar riesgo
        risk_assessment = _assess_risk(simulation_data)
        
        return SimulationResult(
            scenario_name=request.scenario.name,
            projected_cash_flow=simulation_data,
            key_metrics=key_metrics,
            recommendations=recommendations,
            risk_assessment=risk_assessment,
            confidence_score=0.8
        )
        
    except Exception as e:
        logger.error(f"Error en simulación: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en simulación: {str(e)}")

async def _run_simulation(scenario: SimulationScenario, base_data: Dict[str, Any], duration_months: int) -> List[Dict[str, Any]]:
    """Ejecutar simulación financiera"""
    simulation_data = []
    
    # Parámetros base
    base_revenue = base_data["monthly_revenue"]
    base_expenses = base_data["monthly_expenses"]
    base_net_flow = base_data["net_cash_flow"]
    
    # Aplicar parámetros del escenario
    parameters = scenario.parameters
    
    # Modificadores de ingresos
    revenue_multiplier = parameters.get("revenue_change_percent", 0) / 100
    revenue_growth_rate = parameters.get("revenue_growth_rate", 0) / 100
    
    # Modificadores de gastos
    expense_multiplier = parameters.get("expense_change_percent", 0) / 100
    new_expense_monthly = parameters.get("new_monthly_expense", 0)
    
    # Simular cada mes
    cumulative_balance = 0
    for month in range(duration_months):
        # Calcular ingresos del mes
        monthly_revenue = base_revenue * (1 + revenue_multiplier + (revenue_growth_rate * month))
        
        # Calcular gastos del mes
        monthly_expenses = base_expenses * (1 + expense_multiplier) + new_expense_monthly
        
        # Calcular flujo neto
        net_cash_flow = monthly_revenue - monthly_expenses
        cumulative_balance += net_cash_flow
        
        # Crear entrada de datos
        month_data = {
            "period": f"Mes {month + 1}",
            "income": monthly_revenue,
            "expenses": monthly_expenses,
            "net_cash_flow": net_cash_flow,
            "cumulative_balance": cumulative_balance
        }
        
        simulation_data.append(month_data)
    
    return simulation_data

def _calculate_key_metrics(simulation_data: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calcular métricas clave de la simulación"""
    if not simulation_data:
        return {}
    
    total_income = sum(month["income"] for month in simulation_data)
    total_expenses = sum(month["expenses"] for month in simulation_data)
    net_cash_flow = sum(month["net_cash_flow"] for month in simulation_data)
    
    # Calcular tendencia
    first_month_flow = simulation_data[0]["net_cash_flow"]
    last_month_flow = simulation_data[-1]["net_cash_flow"]
    trend_percentage = ((last_month_flow - first_month_flow) / first_month_flow * 100) if first_month_flow != 0 else 0
    
    # Calcular punto de equilibrio (mes donde el balance se vuelve positivo)
    break_even_month = None
    for i, month in enumerate(simulation_data):
        if month["cumulative_balance"] >= 0:
            break_even_month = i + 1
            break
    
    return {
        "total_projected_income": total_income,
        "total_projected_expenses": total_expenses,
        "net_projected_cash_flow": net_cash_flow,
        "average_monthly_flow": net_cash_flow / len(simulation_data),
        "trend_percentage": trend_percentage,
        "break_even_month": break_even_month,
        "final_balance": simulation_data[-1]["cumulative_balance"]
    }

def _generate_recommendations(simulation_data: List[Dict[str, Any]], scenario: SimulationScenario) -> List[str]:
    """Generar recomendaciones basadas en la simulación"""
    recommendations = []
    
    if not simulation_data:
        return ["No hay datos suficientes para generar recomendaciones"]
    
    # Analizar flujo de caja
    negative_months = [month for month in simulation_data if month["net_cash_flow"] < 0]
    if negative_months:
        recommendations.append(f"Preparar financiamiento para {len(negative_months)} meses con flujo negativo")
    
    # Analizar balance final
    final_balance = simulation_data[-1]["cumulative_balance"]
    if final_balance < 0:
        recommendations.append("Considerar ajustar parámetros del escenario para evitar balance negativo")
    elif final_balance > 0:
        recommendations.append("El escenario es financieramente viable")
    
    # Analizar tendencia
    first_flow = simulation_data[0]["net_cash_flow"]
    last_flow = simulation_data[-1]["net_cash_flow"]
    if last_flow > first_flow:
        recommendations.append("El escenario muestra tendencia positiva")
    elif last_flow < first_flow:
        recommendations.append("Monitorear de cerca la tendencia negativa")
    
    # Recomendaciones específicas por tipo de escenario
    scenario_name = scenario.name.lower()
    if "contratación" in scenario_name or "empleado" in scenario_name:
        recommendations.extend([
            "Considerar período de prueba antes de contratación permanente",
            "Evaluar impacto en productividad y ingresos",
            "Preparar plan de contingencia en caso de necesidad de reducción"
        ])
    elif "inversión" in scenario_name or "compra" in scenario_name:
        recommendations.extend([
            "Evaluar opciones de financiamiento",
            "Considerar leasing como alternativa",
            "Calcular período de recuperación de inversión"
        ])
    
    return recommendations[:5]  # Máximo 5 recomendaciones

def _assess_risk(simulation_data: List[Dict[str, Any]]) -> str:
    """Evaluar nivel de riesgo de la simulación"""
    if not simulation_data:
        return "Alto - Sin datos suficientes"
    
    # Calcular métricas de riesgo
    negative_months = len([month for month in simulation_data if month["net_cash_flow"] < 0])
    total_months = len(simulation_data)
    negative_percentage = (negative_months / total_months) * 100
    
    final_balance = simulation_data[-1]["cumulative_balance"]
    
    # Determinar nivel de riesgo
    if negative_percentage > 50 or final_balance < -10000:
        return "Alto - Múltiples meses con flujo negativo o balance muy negativo"
    elif negative_percentage > 25 or final_balance < 0:
        return "Medio - Algunos meses problemáticos o balance negativo"
    else:
        return "Bajo - Flujo de caja estable y balance positivo"

@router.get("/history")
async def get_simulation_history(
    data_service: DataService = Depends(get_data_service)
) -> List[Dict[str, Any]]:
    """Obtener historial de simulaciones"""
    # En una implementación real, esto vendría de una base de datos
    return [
        {
            "id": 1,
            "name": "Contratación de nuevo empleado",
            "created_at": "2024-01-15T10:30:00Z",
            "status": "completed",
            "risk_level": "Medio"
        },
        {
            "id": 2,
            "name": "Inversión en nueva maquinaria",
            "created_at": "2024-01-10T14:20:00Z",
            "status": "completed",
            "risk_level": "Alto"
        }
    ]

@router.get("/{simulation_id}")
async def get_simulation_result(
    simulation_id: int,
    data_service: DataService = Depends(get_data_service)
) -> Dict[str, Any]:
    """Obtener resultado de simulación específica"""
    # En una implementación real, esto vendría de una base de datos
    if simulation_id == 1:
        return {
            "id": simulation_id,
            "name": "Contratación de nuevo empleado",
            "results": {
                "total_projected_income": 600000,
                "total_projected_expenses": 580000,
                "net_projected_cash_flow": 20000,
                "risk_assessment": "Medio"
            },
            "recommendations": [
                "Es viable contratar el empleado",
                "Monitorear impacto en los primeros 3 meses",
                "Considerar período de prueba"
            ]
        }
    else:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")
