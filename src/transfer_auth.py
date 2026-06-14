import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, Optional
import json
from cryptography.fernet import Fernet
import base64

class TransferAuthorization:
    """Sistema de autorización de transferencias - SOLO PARA ADMIN"""
    
    ADMIN_ID = "victorhugoramirezsalgado"
    TRANSFER_TIMEOUT = 300  # 5 minutos
    
    def __init__(self):
        self.pending_transfers = {}
        self.authorized_transfers = []
        self.audit_log = []
        self.cipher = Fernet(self._get_encryption_key())
    
    def _get_encryption_key(self) -> bytes:
        """Obtiene clave de encriptación desde variables de entorno"""
        key = os.getenv("ENCRYPTION_KEY")
        if not key:
            raise ValueError("ENCRYPTION_KEY no configurada")
        return key.encode()
    
    def _verify_admin(self, user_id: str) -> bool:
        """Verifica que el usuario sea el administrador único"""
        return user_id == self.ADMIN_ID
    
    def _encrypt_data(self, data: str) -> str:
        """Encripta datos sensibles"""
        encrypted = self.cipher.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()
    
    def _decrypt_data(self, encrypted_data: str) -> str:
        """Desencripta datos sensibles"""
        encrypted = base64.b64decode(encrypted_data.encode())
        decrypted = self.cipher.decrypt(encrypted)
        return decrypted.decode()
    
    def request_transfer(
        self, 
        admin_id: str,
        amount: float, 
        destination: str, 
        reason: str
    ) -> Optional[str]:
        """
        Crea una solicitud de transferencia (SOLO ADMIN).
        
        Args:
            admin_id (str): ID del usuario solicitante
            amount (float): Monto a transferir
            destination (str): Cuenta destino (solo cuentas del admin)
            reason (str): Razón de la transferencia
            
        Returns:
            str: ID de la solicitud o None si falla
        """
        if not self._verify_admin(admin_id):
            self._log_audit("UNAUTHORIZED_TRANSFER_REQUEST", "N/A", 0, "Usuario no autorizado")
            return None
        
        transfer_id = hashlib.sha256(
            f"{amount}{destination}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:24]
        
        encrypted_destination = self._encrypt_data(destination)
        encrypted_reason = self._encrypt_data(reason)
        
        self.pending_transfers[transfer_id] = {
            "amount": amount,
            "destination": encrypted_destination,
            "reason": encrypted_reason,
            "requested_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(seconds=self.TRANSFER_TIMEOUT)).isoformat(),
            "status": "pending",
            "confirmation_token": None,
            "admin_id": admin_id
        }
        
        self._log_audit("TRANSFER_REQUESTED", transfer_id, amount, "Solicitud creada")
        return transfer_id
    
    def authorize_transfer(
        self, 
        admin_id: str,
        transfer_id: str, 
        admin_confirmation_code: str
    ) -> bool:
        """
        Autoriza una transferencia con confirmación del administrador.
        
        Args:
            admin_id (str): ID del administrador
            transfer_id (str): ID de la transferencia
            admin_confirmation_code (str): Código de confirmación (2FA)
            
        Returns:
            bool: True si se autoriza, False si no
        """
        if not self._verify_admin(admin_id):
            self._log_audit("UNAUTHORIZED_AUTH", transfer_id, 0, "No autorizado")
            return False
        
        if transfer_id not in self.pending_transfers:
            self._log_audit("TRANSFER_NOT_FOUND", transfer_id, 0, "Solicitud no existe")
            return False
        
        transfer = self.pending_transfers[transfer_id]
        
        if datetime.fromisoformat(transfer["expires_at"]) < datetime.now():
            self._log_audit("TRANSFER_EXPIRED", transfer_id, transfer["amount"], "Expirada")
            return False
        
        if not self._validate_confirmation_code(admin_confirmation_code):
            self._log_audit("TRANSFER_AUTH_FAILED", transfer_id, transfer["amount"], "Código inválido")
            return False
        
        transfer["status"] = "authorized"
        transfer["authorized_at"] = datetime.now().isoformat()
        transfer["authorized_by"] = admin_id
        self.authorized_transfers.append(transfer.copy())
        
        self._log_audit("TRANSFER_AUTHORIZED", transfer_id, transfer["amount"], "Autorizada")
        
        return True
    
    def _validate_confirmation_code(self, code: str) -> bool:
        """Valida código 2FA del administrador"""
        expected_code = os.getenv("ADMIN_CONFIRMATION_CODE")
        if not expected_code:
            return False
        
        code_hash = hashlib.sha256(code.encode()).hexdigest()
        expected_hash = hashlib.sha256(expected_code.encode()).hexdigest()
        return code_hash == expected_hash
    
    def _log_audit(self, action: str, transfer_id: str, amount: float, details: str = "") -> None:
        """Registra acciones en log de auditoría encriptado"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "transfer_id": transfer_id,
            "amount": amount,
            "details": details,
            "admin": self.ADMIN_ID
        }
        
        encrypted_log = self._encrypt_data(json.dumps(log_entry))
        self.audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "data": encrypted_log
        })
    
    def get_audit_log(self, admin_id: str) -> Optional[list]:
        """Obtiene log de auditoría (SOLO ADMIN)"""
        if not self._verify_admin(admin_id):
            return None
        
        decrypted_logs = []
        for log in self.audit_log:
            try:
                decrypted_data = self._decrypt_data(log["data"])
                decrypted_logs.append(json.loads(decrypted_data))
            except Exception as e:
                decrypted_logs.append({"error": "No se pudo desencriptar"})
        
        return decrypted_logs
    
    def get_pending_transfers(self, admin_id: str) -> Optional[Dict]:
        """Obtiene transferencias pendientes (SOLO ADMIN)"""
        if not self._verify_admin(admin_id):
            return None
        
        result = {}
        for transfer_id, transfer in self.pending_transfers.items():
            result[transfer_id] = {
                "amount": transfer["amount"],
                "status": transfer["status"],
                "requested_at": transfer["requested_at"],
                "expires_at": transfer["expires_at"],
                "destination": self._decrypt_data(transfer["destination"]) if transfer.get("destination") else "N/A"
            }
        
        return result