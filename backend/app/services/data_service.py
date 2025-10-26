"""
Servicio de datos financieros
Maneja la carga, procesamiento y análisis de datos financieros desde Excel, Snowflake y otras fuentes
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
from app.services.snowflake_service import snowflake_service

logger = logging.getLogger(__name__)

# Caché global por empresa
_data_cache: Dict[str, Dict[str, Any]] = {}

class DataService:
    def __init__(self, db_path: str = "asesor_pyme.db", use_snowflake: bool = True, empresa_id: str = None):
        self.db_path = db_path
        self.data_path = Path("data")
        self.empresa_id = empresa_id or os.getenv("DEFAULT_EMPRESA_ID", "E001")
        self.transactions: List[FinancialTransaction] = []
        self.metrics: Optional[FinancialMetrics] = None
        self.cash_flow_history: List[CashFlowData] = []
        self.use_snowflake = use_snowflake
        self.snowflake_connected = False
        self.data_loaded = False  # Flag para saber si los datos ya fueron cargados
        self.use_sample_data = os.getenv("USE_SAMPLE_DATA", "true").lower() == "true"  # TRUE por defecto
        self.skip_excel_loading = os.getenv("SKIP_EXCEL_LOADING", "true").lower() == "true"  # TRUE por defecto
        
        # Verificar si ya tenemos datos en caché para esta empresa
        if self.empresa_id in _data_cache:
            cached_data = _data_cache[self.empresa_id]
            self.transactions = cached_data.get('transactions', [])
            self.metrics = cached_data.get('metrics')
            self.cash_flow_history = cached_data.get('cash_flow_history', [])
            self.data_loaded = True
            print(f"📊 Datos cargados desde caché para empresa {self.empresa_id}: {len(self.transactions)} transacciones")
        
        # SIEMPRE usar datos de ejemplo por defecto (rápido y eficiente)
        # No intentar conectar con Snowflake ni cargar Excel a menos que se especifique explícitamente
        if self.use_sample_data:
            logger.info("📊 Modo de datos de ejemplo activado - omitiendo Snowflake y Excel")
            self.use_snowflake = False
        else:
            # Intentar conectar con Snowflake SOLO si el usuario lo solicita explícitamente
            if self.use_snowflake:
                self.snowflake_connected = snowflake_service.connect()
                if self.snowflake_connected:
                    snowflake_service.create_tables()
                    logger.info("✅ Snowflake habilitado y conectado")
                else:
                    logger.warning("⚠️ Snowflake no disponible, usando datos de ejemplo por defecto")
                    self.use_sample_data = True
        
    async def load_financial_data(self):
        """Cargar datos financieros de manera eficiente (solo una vez)"""
        if self.data_loaded:
            print("📊 Datos ya cargados, omitiendo carga...")
            return
            
        try:
            # Si está en modo de datos de ejemplo, cargar directamente
            if self.use_sample_data:
                print("📊 Modo rápido: Cargando datos de ejemplo...")
                self.transactions = self._load_sample_data()
                print(f"✅ Cargados {len(self.transactions)} transacciones de ejemplo")
            else:
                # Intentar Snowflake primero
                if self.use_snowflake and self.snowflake_connected:
                    print("📊 Cargando datos desde Snowflake...")
                    # Usar E001 como default (tiene datos reales en ROW_DATA_EMPRESA)
                    # TODO: Debería venir del JWT del usuario logueado
                    empresa_id = os.getenv("DEFAULT_EMPRESA_ID", "E001")
                    snowflake_transactions = snowflake_service.get_transactions(empresa_id)
                    if snowflake_transactions:
                        self.transactions = [FinancialTransaction(**t) for t in snowflake_transactions]
                        print(f"✅ Cargados {len(self.transactions)} transacciones desde Snowflake")
                    else:
                        print("⚠️ No se encontraron datos en Snowflake")
                        # SIEMPRE usar datos de ejemplo si no hay datos en Snowflake (NO procesar Excel)
                        print("📊 Saltando carga de Excel, usando datos de ejemplo...")
                        self.transactions = self._load_sample_data()
                else:
                    # Si no hay Snowflake disponible, usar datos de ejemplo directamente
                    print("📊 Snowflake no disponible, usando datos de ejemplo...")
                    self.transactions = self._load_sample_data()

                # Si aún no hay transacciones, usar datos de ejemplo como fallback
                if not self.transactions:
                    print("📊 Fallback: Cargando datos de ejemplo...")
                    self.transactions = self._load_sample_data()

            # Procesar datos
            self.transactions.sort(key=lambda t: t.date)
            self.metrics = self._calculate_metrics()
            self.cash_flow_history = self._calculate_cash_flow_history()
            
            # Guardar en caché
            _data_cache[self.empresa_id] = {
                'transactions': self.transactions,
                'metrics': self.metrics,
                'cash_flow_history': self.cash_flow_history
            }
            
            # Marcar como cargado
            self.data_loaded = True
            print(f"✅ Datos financieros cargados exitosamente: {len(self.transactions)} transacciones (caché actualizado)")

        except Exception as e:
            logger.error(f"Error al cargar datos financieros: {e}")
            # Fallback garantizado a datos de ejemplo
            print("📊 Error crítico, usando datos de ejemplo como fallback...")
            self.transactions = self._load_sample_data()
            self.metrics = self._calculate_metrics()
            self.cash_flow_history = self._calculate_cash_flow_history()
            self.data_loaded = True
            print(f"✅ Fallback exitoso: {len(self.transactions)} transacciones de ejemplo")
    
    async def _load_from_excel_and_migrate(self):
        """Carga datos desde Excel y los migra a Snowflake si está conectado."""
        empresa_data = await self._load_excel_data("finanzas_empresa.xlsx")
        if empresa_data:
            self.transactions.extend(empresa_data)
            print(f"✅ Cargados {len(empresa_data)} transacciones de empresa desde Excel")
            if self.use_snowflake and self.snowflake_connected:
                snowflake_service.insert_transactions([t.dict() for t in empresa_data])
        
        personal_data = await self._load_excel_data("finanzas_personales.xlsx")
        if personal_data:
            pyme_personal_data = [
                t for t in personal_data if t.transaction_type == TransactionType.EXPENSE and t.category != CategoryType.OTHER
            ]
            self.transactions.extend(pyme_personal_data)
            print(f"✅ Cargados {len(pyme_personal_data)} transacciones personales relevantes para PyME desde Excel")
            if self.use_snowflake and self.snowflake_connected:
                snowflake_service.insert_transactions([t.dict() for t in pyme_personal_data])
    
    def _load_sample_data(self) -> List[FinancialTransaction]:
        """Carga datos de ejemplo si no hay datos disponibles."""
        today = date.today()
        return [
            FinancialTransaction(id=1, date=today.replace(day=1) - timedelta(days=30), amount=5000.0, description="Ventas Enero", category=CategoryType.SALES, transaction_type=TransactionType.INCOME, user_id="demo_user"),
            FinancialTransaction(id=2, date=today.replace(day=1) - timedelta(days=25), amount=1500.0, description="Alquiler Enero", category=CategoryType.OPERATING_EXPENSES, transaction_type=TransactionType.EXPENSE, user_id="demo_user"),
            FinancialTransaction(id=3, date=today.replace(day=1) - timedelta(days=20), amount=2000.0, description="Salarios Enero", category=CategoryType.PERSONNEL, transaction_type=TransactionType.EXPENSE, user_id="demo_user"),
            FinancialTransaction(id=4, date=today.replace(day=1) - timedelta(days=15), amount=7000.0, description="Ventas Febrero", category=CategoryType.SALES, transaction_type=TransactionType.INCOME, user_id="demo_user"),
            FinancialTransaction(id=5, date=today.replace(day=1) - timedelta(days=10), amount=1600.0, description="Alquiler Febrero", category=CategoryType.OPERATING_EXPENSES, transaction_type=TransactionType.EXPENSE, user_id="demo_user"),
            FinancialTransaction(id=6, date=today.replace(day=1) - timedelta(days=5), amount=2200.0, description="Salarios Febrero", category=CategoryType.PERSONNEL, transaction_type=TransactionType.EXPENSE, user_id="demo_user"),
            FinancialTransaction(id=7, date=today, amount=8000.0, description="Ventas Marzo", category=CategoryType.SALES, transaction_type=TransactionType.INCOME, user_id="demo_user"),
            FinancialTransaction(id=8, date=today, amount=1700.0, description="Alquiler Marzo", category=CategoryType.OPERATING_EXPENSES, transaction_type=TransactionType.EXPENSE, user_id="demo_user"),
            FinancialTransaction(id=9, date=today, amount=2300.0, description="Salarios Marzo", category=CategoryType.PERSONNEL, transaction_type=TransactionType.EXPENSE, user_id="demo_user"),
            FinancialTransaction(id=10, date=today - timedelta(days=60), amount=1000.0, description="Marketing Campaña Q4", category=CategoryType.MARKETING, transaction_type=TransactionType.EXPENSE, user_id="demo_user"),
            FinancialTransaction(id=11, date=today - timedelta(days=90), amount=500.0, description="Compra de Equipo Menor", category=CategoryType.EQUIPMENT, transaction_type=TransactionType.EXPENSE, user_id="demo_user"),
            FinancialTransaction(id=12, date=today - timedelta(days=120), amount=300.0, description="Factura de Electricidad", category=CategoryType.UTILITIES, transaction_type=TransactionType.EXPENSE, user_id="demo_user"),
            FinancialTransaction(id=13, date=today - timedelta(days=150), amount=1200.0, description="Consultoría Legal", category=CategoryType.OTHER, transaction_type=TransactionType.EXPENSE, user_id="demo_user"),
            FinancialTransaction(id=14, date=today - timedelta(days=180), amount=6000.0, description="Ventas Abril", category=CategoryType.SALES, transaction_type=TransactionType.INCOME, user_id="demo_user"),
            FinancialTransaction(id=15, date=today - timedelta(days=210), amount=1800.0, description="Alquiler Abril", category=CategoryType.OPERATING_EXPENSES, transaction_type=TransactionType.EXPENSE, user_id="demo_user"),
            FinancialTransaction(id=16, date=today - timedelta(days=240), amount=2500.0, description="Salarios Abril", category=CategoryType.PERSONNEL, transaction_type=TransactionType.EXPENSE, user_id="demo_user"),
            FinancialTransaction(id=17, date=today - timedelta(days=270), amount=9000.0, description="Ventas Mayo", category=CategoryType.SALES, transaction_type=TransactionType.INCOME, user_id="demo_user"),
            FinancialTransaction(id=18, date=today - timedelta(days=300), amount=1900.0, description="Alquiler Mayo", category=CategoryType.OPERATING_EXPENSES, transaction_type=TransactionType.EXPENSE, user_id="demo_user"),
            FinancialTransaction(id=19, date=today - timedelta(days=330), amount=2600.0, description="Salarios Mayo", category=CategoryType.PERSONNEL, transaction_type=TransactionType.EXPENSE, user_id="demo_user"),
            FinancialTransaction(id=20, date=today - timedelta(days=360), amount=10000.0, description="Ventas Junio", category=CategoryType.SALES, transaction_type=TransactionType.INCOME, user_id="demo_user"),
        ]
    
    def _calculate_metrics(self) -> FinancialMetrics:
        """Calcula las métricas financieras a partir de las transacciones."""
        if not self.transactions:
            return FinancialMetrics()
        
        df = pd.DataFrame([t.dict() for t in self.transactions])
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        
        # Asegurarse de que 'amount' es numérico
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
        
        # Filtrar por el último año para métricas principales
        one_year_ago = datetime.now() - timedelta(days=365)
        df_last_year = df[df['date'] >= one_year_ago]
        
        total_income = df_last_year[df_last_year['transaction_type'] == TransactionType.INCOME]['amount'].sum()
        total_expenses = df_last_year[df_last_year['transaction_type'] == TransactionType.EXPENSE]['amount'].sum()
        net_profit = total_income - total_expenses
        profit_margin = (net_profit / total_income * 100) if total_income > 0 else 0
        
        # Cash Flow (simplificado: ingresos - gastos del último mes)
        last_month_start = (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1)
        df_last_month = df[(df['date'] >= last_month_start)]
        cash_in = df_last_month[df_last_month['transaction_type'] == TransactionType.INCOME]['amount'].sum()
        cash_out = df_last_month[df_last_month['transaction_type'] == TransactionType.EXPENSE]['amount'].sum()
        current_cash_flow = cash_in - cash_out
        
        # Tendencia de flujo de caja (comparar con el mes anterior)
        two_months_ago_start = (last_month_start.replace(day=1) - timedelta(days=1)).replace(day=1)
        df_two_months_ago = df[(df['date'] >= two_months_ago_start) & (df['date'] < last_month_start)]
        prev_cash_in = df_two_months_ago[df_two_months_ago['transaction_type'] == TransactionType.INCOME]['amount'].sum()
        prev_cash_out = df_two_months_ago[df_two_months_ago['transaction_type'] == TransactionType.EXPENSE]['amount'].sum()
        prev_cash_flow = prev_cash_in - prev_cash_out
        
        cash_flow_trend = "stable"
        if current_cash_flow > prev_cash_flow:
            cash_flow_trend = "positive"
        elif current_cash_flow < prev_cash_flow:
            cash_flow_trend = "negative"
        
        # Desglose de gastos - convertir valores a strings para asegurar compatibilidad
        expense_breakdown = df_last_year[df_last_year['transaction_type'] == TransactionType.EXPENSE].groupby('category')['amount'].sum().to_dict()
        expense_breakdown = {str(k): float(v) for k, v in expense_breakdown.items()}
        
        revenue_breakdown = df_last_year[df_last_year['transaction_type'] == TransactionType.INCOME].groupby('category')['amount'].sum().to_dict()
        revenue_breakdown = {str(k): float(v) for k, v in revenue_breakdown.items()}
        
        return FinancialMetrics(
            total_revenue=total_income,
            total_expenses=total_expenses,
            net_profit=net_profit,
            profit_margin=profit_margin,
            operating_margin=profit_margin,  # Usar profit_margin como operating_margin por ahora
            cash_flow_trend=cash_flow_trend,
            expense_breakdown=expense_breakdown,
            revenue_breakdown=revenue_breakdown
        )
    
    def _calculate_cash_flow_history(self) -> List[CashFlowData]:
        """Calcula el historial de flujo de caja mensual."""
        if not self.transactions:
            return []
        
        df = pd.DataFrame([t.dict() for t in self.transactions])
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
        df['month'] = df['date'].dt.to_period('M')
        
        monthly_data = []
        cumulative_balance = 0
        for month, group in df.groupby('month'):
            income = group[group['transaction_type'] == TransactionType.INCOME]['amount'].sum()
            expenses = group[group['transaction_type'] == TransactionType.EXPENSE]['amount'].sum()
            net_cash_flow = income - expenses
            cumulative_balance += net_cash_flow
            monthly_data.append(CashFlowData(
                period=str(month),
                income=income,
                expenses=expenses,
                net_cash_flow=net_cash_flow,
                cumulative_balance=cumulative_balance
            ))
        
        # Ordenar por mes
        monthly_data.sort(key=lambda x: datetime.strptime(x.period, '%Y-%m'))
        
        return monthly_data
    
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
