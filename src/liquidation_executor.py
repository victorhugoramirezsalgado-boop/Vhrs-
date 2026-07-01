import os
from typing import Dict, Optional
from src.asset_liquidation import AssetLiquidationRequest
import hashlib

class LiquidationExecutor:
    """
    Ejecutor de liquidación de activos
    Vende activos SOLO en las cantidades solicitadas por el admin
    """
    
    ADMIN_ID = "victorhugoramirezsalgado"
    
    def __init__(self):
        self.liquidation_system = AssetLiquidationRequest()
    
    def _verify_admin_access(self, user_id: str, session_token: str) -> bool:
        """Verifica acceso de administrador"""
        if user_id != self.ADMIN_ID:
            return False
        
        stored_token = os.getenv("ADMIN_SESSION_TOKEN")
        if not stored_token:
            return False
        
        token_hash = hashlib.sha256(session_token.encode()).hexdigest()
        stored_hash = hashlib.sha256(stored_token.encode()).hexdigest()
        
        return token_hash == stored_hash
    
    def request_asset_liquidation(
        self,
        user_id: str,
        session_token: str,
        amount_usd: float,
        asset_type: str,
        source_provider: str,
        destination_account: str,
        instruction: str
    ) -> Optional[str]:
        """
        Solicita liquidación de activos por cantidad específica.
        
        Args:
            user_id (str): ID del usuario
            session_token (str): Token de sesión
            amount_usd (float): Cantidad exacta en USD a liquidar
            asset_type (str): Tipo de activo
            source_provider (str): Proveedor (bbva/capital)
            destination_account (str): Cuenta destino
            instruction (str): Instrucción del admin
            
        Returns:
            str: ID de solicitud o None
        """
        if not self._verify_admin_access(user_id, session_token):
            return None
        
        request_id = self.liquidation_system.request_liquidation(
            admin_id=user_id,
            amount_usd=amount_usd,
            asset_type=asset_type,
            source_provider=source_provider,
            destination_account=destination_account,
            instruction=instruction
        )
        
        if request_id:
            print(f"✅ [LIQUIDACIÓN] Solicitud creada: {request_id[:8]}...")
            print(f"💰 Cantidad solicitada: ${amount_usd} USD")
            print(f"📊 Activo: {asset_type} desde {source_provider}")
        
        return request_id
    
    def approve_liquidation_request(
        self,
        user_id: str,
        session_token: str,
        request_id: str,
        approval_code: str
    ) -> bool:
        """
        Aprueba una solicitud de liquidación con 2FA.
        
        Args:
            user_id (str): ID del usuario
            session_token (str): Token de sesión
            request_id (str): ID de solicitud
            approval_code (str): Código 2FA de aprobación
            
        Returns:
            bool: True si se aprueba
        """
        if not self._verify_admin_access(user_id, session_token):
            return False
        
        success = self.liquidation_system.approve_liquidation(
            admin_id=user_id,
            request_id=request_id,
            approval_code=approval_code
        )
        
        if success:
            print(f"✅ [APROBACIÓN] Solicitud aprobada: {request_id[:8]}...")
        else:
            print(f"❌ [APROBACIÓN] Falló la aprobación")
        
        return success
    
    def execute_liquidation_request(
        self,
        user_id: str,
        session_token: str,
        request_id: str,
        execution_code: str
    ) -> bool:
        """
        Ejecuta la liquidación de activos.
        
        Args:
            user_id (str): ID del usuario
            session_token (str): Token de sesión
            request_id (str): ID de solicitud
            execution_code (str): Código 2FA de ejecución
            
        Returns:
            bool: True si se ejecuta
        """
        if not self._verify_admin_access(user_id, session_token):
            return False
        
        pending = self.liquidation_system.pending_requests.get(request_id)
        if not pending:
            return False
        
        success = self.liquidation_system.execute_liquidation(
            admin_id=user_id,
            request_id=request_id,
            execution_code=execution_code
        )
        
        if success:
            print(f"✅ [EJECUCIÓN] Liquidación ejecutada: {request_id[:8]}...")
            print(f"💵 Dinero físico (USD): ${pending['amount_usd']}")
            print(f"🏦 Enviando a cuenta de destino...")
        else:
            print(f"❌ [EJECUCIÓN] Falló la ejecución")
        
        return success
    
    def get_liquidation_status(
        self,
        user_id: str,
        session_token: str,
        request_id: str
    ) -> Optional[Dict]:
        """Obtiene estado de una solicitud de liquidación"""
        if not self._verify_admin_access(user_id, session_token):
            return None
        
        if request_id in self.liquidation_system.pending_requests:
            req = self.liquidation_system.pending_requests[request_id]
            return {
                "id": request_id,
                "amount_usd": req["amount_usd"],
                "status": req["status"],
                "asset_type": req["asset_type"],
                "source_provider": req["source_provider"],
                "requested_at": req["requested_at"]
            }
        
        return None
    
    def get_liquidation_audit(
        self,
        user_id: str,
        session_token: str
    ) -> Optional[list]:
        """Obtiene auditoría de liquidaciones (SOLO ADMIN)"""
        if not self._verify_admin_access(user_id, session_token):
            return None
        
        return self.liquidation_system.get_audit_log(user_id)