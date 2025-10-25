"""
Modelos de datos para análisis financiero
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    INVESTMENT = "investment"

class CategoryType(str, Enum):
    SALES = "sales"
    OPERATING_EXPENSES = "operating_expenses"
    PERSONNEL = "personnel"
    MARKETING = "marketing"
    EQUIPMENT = "equipment"
    UTILITIES = "utilities"
    OTHER = "other"

class FinancialTransaction(BaseModel):
    """Modelo para transacciones financieras"""
    id: Optional[int] = None
    date: date
    amount: float = Field(..., gt=0, description="Monto de la transacción")
    description: str
    category: CategoryType
    transaction_type: TransactionType
    account: Optional[str] = None
    created_at: Optional[datetime] = None

class CashFlowData(BaseModel):
    """Datos de flujo de caja"""
    period: str
    income: float
    expenses: float
    net_cash_flow: float
    cumulative_balance: float

class FinancialMetrics(BaseModel):
    """Métricas financieras calculadas"""
    total_revenue: float
    total_expenses: float
    net_profit: float
    profit_margin: float
    operating_margin: float
    cash_flow_trend: str  # "positive", "negative", "stable"
    expense_breakdown: Dict[str, float]
    revenue_breakdown: Dict[str, float]

class SimulationScenario(BaseModel):
    """Escenario de simulación"""
    name: str
    description: str
    parameters: Dict[str, Any]
    duration_months: int = 12

class SimulationRequest(BaseModel):
    """Solicitud de simulación"""
    scenario: SimulationScenario
    base_data_period: str = "last_12_months"
    include_recommendations: bool = True

class SimulationResult(BaseModel):
    """Resultado de simulación"""
    scenario_name: str
    projected_cash_flow: List[CashFlowData]
    key_metrics: Dict[str, float]
    recommendations: List[str]
    risk_assessment: str
    confidence_score: float = Field(..., ge=0, le=1)

class ChatMessage(BaseModel):
    """Mensaje del chat"""
    message: str
    context: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    """Respuesta del chat"""
    response: str
    analysis: Optional[Dict[str, Any]] = None
    recommendations: Optional[List[str]] = None
    visualizations: Optional[List[str]] = None
    confidence: float = Field(..., ge=0, le=1)

class FinancialData(BaseModel):
    """Datos financieros completos"""
    transactions: List[FinancialTransaction]
    metrics: FinancialMetrics
    cash_flow_history: List[CashFlowData]
    last_updated: datetime

class AnalysisRequest(BaseModel):
    """Solicitud de análisis"""
    analysis_type: str  # "cashflow", "expenses", "revenue", "profitability"
    period: str = "last_12_months"
    include_projections: bool = True
    include_recommendations: bool = True

class AnalysisResponse(BaseModel):
    """Respuesta de análisis"""
    analysis_type: str
    results: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]
    visualizations: List[str]
    confidence: float = Field(..., ge=0, le=1)
