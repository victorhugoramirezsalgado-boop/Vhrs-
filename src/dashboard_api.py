"""
Dashboard Backend API - REST endpoints para datos del dashboard
SOLO para Víctor Hugo Ramírez Salgado
"""

from flask import Flask, request, jsonify
from functools import wraps
import os
from datetime import datetime, timedelta
from src.secure_transfer import SecureTransfer
from src.liquidation_executor import LiquidationExecutor

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "SECURE_KEY")

transfer_handler = SecureTransfer()
liquidation_handler = LiquidationExecutor()

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

@app.route('/api/dashboard/overview', methods=['GET'])
@require_admin_auth
def get_overview(user_id, session_token):
    """
    Obtiene vista general del dashboard
    """
    try:
        pending_transfers = transfer_handler.auth.pending_transfers
        pending_liquidations = liquidation_handler.liquidation_system.pending_requests
        
        overview = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "admin": "Víctor Hugo Ramírez Salgado",
            "entity": "Intertopía / 1ntertopía",
            "summary": {
                "total_pending_transfers": len([t for t in pending_transfers.values() if t["status"] == "pending"]),
                "total_approved_transfers": len([t for t in pending_transfers.values() if t["status"] == "authorized"]),
                "total_pending_liquidations": len([l for l in pending_liquidations.values() if l["status"] == "pending"]),
                "total_approved_liquidations": len([l for l in pending_liquidations.values() if l["status"] == "approved"]),
                "total_executed_liquidations": len(liquidation_handler.liquidation_system.executed_liquidations)
            }
        }
        
        return jsonify(overview), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": "Error interno"}), 500

@app.route('/api/dashboard/transfers', methods=['GET'])
@require_admin_auth
def get_transfers_dashboard(user_id, session_token):
    """
    Obtiene información de transferencias para dashboard
    """
    try:
        transfers = transfer_handler.auth.pending_transfers
        
        transfers_data = []
        for transfer_id, transfer in transfers.items():
            transfers_data.append({
                "id": transfer_id[:8] + "...",
                "amount": transfer["amount"],
                "status": transfer["status"],
                "created": transfer["requested_at"],
                "type": "transfer_to_account"
            })
        
        return jsonify({
            "status": "success",
            "total": len(transfers_data),
            "transfers": transfers_data
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error"}), 500

@app.route('/api/dashboard/liquidations', methods=['GET'])
@require_admin_auth
def get_liquidations_dashboard(user_id, session_token):
    """
    Obtiene información de liquidaciones para dashboard
    """
    try:
        liquidations = liquidation_handler.liquidation_system.pending_requests
        
        liquidations_data = []
        for req_id, req in liquidations.items():
            liquidations_data.append({
                "id": req_id[:8] + "...",
                "amount_usd": req["amount_usd"],
                "asset_type": req["asset_type"],
                "source": req["source_provider"],
                "status": req["status"],
                "created": req["requested_at"],
                "type": "asset_liquidation"
            })
        
        return jsonify({
            "status": "success",
            "total": len(liquidations_data),
            "liquidations": liquidations_data
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error"}), 500

@app.route('/api/dashboard/activity', methods=['GET'])
@require_admin_auth
def get_activity(user_id, session_token):
    """
    Obtiene historial de actividad reciente
    """
    try:
        audit_logs = transfer_handler.auth.get_audit_log(user_id)
        
        if not audit_logs:
            return jsonify({"error": "No autorizado"}), 401
        
        recent_activity = []
        for log in audit_logs[-20:]:  # Últimas 20 acciones
            if isinstance(log, dict) and "action" in log:
                recent_activity.append({
                    "action": log.get("action"),
                    "timestamp": log.get("timestamp"),
                    "amount": log.get("amount", 0),
                    "details": log.get("details", "")
                })
        
        return jsonify({
            "status": "success",
            "activity": recent_activity
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error"}), 500

@app.route('/api/dashboard/stats', methods=['GET'])
@require_admin_auth
def get_stats(user_id, session_token):
    """
    Obtiene estadísticas del dashboard
    """
    try:
        transfers = transfer_handler.auth.authorized_transfers
        liquidations = liquidation_handler.liquidation_system.executed_liquidations
        
        total_transferred = sum(t.get("amount", 0) for t in transfers)
        total_liquidated = sum(l.get("amount_usd", 0) for l in liquidations)
        
        stats = {
            "status": "success",
            "statistics": {
                "total_transferred_usd": total_transferred,
                "total_liquidated_usd": total_liquidated,
                "total_transactions": len(transfers) + len(liquidations),
                "transfers_count": len(transfers),
                "liquidations_count": len(liquidations)
            }
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({"status": "error"}), 500

@app.route('/api/dashboard/health', methods=['GET'])
@require_admin_auth
def get_health(user_id, session_token):
    """
    Estado del sistema
    """
    return jsonify({
        "status": "success",
        "system": "online",
        "timestamp": datetime.now().isoformat(),
        "admin": "victorhugoramirezsalgado"
    }), 200

@app.route('/api/dashboard/export', methods=['GET'])
@require_admin_auth
def export_data(user_id, session_token):
    """
    Exporta datos completos (JSON)
    """
    try:
        audit_logs = transfer_handler.auth.get_audit_log(user_id)
        
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "admin": user_id,
            "entity": "Intertopía / 1ntertopía",
            "transfers": len(transfer_handler.auth.authorized_transfers),
            "liquidations": len(liquidation_handler.liquidation_system.executed_liquidations),
            "audit_entries": len(audit_logs) if audit_logs else 0
        }
        
        return jsonify(export_data), 200
        
    except Exception as e:
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5002,
        debug=False,
        ssl_context='adhoc'
    )