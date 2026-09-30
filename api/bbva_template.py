"""
🏦 BBVA API Template
Plantilla para integración con APIs de BBVA
Sin operaciones reales - Solo estructura para llenar posterior
"""

import os
from dotenv import load_dotenv

load_dotenv('config/.env')

class BBVAAPIClient:
    """
    Cliente para interactuar con APIs de BBVA
    STATUS: Plantilla - Esperando configuración
    """
    
    def __init__(self):
        self.client_id = os.getenv('BBVA_CLIENT_ID')
        self.client_secret = os.getenv('BBVA_CLIENT_SECRET')
        self.api_url = os.getenv('BBVA_API_URL', 'https://apis.bbva.com/')
        self.account_number = os.getenv('BBVA_ACCOUNT_NUMBER')
        self.is_configured = self._validate_config()
    
    def _validate_config(self):
        """Valida si las credenciales están configuradas"""
        return all([self.client_id, self.client_secret, self.account_number])
    
    def authenticate(self):
        """
        Autentica con BBVA API
        TODO: Implementar autenticación OAuth2
        """
        if not self.is_configured:
            return {
                'status': 'error',
                'message': '❌ Credenciales BBVA no configuradas',
                'action': 'Completa config/.env con datos de BBVA'
            }
        
        print("🔐 Autenticación con BBVA...")
        return {
            'status': 'pending',
            'message': '⏳ Esperando implementación de OAuth2'
        }
    
    def get_accounts(self):
        """
        Obtiene lista de cuentas
        TODO: Implementar consulta de cuentas
        """
        return {
            'status': 'pending',
            'accounts': [],
            'message': '⏳ Esperando implementación'
        }
    
    def get_balance(self, account_id=None):
        """
        Obtiene saldo de cuenta
        TODO: Implementar consulta de saldo
        """
        account = account_id or self.account_number
        return {
            'status': 'pending',
            'account': account,
            'balance': None,
            'message': '⏳ Esperando implementación'
        }
    
    def get_transactions(self, days=30):
        """
        Obtiene transacciones recientes
        TODO: Implementar consulta de transacciones
        """
        return {
            'status': 'pending',
            'transactions': [],
            'days': days,
            'message': '⏳ Esperando implementación'
        }
    
    def transfer_funds(self, to_account, amount, description):
        """
        Realiza transferencia (SIMULADA - NUNCA ejecutar sin confirmación)
        TODO: Implementar transferencias con doble autenticación
        """
        return {
            'status': 'blocked',
            'message': '🚫 Transferencias deshabilitadas en plantilla',
            'warning': 'Requiere implementación de seguridad adicional'
        }

# Template de uso
if __name__ == "__main__":
    client = BBVAAPIClient()
    print("\n🏦 Cliente BBVA API")
    print(f"Configurado: {client.is_configured}")
    print(f"URL: {client.api_url}")
    print("\n✓ Estructura lista para llenar")