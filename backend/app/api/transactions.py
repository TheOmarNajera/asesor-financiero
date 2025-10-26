"""
Endpoints para gestión de transacciones financieras
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from app.models.financial_models import FinancialTransaction, TransactionType, CategoryType
from app.services.data_service import DataService
from app.services.snowflake_service import snowflake_service

logger = logging.getLogger(__name__)
router = APIRouter()

def get_data_service(empresa_id: Optional[str] = Header(None, alias="X-Empresa-ID")) -> DataService:
    """Dependency para obtener el servicio de datos con empresa_id del header"""
    empresa = empresa_id or "E001"
    return DataService(empresa_id=empresa)

@router.get("/")
async def get_transactions(
    limit: int = 10,
    empresa_id: Optional[str] = Header(None, alias="X-Empresa-ID")
) -> List[Dict[str, Any]]:
    """Obtener últimas transacciones"""
    try:
        empresa = empresa_id or "E001"
        
        # Si hay conexión a Snowflake, obtener de ahí
        if snowflake_service.connection:
            transactions = snowflake_service.get_transactions(empresa)
            return transactions[-limit:] if transactions else []
        
        # Si no, usar DataService
        data_service = DataService(empresa_id=empresa)
        if not data_service.transactions:
            await data_service.load_financial_data()
        
        # Obtener últimas transacciones
        transactions = data_service.transactions[-limit:] if len(data_service.transactions) > limit else data_service.transactions
        transactions.reverse()  # Más reciente primero
        
        return [t.dict() if hasattr(t, 'dict') else t for t in transactions]
    except Exception as e:
        logger.error(f"Error obteniendo transacciones: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo transacciones: {str(e)}")

@router.post("/")
async def create_transaction(
    transaction: Dict[str, Any],
    empresa_id: Optional[str] = Header(None, alias="X-Empresa-ID")
) -> Dict[str, Any]:
    """Crear nueva transacción"""
    try:
        empresa = empresa_id or "E001"
        
        # Insertar en Snowflake si está disponible
        if snowflake_service.connection:
            transaction_data = {
                'pyme_id': empresa,
                'date': transaction.get('date'),
                'amount': transaction.get('amount'),
                'description': transaction.get('description'),
                'category': transaction.get('category'),
                'transaction_type': transaction.get('transaction_type')
            }
            
            success = snowflake_service.insert_transaction(transaction_data)
            if success:
                logger.info(f"✅ Transacción insertada en Snowflake para empresa {empresa}")
            else:
                logger.warning(f"⚠️ No se pudo insertar en Snowflake, pero continuando...")
        
        return {
            "success": True,
            "message": "Transacción creada exitosamente",
            "transaction": transaction
        }
    except Exception as e:
        logger.error(f"Error creando transacción: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creando transacción: {str(e)}")

@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    empresa_id: Optional[str] = Header(None, alias="X-Empresa-ID")
) -> Dict[str, Any]:
    """Eliminar transacción"""
    try:
        empresa = empresa_id or "E001"
        
        # Eliminar de Snowflake si está disponible
        if snowflake_service.connection:
            try:
                cursor = snowflake_service.connection.cursor()
                
                cursor.execute("""
                    DELETE FROM transactions 
                    WHERE transaction_id = ? AND pyme_id = ?
                """, (transaction_id, empresa))
                cursor.close()
                snowflake_service.connection.commit()
                
                logger.info(f"✅ Transacción {transaction_id} eliminada de Snowflake")
            except Exception as e:
                logger.error(f"❌ Error eliminando de Snowflake: {e}")
        
        return {
            "success": True,
            "message": f"Transacción {transaction_id} eliminada"
        }
    except Exception as e:
        logger.error(f"Error eliminando transacción: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error eliminando transacción: {str(e)}")

