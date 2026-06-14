"""
API Privada de Transferencias Seguras
SOLO para Víctor Hugo Ramírez Salgado
Todos los datos están encriptados y no son públicos.
"""

from flask import Flask, request, jsonify
from functools import wraps
import os
import hashlib
from src.secure_transfer import SecureTransfer

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "SECURE_KEY_CHANGE_IN_PRODUCTION")

transfer_handler = SecureTransfer()

# Middleware de autenticación privada
def require_admin_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "No autorizado"}), 401
        
        token = auth_header.split(' ')[1]
        user_id = request.headers.get('X-User-ID')
        
        if user_id != "victorhugoramirezsalgado":
            return jsonify({"error": "No autorizado"}), 401
        
        return f(user_id, token, *args, **kwargs)
    
    return decorated

@app.route('/api/private/transfer/initiate', methods=['POST'])
@require_admin_auth
def initiate_transfer(user_id, session_token):
    """
    Inicia una solicitud de transferencia privada.
    SOLO ACCESIBLE para victorhugoramirezsalgado
    """
    try:
        data = request.json
        
        transfer_id = transfer_handler.initiate_transfer(
            user_id=user_id,
            session_token=session_token,
            amount=data.get('amount'),
            provider=data.get('provider'),
            reason=data.get('reason')
        )
        
        if not transfer_id:
            return jsonify({"error": "No se pudo crear la solicitud"}), 400
        
        return jsonify({
            "status": "success",
            "transfer_id": transfer_id,
            "message": "Solicitud privada creada. Pendiente de confirmación."
        }), 202
        
    except Exception as e:
        return jsonify({"status": "error", "message": "Error interno"}), 500

@app.route('/api/private/transfer/confirm', methods=['POST'])
@require_admin_auth
def confirm_transfer(user_id, session_token):
    """
    Confirma y ejecuta una transferencia privada.
    Requiere código 2FA.
    """
    try:
        data = request.json
        
        success = transfer_handler.confirm_and_execute(
            user_id=user_id,
            session_token=session_token,
            transfer_id=data.get('transfer_id'),
            admin_code=data.get('admin_code')
        )
        
        return jsonify({
            "status": "success" if success else "failed",
            "transfer_id": data.get('transfer_id')
        }), 200 if success else 400
        
    except Exception as e:
        return jsonify({"status": "error", "message": "Error interno"}), 500

@app.route('/api/private/transfer/status/<transfer_id>', methods=['GET'])
@require_admin_auth
def get_transfer_status(user_id, session_token, transfer_id):
    """
    Obtiene estado de una transferencia.
    SOLO información privada visible para admin.
    """
    status = transfer_handler.get_transfer_status(
        user_id=user_id,
        session_token=session_token,
        transfer_id=transfer_id
    )
    
    if not status:
        return jsonify({"error": "No encontrado o no autorizado"}), 404
    
    return jsonify(status), 200

@app.route('/api/private/audit/log', methods=['GET'])
@require_admin_auth
def get_audit_log(user_id, session_token):
    """
    Obtiene log de auditoría privado.
    SOLO para victorhugoramirezsalgado
    Datos completamente encriptados.
    """
    log = transfer_handler.get_audit_log(
        user_id=user_id,
        session_token=session_token
    )
    
    if not log:
        return jsonify({"error": "No autorizado"}), 401
    
    return jsonify({
        "status": "success",
        "audit_log": log,
        "count": len(log)
    }), 200

@app.route('/api/health/private', methods=['GET'])
def health_check():
    """Verificación de estado (información mínima)"""
    return jsonify({"status": "online"}), 200

@app.errorhandler(404)
def not_found(error):
    """Endpoint no encontrado"""
    return jsonify({"error": "Recurso no encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Error interno del servidor"""
    return jsonify({"error": "Error interno"}), 500

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        ssl_context='adhoc'
    )