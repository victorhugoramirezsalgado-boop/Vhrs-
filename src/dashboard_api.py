ni"""
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
    import { useState, useRef, useEffect } from "react";
import { Send, Loader2, Sparkles } from "lucide-react";

// Interfaz de chat con Claude para Intertopía.
// Paleta: base grafito (#14171A), acento oro viejo (#B8935A), plata fría (#C9CDD3)

export default function IntertopiaClaudeChat() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Consola de Intertopía lista. Pregúntame sobre el sistema, precios de referencia o lógica del ciclo financiero.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage() {
    const text = input.trim();
    if (!text || loading) return;

    const newMessages = [...messages, { role: "user", content: text }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-6",
          max_tokens: 1000,
          system:
            "Eres el asistente técnico de Intertopía, un sistema conceptual de seguimiento de activos (oro, plata, Bitcoin, ITC coin). Responde en español, de forma breve y precisa.",
          messages: newMessages.map((m) => ({ role: m.role, content: m.content })),
        }),
      });
      const data = await response.json();
      const textBlock = (data.content || [])
        .map((block) => (block.type === "text" ? block.text : ""))
        .join("\n")
        .trim();

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: textBlock || "No obtuve respuesta. Intenta de nuevo." },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error de conexión con Claude. Intenta de nuevo." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="flex h-screen w-full items-center justify-center bg-[#0F1113] p-4">
      <div className="flex h-full max-h-[720px] w-full max-w-2xl flex-col overflow-hidden rounded-xl border border-[#2A2E33] bg-[#14171A] shadow-2xl">
        <div className="flex items-center gap-3 border-b border-[#2A2E33] bg-[#17191C] px-5 py-4">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-[#B8935A] to-[#8A6A3E]">
            <Sparkles size={16} className="text-[#0F1113]" />
          </div>
          <div>
            <h1 className="text-sm font-semibold tracking-wide text-[#EDEBE6]">
              Intertopía · Consola Claude
            </h1>
            <p className="text-xs text-[#7C828A]">Asistente del sistema</p>
          </div>
        </div>

        <div className="flex-1 space-y-4 overflow-y-auto px-5 py-5">
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2.5 text-sm leading-relaxed ${
                  m.role === "user"
                    ? "bg-[#B8935A] text-[#14171A]"
                    : "bg-[#1E2226] text-[#C9CDD3] border border-[#2A2E33]"
                }`}
              >
                {m.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="flex items-center gap-2 rounded-lg border border-[#2A2E33] bg-[#1E2226] px-4 py-2.5 text-sm text-[#7C828A]">
                <Loader2 size={14} className="animate-spin" />
                Procesando
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="border-t border-[#2A2E33] bg-[#17191C] p-3">
          <div className="flex items-end gap-2">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Escribe tu mensaje..."
              rows={1}
              className="flex-1 resize-none rounded-lg border border-[#2A2E33] bg-[#0F1113] px-3 py-2.5 text-sm text-[#EDEBE6] placeholder-[#5A6068] outline-none focus:border-[#B8935A]"
            />
            <button
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-[#B8935A] text-[#14171A] transition-opacity disabled:opacity-40"
              aria-label="Enviar mensaje"
            >
              <Send size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}