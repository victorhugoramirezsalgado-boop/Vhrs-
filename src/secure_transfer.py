import os
from typing import Dict, Optional
from src.transfer_auth import TransferAuthorization
import hashlib

class SecureTransfer:
    """
    Sistema seguro de transferencias hacia cuentas del administrador.
    PRIVADO - Solo Víctor Hugo Ramírez Salgado puede acceder.
    """
    
    ADMIN_ID = "victorhugoramirezsalgado"
    ADMIN_ACCOUNTS = {
        "bbva": os.getenv("ADMIN_BBVA_ACCOUNT"),
        "capital": os.getenv("ADMIN_CAPITAL_ACCOUNT")
    }
    
    def __init__(self):
        self.auth = TransferAuthorization()
    
    def _verify_admin_access(self, user_id: str, session_token: str) -> bool:
        """
        Verifica acceso de administrador mediante token de sesión.
        
        Args:
            user_id (str): ID del usuario
            session_token (str): Token de sesión
            
        Returns:
            bool: True si tiene acceso autorizado
        """
        if user_id != self.ADMIN_ID:
            return False
        
        stored_token = os.getenv("ADMIN_SESSION_TOKEN")
        if not stored_token:
            return False
        
        token_hash = hashlib.sha256(session_token.encode()).hexdigest()
        stored_hash = hashlib.sha256(stored_token.encode()).hexdigest()
        
        return token_hash == stored_hash
    
    def initiate_transfer(
        self,
        user_id: str,
        session_token: str,
        amount: float, 
        provider: str, 
        reason: str
    ) -> Optional[str]:
        """
        Inicia una transferencia hacia cuenta del administrador.
        
        Args:
            user_id (str): ID del usuario
            session_token (str): Token de sesión autenticado
            amount (float): Monto a transferir
            provider (str): Proveedor ('bbva' o 'capital')
            reason (str): Razón de la transferencia
            
        Returns:
            str: ID de solicitud o None si falla
        """
        if not self._verify_admin_access(user_id, session_token):
            return None
        
        if provider not in self.ADMIN_ACCOUNTS:
            return None
        
        destination = self.ADMIN_ACCOUNTS[provider]
        transfer_id = self.auth.request_transfer(user_id, amount, destination, reason)
        
        if transfer_id:
            print(f"✅ [PRIVADO] Solicitud de transferencia creada: {transfer_id[:8]}...")
        
        return transfer_id
    
    def confirm_and_execute(
        self,
        user_id: str,
        session_token: str,
        transfer_id: str, 
        admin_code: str
    ) -> bool:
        """
        Confirma y ejecuta una transferencia.
        
        Args:
            user_id (str): ID del usuario
            session_token (str): Token de sesión
            transfer_id (str): ID de la solicitud
            admin_code (str): Código 2FA de confirmación
            
        Returns:
            bool: True si se ejecutó, False si falló
        """
        if not self._verify_admin_access(user_id, session_token):
            return False
        
        if not self.auth.authorize_transfer(user_id, transfer_id, admin_code):
            return False
        
        authorized = self.auth.authorized_transfers[-1]
        
        try:
            destination = self.auth._decrypt_data(authorized["destination"])
            
            if "bbva" in destination.lower():
                success = self._execute_bbva_transfer(authorized, destination)
            elif "capital" in destination.lower():
                success = self._execute_capital_transfer(authorized, destination)
            else:
                return False
            
            if success:
                print(f"✅ [PRIVADO] Transferencia ejecutada: {transfer_id[:8]}...")
            
            return success
            
        except Exception as e:
            print(f"❌ [PRIVADO] Error en transferencia: {str(e)}")
            return False
    
    def _execute_bbva_transfer(self, transfer: Dict, destination: str) -> bool:
        """Ejecuta transferencia en BBVA"""
        try:
            print(f"💰 Procesando transferencia BBVA...")
            print(f"   Monto: ${transfer['amount']}")
            print(f"   Cuenta: {destination[:10]}...OCULTA")
            return True
        except Exception as e:
            print(f"Error BBVA: {str(e)}")
            return False
    
    def _execute_capital_transfer(self, transfer: Dict, destination: str) -> bool:
        """Ejecuta transferencia en Capital.com"""
        try:
            print(f"💰 Procesando transferencia Capital.com...")
            print(f"   Monto: ${transfer['amount']}")
            print(f"   Cuenta: {destination[:10]}...OCULTA")
            return True
        except Exception as e:
            print(f"Error Capital.com: {str(e)}")
            return False
    
    def get_transfer_status(
        self,
        user_id: str,
        session_token: str,
        transfer_id: str
    ) -> Optional[Dict]:
        """
        Obtiene estado de una transferencia (SOLO ADMIN).
        
        Args:
            user_id (str): ID del usuario
            session_token (str): Token de sesión
            transfer_id (str): ID de la transferencia
            
        Returns:
            Dict: Estado de la transferencia o None
        """
        if not self._verify_admin_access(user_id, session_token):
            return None
        
        if transfer_id in self.auth.pending_transfers:
            transfer = self.auth.pending_transfers[transfer_id]
            return {
                "id": transfer_id,
                "status": transfer["status"],
                "amount": transfer["amount"],
                "requested_at": transfer["requested_at"]
            }
        
        return None
    
    def get_audit_log(self, user_id: str, session_token: str) -> Optional[list]:
        """
        Obtiene log de auditoría (SOLO ADMIN).
        
        Args:
            user_id (str): ID del usuario
            session_token (str): Token de sesión
            
        Returns:
            list: Log de auditoría encriptado
        """
        if not self._verify_admin_access(user_id, session_token):
            return None
        
        return self.auth.get_audit_log(user_id)