"""
Servicio de datos financieros
Maneja la carga, procesamiento y análisis de datos financieros desde Excel y otras fuentes
"""

import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
import sqlite3
import os
from pathlib import Path
import logging

from app.models.financial_models import (
    FinancialTransaction, FinancialMetrics, CashFlowData, 
    TransactionType, CategoryType
)

logger = logging.getLogger(__name__)

class DataService:
    def __init__(self, db_path: str = "asesor_pyme.db"):
        self.db_path = db_path
        self.data_path = Path("data")
        self.transactions: List[FinancialTransaction] = []
        self.metrics: Optional[FinancialMetrics] = None
        self.cash_flow_history: List[CashFlowData] = []
        
    async def load_financial_data(self):
        """Cargar datos financieros desde archivos Excel"""
        try:
            print("📁 Verificando directorio de datos...")
            # Crear directorio de datos si no existe
            self.data_path.mkdir(exist_ok=True)
            
            print("📊 Intentando cargar datos de empresa...")
            # Intentar cargar datos de empresa
            empresa_data = await self._load_excel_data("finanzas_empresa.xlsx")
            if empresa_data is not None and len(empresa_data) > 0:
                self.transactions.extend(empresa_data)
                print(f"✅ Cargados {len(empresa_data)} transacciones de empresa")
            else:
                print("⚠️ No se pudieron cargar datos de empresa, usando datos de ejemplo")
            
            print("📊 Intentando cargar datos personales...")
            # Intentar cargar datos personales
            personal_data = await self._load_excel_data("finanzas_personales.xlsx")
            if personal_data is not None and len(personal_data) > 0:
                # Filtrar solo transacciones relevantes para PyME
                relevant_personal = [t for t in personal_data if self._is_business_relevant(t)]
                self.transactions.extend(relevant_personal)
                print(f"✅ Cargados {len(relevant_personal)} transacciones personales relevantes")
            else:
                print("⚠️ No se pudieron cargar datos personales")
            
            # Si no hay datos, crear datos de ejemplo
            if len(self.transactions) == 0:
                print("📊 Creando datos de ejemplo...")
                await self._create_sample_data()
            
            print("🧮 Calculando métricas...")
            # Calcular métricas
            await self._calculate_metrics()
            
            print("📈 Generando historial de flujo de caja...")
            # Generar historial de flujo de caja
            await self._generate_cash_flow_history()
            
            print("✅ Datos financieros cargados exitosamente")
            
        except Exception as e:
            print(f"❌ Error al cargar datos financieros: {str(e)}")
            logger.error(f"Error al cargar datos financieros: {str(e)}")
            # Crear datos de ejemplo si no se pueden cargar los reales
            await self._create_sample_data()
    
    async def _load_excel_data(self, filename: str) -> Optional[List[FinancialTransaction]]:
        """Cargar datos desde archivo Excel"""
        file_path = self.data_path / filename
        
        print(f"🔍 Verificando archivo: {file_path}")
        if not file_path.exists():
            print(f"⚠️ Archivo {filename} no encontrado")
            logger.warning(f"Archivo {filename} no encontrado")
            return None
        
        try:
            print(f"📖 Leyendo archivo Excel: {filename}")
            # Leer archivo Excel
            df = pd.read_excel(file_path)
            print(f"✅ Archivo leído exitosamente. Filas: {len(df)}, Columnas: {list(df.columns)}")
            
            if len(df) == 0:
                print(f"⚠️ Archivo {filename} está vacío")
                return None
            
            transactions = []
            print(f"🔄 Procesando {len(df)} filas...")
            for i, row in df.iterrows():
                try:
                    # Mapear columnas del Excel a nuestro modelo
                    transaction = self._map_excel_row_to_transaction(row, filename)
                    if transaction:
                        transactions.append(transaction)
                    if i % 100 == 0 and i > 0:  # Log cada 100 filas
                        print(f"   Procesadas {i+1} filas...")
                except Exception as e:
                    print(f"⚠️ Error procesando fila {i}: {str(e)}")
                    continue
            
            print(f"✅ Procesamiento completado. Transacciones válidas: {len(transactions)}")
            return transactions if len(transactions) > 0 else None
            
        except Exception as e:
            print(f"❌ Error al leer {filename}: {str(e)}")
            logger.error(f"Error al leer {filename}: {str(e)}")
            return None
    
    def _map_excel_row_to_transaction(self, row: pd.Series, filename: str) -> Optional[FinancialTransaction]:
        """Mapear fila de Excel a transacción financiera"""
        try:
            # Detectar columnas comunes en archivos financieros
            amount_col = self._find_column(row, ['amount', 'monto', 'valor', 'importe'])
            date_col = self._find_column(row, ['date', 'fecha', 'fecha_transaccion'])
            desc_col = self._find_column(row, ['description', 'descripcion', 'concepto', 'detalle'])
            category_col = self._find_column(row, ['category', 'categoria', 'tipo'])
            
            if not all([amount_col, date_col, desc_col]):
                return None
            
            # Determinar tipo de transacción basado en el monto y descripción
            amount = float(row[amount_col])
            description = str(row[desc_col]).lower()
            
            if amount > 0:
                transaction_type = TransactionType.INCOME
            else:
                transaction_type = TransactionType.EXPENSE
                amount = abs(amount)
            
            # Mapear categoría
            category = self._map_category(row.get(category_col, ''), description)
            
            # Parsear fecha
            date_value = self._parse_date(row[date_col])
            
            return FinancialTransaction(
                date=date_value,
                amount=amount,
                description=str(row[desc_col]),
                category=category,
                transaction_type=transaction_type,
                created_at=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error al mapear fila: {str(e)}")
            return None
    
    def _find_column(self, row: pd.Series, possible_names: List[str]) -> Optional[str]:
        """Encontrar columna por nombres posibles"""
        for name in possible_names:
            if name in row.index:
                return name
        return None
    
    def _map_category(self, category: str, description: str) -> CategoryType:
        """Mapear categoría de texto a enum"""
        category_lower = category.lower()
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in ['venta', 'ventas', 'sales', 'ingreso']):
            return CategoryType.SALES
        elif any(word in desc_lower for word in ['salario', 'empleado', 'personal', 'nómina']):
            return CategoryType.PERSONNEL
        elif any(word in desc_lower for word in ['marketing', 'publicidad', 'promocion']):
            return CategoryType.MARKETING
        elif any(word in desc_lower for word in ['equipo', 'maquinaria', 'computadora']):
            return CategoryType.EQUIPMENT
        elif any(word in desc_lower for word in ['luz', 'agua', 'telefono', 'internet']):
            return CategoryType.UTILITIES
        else:
            return CategoryType.OTHER
    
    def _parse_date(self, date_value) -> date:
        """Parsear fecha desde diferentes formatos"""
        if isinstance(date_value, date):
            return date_value
        elif isinstance(date_value, datetime):
            return date_value.date()
        elif isinstance(date_value, str):
            try:
                return datetime.strptime(date_value, '%Y-%m-%d').date()
            except:
                try:
                    return datetime.strptime(date_value, '%d/%m/%Y').date()
                except:
                    return date.today()
        else:
            return date.today()
    
    def _is_business_relevant(self, transaction: FinancialTransaction) -> bool:
        """Determinar si una transacción personal es relevante para el negocio"""
        # Filtrar transacciones muy pequeñas o personales
        if transaction.amount < 100:
            return False
        
        # Incluir transacciones de inversión o gastos significativos
        if transaction.transaction_type == TransactionType.INVESTMENT:
            return True
        
        # Incluir gastos que podrían ser empresariales
        business_keywords = ['oficina', 'equipo', 'software', 'servicio', 'profesional']
        if any(keyword in transaction.description.lower() for keyword in business_keywords):
            return True
        
        return False
    
    async def _calculate_metrics(self):
        """Calcular métricas financieras"""
        if not self.transactions:
            return
        
        df = pd.DataFrame([t.dict() for t in self.transactions])
        
        # Calcular métricas básicas
        total_revenue = df[df['transaction_type'] == TransactionType.INCOME]['amount'].sum()
        total_expenses = df[df['transaction_type'] == TransactionType.EXPENSE]['amount'].sum()
        net_profit = total_revenue - total_expenses
        
        # Calcular márgenes
        profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
        operating_margin = ((total_revenue - total_expenses) / total_revenue * 100) if total_revenue > 0 else 0
        
        # Análisis de tendencia de flujo de caja
        recent_months = self._get_recent_cash_flow_trend()
        
        # Desglose de gastos por categoría
        expense_breakdown = df[df['transaction_type'] == TransactionType.EXPENSE].groupby('category')['amount'].sum().to_dict()
        
        # Desglose de ingresos por categoría
        revenue_breakdown = df[df['transaction_type'] == TransactionType.INCOME].groupby('category')['amount'].sum().to_dict()
        
        self.metrics = FinancialMetrics(
            total_revenue=total_revenue,
            total_expenses=total_expenses,
            net_profit=net_profit,
            profit_margin=profit_margin,
            operating_margin=operating_margin,
            cash_flow_trend=recent_months,
            expense_breakdown=expense_breakdown,
            revenue_breakdown=revenue_breakdown
        )
    
    def _get_recent_cash_flow_trend(self) -> str:
        """Analizar tendencia reciente del flujo de caja"""
        if len(self.transactions) < 6:
            return "stable"
        
        # Obtener últimos 3 meses
        recent_date = datetime.now().date() - timedelta(days=90)
        recent_transactions = [t for t in self.transactions if t.date >= recent_date]
        
        if len(recent_transactions) < 3:
            return "stable"
        
        # Calcular flujo neto mensual
        monthly_flows = {}
        for t in recent_transactions:
            month_key = t.date.strftime('%Y-%m')
            if month_key not in monthly_flows:
                monthly_flows[month_key] = 0
            
            if t.transaction_type == TransactionType.INCOME:
                monthly_flows[month_key] += t.amount
            else:
                monthly_flows[month_key] -= t.amount
        
        flows = list(monthly_flows.values())
        if len(flows) < 2:
            return "stable"
        
        # Determinar tendencia
        if flows[-1] > flows[-2] > flows[-3] if len(flows) >= 3 else flows[-1] > flows[-2]:
            return "positive"
        elif flows[-1] < flows[-2] < flows[-3] if len(flows) >= 3 else flows[-1] < flows[-2]:
            return "negative"
        else:
            return "stable"
    
    async def _generate_cash_flow_history(self):
        """Generar historial de flujo de caja mensual"""
        if not self.transactions:
            return
        
        # Agrupar por mes
        monthly_data = {}
        cumulative_balance = 0
        
        for transaction in self.transactions:
            month_key = transaction.date.strftime('%Y-%m')
            if month_key not in monthly_data:
                monthly_data[month_key] = {'income': 0, 'expenses': 0}
            
            if transaction.transaction_type == TransactionType.INCOME:
                monthly_data[month_key]['income'] += transaction.amount
            else:
                monthly_data[month_key]['expenses'] += transaction.amount
        
        # Crear historial ordenado
        for period in sorted(monthly_data.keys()):
            data = monthly_data[period]
            net_flow = data['income'] - data['expenses']
            cumulative_balance += net_flow
            
            self.cash_flow_history.append(CashFlowData(
                period=period,
                income=data['income'],
                expenses=data['expenses'],
                net_cash_flow=net_flow,
                cumulative_balance=cumulative_balance
            ))
    
    async def _create_sample_data(self):
        """Crear datos de ejemplo para demostración"""
        logger.info("Creando datos de ejemplo...")
        
        # Crear transacciones de ejemplo para los últimos 12 meses
        base_date = datetime.now().date()
        
        sample_transactions = [
            # Ingresos mensuales
            FinancialTransaction(
                date=base_date - timedelta(days=30),
                amount=50000,
                description="Ventas del mes",
                category=CategoryType.SALES,
                transaction_type=TransactionType.INCOME
            ),
            FinancialTransaction(
                date=base_date - timedelta(days=60),
                amount=48000,
                description="Ventas del mes",
                category=CategoryType.SALES,
                transaction_type=TransactionType.INCOME
            ),
            FinancialTransaction(
                date=base_date - timedelta(days=90),
                amount=52000,
                description="Ventas del mes",
                category=CategoryType.SALES,
                transaction_type=TransactionType.INCOME
            ),
            
            # Gastos operativos
            FinancialTransaction(
                date=base_date - timedelta(days=25),
                amount=15000,
                description="Salarios personal",
                category=CategoryType.PERSONNEL,
                transaction_type=TransactionType.EXPENSE
            ),
            FinancialTransaction(
                date=base_date - timedelta(days=20),
                amount=5000,
                description="Renta oficina",
                category=CategoryType.OPERATING_EXPENSES,
                transaction_type=TransactionType.EXPENSE
            ),
            FinancialTransaction(
                date=base_date - timedelta(days=15),
                amount=2000,
                description="Servicios públicos",
                category=CategoryType.UTILITIES,
                transaction_type=TransactionType.EXPENSE
            ),
        ]
        
        self.transactions = sample_transactions
        await self._calculate_metrics()
        await self._generate_cash_flow_history()
    
    async def get_data_summary(self) -> Dict[str, Any]:
        """Obtener resumen de datos disponibles"""
        return {
            "total_transactions": len(self.transactions),
            "date_range": {
                "start": min(t.date for t in self.transactions) if self.transactions else None,
                "end": max(t.date for t in self.transactions) if self.transactions else None
            },
            "metrics_available": self.metrics is not None,
            "cash_flow_periods": len(self.cash_flow_history),
            "data_sources": ["finanzas_empresa.xlsx", "finanzas_personales.xlsx"],
            "last_updated": datetime.now().isoformat()
        }
    
    async def close(self):
        """Cerrar conexiones y limpiar recursos"""
        pass
