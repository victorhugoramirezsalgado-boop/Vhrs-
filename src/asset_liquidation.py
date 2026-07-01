import hashlib
import os
from datetime import datetime
from typing import Dict, Optional, List
import json
from cryptography.fernet import Fernet
import base64

class AssetLiquidationRequest:
    """
    Sistema de solicitudes de liquidación de activos - SOLO ADMIN
    Solo ejecuta lo que el administrador único solicita explícitamente
    """
    
    ADMIN_ID = "victorhugoramirezsalgado"
    INTERTOPIA_ADMIN = "Intertopía / 1ntertopía"
    
    def __init__(self):
        self.pending_requests = {}
        self.executed_liquidations = []
        self.audit_log = []
        self.cipher = Fernet(self._get_encryption_key())
    
    def _get_encryption_key(self) -> bytes:
        """Obtiene clave de encriptación desde variables de entorno"""
        key = os.getenv("ENCRYPTION_KEY")
        if not key:
            raise ValueError("ENCRYPTION_KEY no configurada")
        return key.encode()
    
    def _verify_admin(self, user_id: str) -> bool:
        """Verifica que sea el administrador único"""
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
    
    def request_liquidation(
        self,
        admin_id: str,
        amount_usd: float,
        asset_type: str,
        source_provider: str,
        destination_account: str,
        instruction: str
    ) -> Optional[str]:
        """
        Crea una solicitud de liquidación de activos.
        SOLO el administrador puede solicitar.
        
        Args:
            admin_id (str): ID del administrador
            amount_usd (str): Cantidad exacta en USD solicitada
            asset_type (str): Tipo de activo ('stock', 'crypto', 'fund', etc.)
            source_provider (str): Proveedor ('bbva' o 'capital')
            destination_account (str): Cuenta destino para dinero físico
            instruction (str): Instrucción específica del admin
            
        Returns:
            str: ID de solicitud o None si falla
        """
        if not self._verify_admin(admin_id):
            self._log_audit("UNAUTHORIZED_LIQUIDATION_REQUEST", "N/A", 0, "Usuario no autorizado")
            return None
        
        if amount_usd <= 0:
            self._log_audit("INVALID_AMOUNT", "N/A", amount_usd, "Cantidad debe ser positiva")
            return None
        
        if source_provider not in ["bbva", "capital"]:
            self._log_audit("INVALID_PROVIDER", "N/A", amount_usd, "Proveedor inválido")
            return None
        
        request_id = hashlib.sha256(
            f"{amount_usd}{source_provider}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:24]
        
        encrypted_destination = self._encrypt_data(destination_account)
        encrypted_instruction = self._encrypt_data(instruction)
        
        self.pending_requests[request_id] = {
            "amount_usd": amount_usd,
            "asset_type": asset_type,
            "source_provider": source_provider,
            "destination_account": encrypted_destination,
            "instruction": encrypted_instruction,
            "requested_by": admin_id,
            "requested_at": datetime.now().isoformat(),
            "status": "pending",
            "confirmation_required": True,
            "intertopia_admin": self.INTERTOPIA_ADMIN
        }
        
        self._log_audit(
            "LIQUIDATION_REQUESTED",
            request_id,
            amount_usd,
            f"Solicitud de liquidación: {asset_type} desde {source_provider}"
        )
        
        return request_id
    
    def approve_liquidation(
        self,
        admin_id: str,
        request_id: str,
        approval_code: str
    ) -> bool:
        """
        Aprueba y autoriza una solicitud de liquidación.
        Requiere código de confirmación 2FA.
        
        Args:
            admin_id (str): ID del administrador
            request_id (str): ID de la solicitud
            approval_code (str): Código de aprobación 2FA
            
        Returns:
            bool: True si se aprueba, False si no
        """
        if not self._verify_admin(admin_id):
            self._log_audit("UNAUTHORIZED_APPROVAL", request_id, 0, "No autorizado")
            return False
        
        if request_id not in self.pending_requests:
            self._log_audit("REQUEST_NOT_FOUND", request_id, 0, "Solicitud no existe")
            return False
        
        liquidation = self.pending_requests[request_id]
        
        if not self._validate_approval_code(approval_code):
            self._log_audit("APPROVAL_FAILED", request_id, liquidation["amount_usd"], "Código inválido")
            return False
        
        liquidation["status"] = "approved"
        liquidation["approved_at"] = datetime.now().isoformat()
        liquidation["approved_by"] = admin_id
        
        self._log_audit(
            "LIQUIDATION_APPROVED",
            request_id,
            liquidation["amount_usd"],
            f"Aprobado por {admin_id}"
        )
        
        return True
    
    def execute_liquidation(
        self,
        admin_id: str,
        request_id: str,
        execution_code: str
    ) -> bool:
        """
        Ejecuta la liquidación de activos después de aprobación.
        
        Args:
            admin_id (str): ID del administrador
            request_id (str): ID de la solicitud
            execution_code (str): Código de ejecución
            
        Returns:
            bool: True si se ejecuta, False si falla
        """
        if not self._verify_admin(admin_id):
            return False
        
        if request_id not in self.pending_requests:
            return False
        
        liquidation = self.pending_requests[request_id]
        
        if liquidation["status"] != "approved":
            self._log_audit("EXECUTION_FAILED", request_id, liquidation["amount_usd"], "No está aprobado")
            return False
        
        if not self._validate_execution_code(execution_code):
            self._log_audit("EXECUTION_FAILED", request_id, liquidation["amount_usd"], "Código inválido")
            return False
        
        liquidation["status"] = "executed"
        liquidation["executed_at"] = datetime.now().isoformat()
        liquidation["executed_by"] = admin_id
        self.executed_liquidations.append(liquidation.copy())
        
        self._log_audit(
            "LIQUIDATION_EXECUTED",
            request_id,
            liquidation["amount_usd"],
            f"Liquidación ejecutada: USD {liquidation['amount_usd']}"
        )
        
        return True
    
    def _validate_approval_code(self, code: str) -> bool:
        """Valida código de aprobación 2FA"""
        expected_code = os.getenv("ADMIN_APPROVAL_CODE")
        if not expected_code:
            return False
        
        code_hash = hashlib.sha256(code.encode()).hexdigest()
        expected_hash = hashlib.sha256(expected_code.encode()).hexdigest()
        return code_hash == expected_hash
    
    def _validate_execution_code(self, code: str) -> bool:
        """Valida código de ejecución 2FA"""
        expected_code = os.getenv("ADMIN_EXECUTION_CODE")
        if not expected_code:
            return False
        
        code_hash = hashlib.sha256(code.encode()).hexdigest()
        expected_hash = hashlib.sha256(expected_code.encode()).hexdigest()
        return code_hash == expected_hash
    
    def _log_audit(self, action: str, request_id: str, amount: float, details: str = "") -> None:
        """Registra en log de auditoría encriptado"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "request_id": request_id,
            "amount_usd": amount,
            "details": details,
            "admin": self.ADMIN_ID,
            "intertopia": self.INTERTOPIA_ADMIN
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
            except Exception:
                decrypted_logs.append({"error": "No se pudo desencriptar"})
        
        return decrypted_logs
    
    def get_pending_requests(self, admin_id: str) -> Optional[Dict]:
        """Obtiene solicitudes pendientes (SOLO ADMIN)"""
        if not self._verify_admin(admin_id):
            return None
        
        result = {}
        for request_id, req in self.pending_requests.items():
            result[request_id] = {
                "amount_usd": req["amount_usd"],
                "asset_type": req["asset_type"],
                "source_provider": req["source_provider"],
                "status": req["status"],
                "requested_at": req["requested_at"],
                "instruction": self._decrypt_data(req["instruction"]) if req.get("instruction") else "N/A"
            }
        
        return result