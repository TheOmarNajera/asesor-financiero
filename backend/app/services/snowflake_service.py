"""
Servicio de integración con Snowflake para análisis financiero avanzado
"""

import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
from snowflake.connector import connect
from snowflake.connector.pandas_tools import write_pandas
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)

class SnowflakeService:
    """Servicio para integración con Snowflake Data Cloud"""
    
    def __init__(self):
        self.account = os.getenv('SNOWFLAKE_ACCOUNT')
        self.user = os.getenv('SNOWFLAKE_USER')
        self.password = os.getenv('SNOWFLAKE_PASSWORD')
        self.warehouse = os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH')
        self.database = os.getenv('SNOWFLAKE_DATABASE', 'PYME_FINANCIAL')
        self.schema = os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
        self.connection = None
        
    def connect(self) -> bool:
        """Establecer conexión con Snowflake"""
        try:
            self.connection = connect(
                account=self.account,
                user=self.user,
                password=self.password,
                warehouse=self.warehouse,
                database=self.database,
                schema=self.schema
            )
            logger.info("✅ Conexión exitosa con Snowflake")
            return True
        except Exception as e:
            logger.error(f"❌ Error conectando con Snowflake: {e}")
            return False
    
    def disconnect(self):
        """Cerrar conexión con Snowflake"""
        if self.connection:
            self.connection.close()
            logger.info("🔌 Conexión con Snowflake cerrada")
    
    def create_tables(self) -> bool:
        """Crear tablas necesarias en Snowflake"""
        if not self.connection:
            return False
            
        try:
            cursor = self.connection.cursor()
            
            # Tabla de PyMEs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pymes (
                    pyme_id VARCHAR(50) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    industry VARCHAR(100),
                    size_category VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
                )
            """)
            
            # Tabla de transacciones financieras
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id VARCHAR(50) PRIMARY KEY,
                    pyme_id VARCHAR(50) REFERENCES pymes(pyme_id),
                    transaction_type VARCHAR(20) NOT NULL, -- 'income' o 'expense'
                    category VARCHAR(100) NOT NULL,
                    amount DECIMAL(15,2) NOT NULL,
                    description TEXT,
                    transaction_date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
                )
            """)
            
            # Tabla de métricas calculadas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS financial_metrics (
                    metric_id VARCHAR(50) PRIMARY KEY,
                    pyme_id VARCHAR(50) REFERENCES pymes(pyme_id),
                    metric_name VARCHAR(100) NOT NULL,
                    metric_value DECIMAL(15,2) NOT NULL,
                    calculation_date DATE NOT NULL,
                    period_type VARCHAR(20) NOT NULL, -- 'daily', 'monthly', 'yearly'
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
                )
            """)
            
            # Tabla de simulaciones
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS simulations (
                    simulation_id VARCHAR(50) PRIMARY KEY,
                    pyme_id VARCHAR(50) REFERENCES pymes(pyme_id),
                    scenario_name VARCHAR(255) NOT NULL,
                    scenario_data VARIANT NOT NULL,
                    results VARIANT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
                    created_by VARCHAR(100)
                )
            """)
            
            # Tabla de conversaciones con IA
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_conversations (
                    conversation_id VARCHAR(50) PRIMARY KEY,
                    pyme_id VARCHAR(50) REFERENCES pymes(pyme_id),
                    user_message TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    context_data VARIANT,
                    confidence_score DECIMAL(3,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
                )
            """)
            
            cursor.close()
            logger.info("✅ Tablas creadas exitosamente en Snowflake")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error creando tablas: {e}")
            return False
    
    def insert_pyme_data(self, pyme_data: Dict[str, Any]) -> bool:
        """Insertar datos de una PyME"""
        if not self.connection:
            return False
            
        try:
            cursor = self.connection.cursor()
            
            # Insertar PyME (usar MERGE en lugar de ON CONFLICT)
            cursor.execute("""
                MERGE INTO pymes AS target
                USING (SELECT %s AS pyme_id, %s AS name, %s AS industry, %s AS size_category) AS source
                ON target.pyme_id = source.pyme_id
                WHEN MATCHED THEN
                    UPDATE SET
                        name = source.name,
                        industry = source.industry,
                        size_category = source.size_category,
                        updated_at = CURRENT_TIMESTAMP()
                WHEN NOT MATCHED THEN
                    INSERT (pyme_id, name, industry, size_category)
                    VALUES (source.pyme_id, source.name, source.industry, source.size_category)
            """, (
                pyme_data['pyme_id'],
                pyme_data['name'],
                pyme_data.get('industry', 'Unknown'),
                pyme_data.get('size_category', 'SME')
            ))
            
            # Insertar transacciones (usar MERGE en lugar de ON CONFLICT)
            if 'transactions' in pyme_data:
                for transaction in pyme_data['transactions']:
                    cursor.execute("""
                        MERGE INTO transactions AS target
                        USING (SELECT %s AS transaction_id, %s AS pyme_id, %s AS transaction_type, 
                                      %s AS category, %s AS amount, %s AS description, %s AS transaction_date) AS source
                        ON target.transaction_id = source.transaction_id
                        WHEN MATCHED THEN
                            UPDATE SET
                                transaction_type = source.transaction_type,
                                category = source.category,
                                amount = source.amount,
                                description = source.description,
                                transaction_date = source.transaction_date,
                                updated_at = CURRENT_TIMESTAMP()
                        WHEN NOT MATCHED THEN
                            INSERT (transaction_id, pyme_id, transaction_type, category, amount, description, transaction_date)
                            VALUES (source.transaction_id, source.pyme_id, source.transaction_type, 
                                   source.category, source.amount, source.description, source.transaction_date)
                    """, (
                        transaction['id'],
                        pyme_data['pyme_id'],
                        transaction['type'],
                        transaction['category'],
                        transaction['amount'],
                        transaction.get('description', ''),
                        transaction['date']
                    ))
            
            cursor.close()
            logger.info(f"✅ Datos de PyME {pyme_data['pyme_id']} insertados")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error insertando datos de PyME: {e}")
            return False
    
    def get_financial_analysis(self, pyme_id: str, period_days: int = 365) -> Dict[str, Any]:
        """Obtener análisis financiero avanzado desde Snowflake"""
        if not self.connection:
            return {}
            
        try:
            cursor = self.connection.cursor()
            
            # Análisis de ingresos por mes
            cursor.execute("""
                SELECT 
                    DATE_TRUNC('MONTH', transaction_date) as month,
                    SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as total_income,
                    SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as total_expenses,
                    SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE -amount END) as net_income
                FROM transactions 
                WHERE pyme_id = %s 
                AND transaction_date >= DATEADD(day, -%s, CURRENT_DATE())
                GROUP BY DATE_TRUNC('MONTH', transaction_date)
                ORDER BY month DESC
            """, (pyme_id, period_days))
            
            monthly_data = cursor.fetchall()
            
            # Análisis por categorías
            cursor.execute("""
                SELECT 
                    category,
                    transaction_type,
                    SUM(amount) as total_amount,
                    COUNT(*) as transaction_count,
                    AVG(amount) as avg_amount
                FROM transactions 
                WHERE pyme_id = %s 
                AND transaction_date >= DATEADD(day, -%s, CURRENT_DATE())
                GROUP BY category, transaction_type
                ORDER BY total_amount DESC
            """, (pyme_id, period_days))
            
            category_data = cursor.fetchall()
            
            # Métricas de tendencias
            cursor.execute("""
                SELECT 
                    AVG(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as avg_income,
                    AVG(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as avg_expense,
                    STDDEV(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as income_volatility,
                    STDDEV(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as expense_volatility
                FROM transactions 
                WHERE pyme_id = %s 
                AND transaction_date >= DATEADD(day, -%s, CURRENT_DATE())
            """, (pyme_id, period_days))
            
            trend_data = cursor.fetchone()
            
            cursor.close()
            
            return {
                'monthly_analysis': [
                    {
                        'month': row[0].strftime('%Y-%m'),
                        'total_income': float(row[1]),
                        'total_expenses': float(row[2]),
                        'net_income': float(row[3])
                    } for row in monthly_data
                ],
                'category_analysis': [
                    {
                        'category': row[0],
                        'type': row[1],
                        'total_amount': float(row[2]),
                        'transaction_count': row[3],
                        'avg_amount': float(row[4])
                    } for row in category_data
                ],
                'trend_metrics': {
                    'avg_income': float(trend_data[0]) if trend_data[0] else 0,
                    'avg_expense': float(trend_data[1]) if trend_data[1] else 0,
                    'income_volatility': float(trend_data[2]) if trend_data[2] else 0,
                    'expense_volatility': float(trend_data[3]) if trend_data[3] else 0
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error en análisis financiero: {e}")
            return {}
    
    def run_simulation(self, pyme_id: str, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecutar simulación financiera usando Snowflake"""
        if not self.connection:
            return {}
            
        try:
            cursor = self.connection.cursor()
            
            # Obtener datos históricos
            cursor.execute("""
                SELECT 
                    transaction_type,
                    category,
                    amount,
                    transaction_date
                FROM transactions 
                WHERE pyme_id = %s 
                AND transaction_date >= DATEADD(day, -365, CURRENT_DATE())
                ORDER BY transaction_date
            """, (pyme_id,))
            
            historical_data = cursor.fetchall()
            
            # Procesar simulación (lógica simplificada)
            simulation_results = self._process_simulation(historical_data, scenario)
            
            # Guardar resultados
            simulation_id = f"sim_{pyme_id}_{int(datetime.now().timestamp())}"
            cursor.execute("""
                INSERT INTO simulations (simulation_id, pyme_id, scenario_name, scenario_data, results)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                simulation_id,
                pyme_id,
                scenario.get('name', 'Simulación'),
                json.dumps(scenario),
                json.dumps(simulation_results)
            ))
            
            cursor.close()
            
            return {
                'simulation_id': simulation_id,
                'scenario': scenario,
                'results': simulation_results,
                'created_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error en simulación: {e}")
            return {}
    
    def _process_simulation(self, historical_data: List, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Procesar lógica de simulación"""
        # Implementar lógica de simulación basada en datos históricos
        # y parámetros del escenario
        
        total_income = sum(row[2] for row in historical_data if row[0] == 'income')
        total_expenses = sum(row[2] for row in historical_data if row[0] == 'expense')
        
        # Aplicar cambios del escenario
        income_multiplier = scenario.get('income_change', 1.0)
        expense_multiplier = scenario.get('expense_change', 1.0)
        
        projected_income = total_income * income_multiplier
        projected_expenses = total_expenses * expense_multiplier
        projected_net = projected_income - projected_expenses
        
        return {
            'current_income': total_income,
            'current_expenses': total_expenses,
            'current_net': total_income - total_expenses,
            'projected_income': projected_income,
            'projected_expenses': projected_expenses,
            'projected_net': projected_net,
            'income_change_percent': (income_multiplier - 1) * 100,
            'expense_change_percent': (expense_multiplier - 1) * 100,
            'net_change_percent': ((projected_net / (total_income - total_expenses)) - 1) * 100 if (total_income - total_expenses) != 0 else 0
        }
    
    def get_chat_context(self, pyme_id: str) -> Dict[str, Any]:
        """Obtener contexto financiero para el chat con IA"""
        analysis = self.get_financial_analysis(pyme_id, 90)  # Últimos 90 días
        
        if not analysis:
            return {}
        
        # Calcular métricas clave
        monthly_data = analysis.get('monthly_analysis', [])
        if monthly_data:
            latest_month = monthly_data[0]
            avg_income = sum(m['total_income'] for m in monthly_data) / len(monthly_data)
            avg_expenses = sum(m['total_expenses'] for m in monthly_data) / len(monthly_data)
        else:
            latest_month = {}
            avg_income = avg_expenses = 0
        
        return {
            'pyme_id': pyme_id,
            'latest_month': latest_month,
            'avg_monthly_income': avg_income,
            'avg_monthly_expenses': avg_expenses,
            'profit_margin': ((avg_income - avg_expenses) / avg_income * 100) if avg_income > 0 else 0,
            'category_breakdown': analysis.get('category_analysis', []),
            'trend_metrics': analysis.get('trend_metrics', {}),
            'data_period': '90 días'
        }
    
    def log_chat_interaction(self, pyme_id: str, user_message: str, ai_response: str, context: Dict[str, Any], confidence: float = 0.9) -> bool:
        """Registrar interacción del chat en Snowflake"""
        if not self.connection:
            return False
            
        try:
            cursor = self.connection.cursor()
            
            conversation_id = f"chat_{pyme_id}_{int(datetime.now().timestamp())}"
            cursor.execute("""
                INSERT INTO chat_conversations 
                (conversation_id, pyme_id, user_message, ai_response, context_data, confidence_score)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                conversation_id,
                pyme_id,
                user_message,
                ai_response,
                json.dumps(context),
                confidence
            ))
            
            cursor.close()
            return True
            
        except Exception as e:
            logger.error(f"❌ Error registrando chat: {e}")
            return False
    
    def insert_transaction(self, transaction_data: Dict[str, Any]) -> bool:
        """Insertar una nueva transacción en Snowflake"""
        if not self.connection:
            return False
        
        try:
            import uuid
            cursor = self.connection.cursor()
            
            # Generar un transaction_id único
            transaction_id = f"txn_{uuid.uuid4().hex[:12]}"
            
            cursor.execute("""
                INSERT INTO transactions (
                    transaction_id,
                    pyme_id,
                    transaction_date,
                    amount,
                    description,
                    category,
                    transaction_type
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                transaction_id,
                transaction_data.get('pyme_id', 'E001'),
                transaction_data.get('date'),
                transaction_data.get('amount'),
                transaction_data.get('description'),
                transaction_data.get('category'),
                transaction_data.get('transaction_type')
            ))
            
            cursor.close()
            logger.info(f"✅ Transacción {transaction_id} insertada en Snowflake")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error insertando transacción: {e}")
            return False
    
    def get_transactions(self, pyme_id: str = "empresa_001") -> List[Dict[str, Any]]:
        """Obtener todas las transacciones de una PyME"""
        if not self.connection:
            return []
            
        try:
            cursor = self.connection.cursor()
            
            # Primero intentar desde ROW_DATA_EMPRESA (datos reales del Excel)
            cursor.execute("""
                SELECT 
                    ROW_NUMBER() OVER (ORDER BY fecha DESC) as transaction_id,
                    TO_DATE(fecha, 'DD/MM/YYYY') as transaction_date,
                    monto as amount,
                    concepto as description,
                    categoria as category,
                    LOWER(tipo) as transaction_type
                FROM ROW_DATA_EMPRESA
                WHERE empresa_id = %s
                ORDER BY TO_DATE(fecha, 'DD/MM/YYYY') DESC
                LIMIT 10000
            """, (pyme_id,))
            
            row_data = cursor.fetchall()
            
            # Si no hay datos en ROW_DATA_EMPRESA, intentar en transactions
            if not row_data:
                cursor.execute("""
                    SELECT 
                        transaction_id,
                        transaction_date,
                        amount,
                        description,
                        category,
                        transaction_type
                    FROM transactions
                    WHERE pyme_id = %s
                    ORDER BY transaction_date DESC
                """, (pyme_id,))
                row_data = cursor.fetchall()
            
            cursor.close()
            
            # Convertir a formato esperado por FinancialTransaction
            result = []
            for row in row_data:
                # Mapear categoría a formato esperado
                categoria = row[4].lower() if row[4] else ''
                categoria_mapped = 'operating_expenses'  # default
                
                if categoria in ['venta', 'ventas', 'sales']:
                    categoria_mapped = 'sales'
                elif categoria in ['personal', 'nomina', 'nómina', 'personnel']:
                    categoria_mapped = 'personnel'
                elif categoria in ['marketing', 'publicidad', 'promocion']:
                    categoria_mapped = 'marketing'
                elif categoria in ['equipo', 'inventario', 'equipment', 'maquinaria']:
                    categoria_mapped = 'equipment'
                elif categoria in ['servicios', 'utilities', 'publicos', 'luz', 'agua']:
                    categoria_mapped = 'utilities'
                elif categoria in ['costos', 'gastos operativos', 'operating', 'infraestructur']:
                    categoria_mapped = 'operating_expenses'
                else:
                    categoria_mapped = 'operating_expenses'
                
                # Mapear tipo de transacción
                tipo = row[5].lower() if row[5] else ''
                tipo_mapped = 'expense'  # default
                
                if tipo in ['ingreso', 'income', 'i']:
                    tipo_mapped = 'income'
                elif tipo in ['gasto', 'expense', 'e']:
                    tipo_mapped = 'expense'
                elif tipo in ['inversion', 'investment']:
                    tipo_mapped = 'investment'
                
                result.append({
                    'id': int(row[0].split('_')[-1]) if '_' in str(row[0]) else 0,
                    'date': row[1].isoformat() if isinstance(row[1], datetime) else str(row[1]),
                    'amount': float(row[2]),
                    'description': row[3] or '',
                    'category': categoria_mapped,
                    'transaction_type': tipo_mapped
                })
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo transacciones: {e}")
            return []

# Instancia global del servicio
snowflake_service = SnowflakeService()
