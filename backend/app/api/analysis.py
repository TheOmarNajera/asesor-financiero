"""
Endpoints para análisis financiero
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
import logging

from app.models.financial_models import AnalysisRequest, AnalysisResponse, FinancialMetrics
from app.services.data_service import DataService
from app.services.gemini_service import GeminiService

logger = logging.getLogger(__name__)
router = APIRouter()

def get_data_service() -> DataService:
    """Dependency para obtener el servicio de datos"""
    # En una implementación real, esto vendría del contexto de la app
    return DataService()

def get_gemini_service() -> GeminiService:
    """Dependency para obtener el servicio de Gemini"""
    return GeminiService()

@router.get("/cashflow")
async def analyze_cashflow(
    period: str = "last_12_months",
    data_service: DataService = Depends(get_data_service)
) -> Dict[str, Any]:
    """Analizar flujo de caja"""
    try:
        if not data_service.cash_flow_history:
            raise HTTPException(status_code=404, detail="No hay datos de flujo de caja disponibles")
        
        # Filtrar por período
        filtered_data = data_service.cash_flow_history
        if period == "last_6_months":
            filtered_data = filtered_data[-6:]
        elif period == "last_3_months":
            filtered_data = filtered_data[-3:]
        
        # Calcular métricas de flujo de caja
        total_income = sum(cf.income for cf in filtered_data)
        total_expenses = sum(cf.expenses for cf in filtered_data)
        avg_monthly_flow = sum(cf.net_cash_flow for cf in filtered_data) / len(filtered_data) if filtered_data else 0
        
        # Determinar tendencia
        if len(filtered_data) >= 2:
            recent_trend = "positive" if filtered_data[-1].net_cash_flow > filtered_data[-2].net_cash_flow else "negative"
        else:
            recent_trend = "stable"
        
        return {
            "period": period,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_cash_flow": total_income - total_expenses,
            "average_monthly_flow": avg_monthly_flow,
            "trend": recent_trend,
            "monthly_data": [cf.dict() for cf in filtered_data],
            "insights": [
                f"Flujo de caja promedio mensual: ${avg_monthly_flow:,.2f}",
                f"Tendencia reciente: {'Positiva' if recent_trend == 'positive' else 'Negativa' if recent_trend == 'negative' else 'Estable'}",
                f"Total de ingresos en el período: ${total_income:,.2f}",
                f"Total de gastos en el período: ${total_expenses:,.2f}"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error en análisis de flujo de caja: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en análisis: {str(e)}")

@router.get("/expenses")
async def analyze_expenses(
    period: str = "last_12_months",
    data_service: DataService = Depends(get_data_service)
) -> Dict[str, Any]:
    """Analizar gastos por categoría"""
    try:
        if not data_service.transactions:
            raise HTTPException(status_code=404, detail="No hay datos de transacciones disponibles")
        
        # Filtrar gastos
        expenses = [t for t in data_service.transactions if t.transaction_type.value == "expense"]
        
        # Agrupar por categoría
        category_totals = {}
        for expense in expenses:
            category = expense.category.value
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += expense.amount
        
        # Calcular porcentajes
        total_expenses = sum(category_totals.values())
        category_percentages = {
            category: (amount / total_expenses * 100) if total_expenses > 0 else 0
            for category, amount in category_totals.items()
        }
        
        # Identificar categorías con mayor gasto
        top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "period": period,
            "total_expenses": total_expenses,
            "category_breakdown": category_totals,
            "category_percentages": category_percentages,
            "top_categories": [{"category": cat, "amount": amount, "percentage": category_percentages[cat]} 
                             for cat, amount in top_categories],
            "insights": [
                f"Gasto total en el período: ${total_expenses:,.2f}",
                f"Categoría con mayor gasto: {top_categories[0][0]} (${top_categories[0][1]:,.2f})" if top_categories else "Sin datos",
                f"Número de categorías de gasto: {len(category_totals)}"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error en análisis de gastos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en análisis: {str(e)}")

@router.get("/revenue")
async def analyze_revenue(
    period: str = "last_12_months",
    data_service: DataService = Depends(get_data_service)
) -> Dict[str, Any]:
    """Analizar ingresos por categoría"""
    try:
        if not data_service.transactions:
            raise HTTPException(status_code=404, detail="No hay datos de transacciones disponibles")
        
        # Filtrar ingresos
        revenues = [t for t in data_service.transactions if t.transaction_type.value == "income"]
        
        # Agrupar por categoría
        category_totals = {}
        for revenue in revenues:
            category = revenue.category.value
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += revenue.amount
        
        # Calcular métricas
        total_revenue = sum(category_totals.values())
        avg_monthly_revenue = total_revenue / 12  # Asumiendo 12 meses
        
        # Identificar categorías principales
        top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "period": period,
            "total_revenue": total_revenue,
            "average_monthly_revenue": avg_monthly_revenue,
            "category_breakdown": category_totals,
            "top_categories": [{"category": cat, "amount": amount} 
                             for cat, amount in top_categories],
            "insights": [
                f"Ingresos totales en el período: ${total_revenue:,.2f}",
                f"Ingreso promedio mensual: ${avg_monthly_revenue:,.2f}",
                f"Categoría principal de ingresos: {top_categories[0][0]} (${top_categories[0][1]:,.2f})" if top_categories else "Sin datos"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error en análisis de ingresos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en análisis: {str(e)}")

@router.get("/profitability")
async def analyze_profitability(
    data_service: DataService = Depends(get_data_service)
) -> Dict[str, Any]:
    """Analizar rentabilidad general"""
    try:
        if not data_service.metrics:
            raise HTTPException(status_code=404, detail="No hay métricas disponibles")
        
        metrics = data_service.metrics
        
        # Calcular métricas adicionales
        revenue_growth = 0  # Placeholder - necesitaría datos históricos
        expense_efficiency = (metrics.total_revenue - metrics.total_expenses) / metrics.total_revenue * 100 if metrics.total_revenue > 0 else 0
        
        return {
            "total_revenue": metrics.total_revenue,
            "total_expenses": metrics.total_expenses,
            "net_profit": metrics.net_profit,
            "profit_margin": metrics.profit_margin,
            "operating_margin": metrics.operating_margin,
            "expense_efficiency": expense_efficiency,
            "cash_flow_trend": metrics.cash_flow_trend,
            "revenue_growth": revenue_growth,
            "insights": [
                f"Margen de ganancia: {metrics.profit_margin:.1f}%",
                f"Margen operativo: {metrics.operating_margin:.1f}%",
                f"Eficiencia de gastos: {expense_efficiency:.1f}%",
                f"Tendencia de flujo de caja: {metrics.cash_flow_trend}"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error en análisis de rentabilidad: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en análisis: {str(e)}")

@router.post("/comprehensive")
async def comprehensive_analysis(
    request: AnalysisRequest,
    data_service: DataService = Depends(get_data_service),
    gemini_service: GeminiService = Depends(get_gemini_service)
) -> AnalysisResponse:
    """Análisis financiero comprehensivo con IA"""
    try:
        # Obtener datos base
        context = {
            "metrics": data_service.metrics.dict() if data_service.metrics else {},
            "cash_flow": [cf.dict() for cf in data_service.cash_flow_history[-3:]],
            "expense_breakdown": data_service.metrics.expense_breakdown if data_service.metrics else {},
            "revenue_breakdown": data_service.metrics.revenue_breakdown if data_service.metrics else {}
        }
        
        # Generar análisis con IA
        analysis_text = await gemini_service.generate_simulation_analysis(
            {"name": f"Análisis {request.analysis_type}", "description": f"Análisis de {request.analysis_type}"},
            context
        )
        
        # Generar insights específicos
        insights = []
        if request.analysis_type == "cashflow":
            insights = [
                "El flujo de caja muestra tendencia estable",
                "Se recomienda mantener reservas de emergencia",
                "Considerar optimización de gastos operativos"
            ]
        elif request.analysis_type == "expenses":
            insights = [
                "Los gastos están distribuidos en múltiples categorías",
                "Oportunidad de optimización en gastos operativos",
                "Revisar contratos de servicios periódicamente"
            ]
        
        return AnalysisResponse(
            analysis_type=request.analysis_type,
            results=context,
            insights=insights,
            recommendations=[
                "Monitorear métricas mensualmente",
                "Establecer presupuestos por categoría",
                "Revisar gastos trimestralmente"
            ],
            visualizations=[f"{request.analysis_type}_chart"],
            confidence=0.8
        )
        
    except Exception as e:
        logger.error(f"Error en análisis comprehensivo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en análisis: {str(e)}")
