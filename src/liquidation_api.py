\"\"\"\nAPI Privada de Liquidación de Activos\nSOLO para Víctor Hugo Ramírez Salgado - Administrador Único\nIntertopía / 1ntertopía\n\nLiquida SOLO la cantidad de activos que el admin solicite explícitamente\n\"\"\"\n\nfrom flask import Flask, request, jsonify\nfrom functools import wraps\nimport os\nfrom src.liquidation_executor import LiquidationExecutor\n\napp = Flask(__name__)\napp.config['SECRET_KEY'] = os.getenv(\"FLASK_SECRET_KEY\", \"SECURE_KEY_CHANGE_IN_PRODUCTION\")\n\nliquidation_handler = LiquidationExecutor()\n\n# Middleware de autenticación\ndef require_admin_auth(f):\n    @wraps(f)\n    def decorated(*args, **kwargs):\n        auth_header = request.headers.get('Authorization')\n        if not auth_header or not auth_header.startswith('Bearer '):\n            return jsonify({\"error\": \"No autorizado\"}), 401\n        \n        token = auth_header.split(' ')[1]\n        user_id = request.headers.get('X-User-ID')\n        \n        if user_id != \"victorhugoramirezsalgado\":\n            return jsonify({\"error\": \"No autorizado\"}), 401\n        \n        return f(user_id, token, *args, **kwargs)\n    \n    return decorated\n\n@app.route('/api/private/liquidation/request', methods=['POST'])\n@require_admin_auth\ndef request_liquidation(user_id, session_token):\n    \"\"\"\n    Solicita liquidación de activos por cantidad específica.\n    SOLO el administrador puede solicitar.\n    \"\"\"\n    try:\n        data = request.json\n        \n        request_id = liquidation_handler.request_asset_liquidation(\n            user_id=user_id,\n            session_token=session_token,\n            amount_usd=data.get('amount_usd'),\n            asset_type=data.get('asset_type'),\n            source_provider=data.get('source_provider'),\n            destination_account=data.get('destination_account'),\n            instruction=data.get('instruction')\n        )\n        \n        if not request_id:\n            return jsonify({\"error\": \"No se pudo crear la solicitud\"}), 400\n        \n        return jsonify({\n            \"status\": \"success\",\n            \"request_id\": request_id,\n            \"amount_usd\": data.get('amount_usd'),\n            \"message\": \"Solicitud de liquidación creada. Pendiente de aprobación.\"\n        }), 202\n        \n    except Exception as e:\n        return jsonify({\"status\": \"error\", \"message\": \"Error interno\"}), 500\n\n@app.route('/api/private/liquidation/approve', methods=['POST'])\n@require_admin_auth\ndef approve_liquidation(user_id, session_token):\n    \"\"\"\n    Aprueba una solicitud de liquidación con código 2FA.\n    \"\"\"\n    try:\n        data = request.json\n        \n        success = liquidation_handler.approve_liquidation_request(\n            user_id=user_id,\n            session_token=session_token,\n            request_id=data.get('request_id'),\n            approval_code=data.get('approval_code')\n        )\n        \n        return jsonify({\n            \"status\": \"success\" if success else \"failed\",\n            \"request_id\": data.get('request_id')\n        }), 200 if success else 400\n        \n    except Exception as e:\n        return jsonify({\"status\": \"error\", \"message\": \"Error interno\"}), 500\n\n@app.route('/api/private/liquidation/execute', methods=['POST'])\n@require_admin_auth\ndef execute_liquidation(user_id, session_token):\n    \"\"\"\n    Ejecuta la liquidación de activos.\n    Vende SOLO la cantidad solicitada.\n    \"\"\"\n    try:\n        data = request.json\n        \n        success = liquidation_handler.execute_liquidation_request(\n            user_id=user_id,\n            session_token=session_token,\n            request_id=data.get('request_id'),\n            execution_code=data.get('execution_code')\n        )\n        \n        return jsonify({\n            \"status\": \"success\" if success else \"failed\",\n            \"request_id\": data.get('request_id'),\n            \"message\": \"Liquidación ejecutada - Dinero físico enviado\" if success else \"Error en ejecución\"\n        }), 200 if success else 400\n        \n    except Exception as e:\n        return jsonify({\"status\": \"error\", \"message\": \"Error interno\"}), 500\n\n@app.route('/api/private/liquidation/status/<request_id>', methods=['GET'])\n@require_admin_auth\ndef get_status(user_id, session_token, request_id):\n    \"\"\"\n    Obtiene estado de una solicitud de liquidación.\n    \"\"\"\n    status = liquidation_handler.get_liquidation_status(\n        user_id=user_id,\n        session_token=session_token,\n        request_id=request_id\n    )\n    \n    if not status:\n        return jsonify({\"error\": \"No encontrado\"}), 404\n    \n    return jsonify(status), 200\n\n@app.route('/api/private/liquidation/audit', methods=['GET'])\n@require_admin_auth\ndef get_audit(user_id, session_token):\n    \"\"\"\n    Obtiene auditoría de liquidaciones.\n    Datos encriptados - SOLO ADMIN.\n    \"\"\"\n    audit = liquidation_handler.get_liquidation_audit(\n        user_id=user_id,\n        session_token=session_token\n    )\n    \n    if not audit:\n        return jsonify({\"error\": \"No autorizado\"}), 401\n    \n    return jsonify({\n        \"status\": \"success\",\n        \"audit_log\": audit,\n        \"count\": len(audit)\n    }), 200\n\n@app.route('/api/health/liquidation', methods=['GET'])\ndef health():\n    \"\"\"Estado del servicio\"\"\"\n    return jsonify({\"status\": \"online\", \"service\": \"liquidation\"}), 200\n\n@app.errorhandler(404)\ndef not_found(error):\n    return jsonify({\"error\": \"Recurso no encontrado\"}), 404\n\n@app.errorhandler(500)\ndef internal_error(error):\n    return jsonify({\"error\": \"Error interno\"}), 500\n\nif __name__ == '__main__':\n    app.run(\n        host='127.0.0.1',\n        port=5001,\n        debug=False,\n        ssl_context='adhoc'\n    )\n
import os
import pyotp
import requests
from github import Github


class AdministradorSoberanoAuth:

    def __init__(self, admin_secret_seed):
        # Semilla secreta para Google Authenticator (2FA TOTP)
        self.totp = pyotp.TOTP(admin_secret_seed)

    def validar_2fa(self, codigo_ingresado):
        """Valida el código 2FA de Google aleatorio en tiempo real."""
        return self.totp.verify(codigo_ingresado)


class CapitalComLiquidationSovereign:

    def __init__(
        self,
        api_key,
        account_id,
        github_token,
        repo_name,
        admin_secret_seed,
    ):
        self.api_key = api_key
        self.account_id = account_id
        self.base_url = "https://api.capital.com/api/v1"
        self.github = Github(github_token)
        self.repo = self.github.get_repo(repo_name)
        self.auth = AdministradorSoberanoAuth(admin_secret_seed)

    def ejecutar_transferencia_soberana(
        self, amount, currency, bank_account_id, codigo_2fa
    ):
        """Ejecuta la salida de capital validando límites, costos en cálculo separado y 2FA."""
        # 1. Validación estricta de Autenticación de Segundo Factor (2FA)
        if not self.auth.validar_2fa(codigo_2fa):
            return {
                "error": "Acceso denegado: Autenticación 2FA de Google inválida."
            }

        # 2. Verificación de límites en USD (Mínimo $1,000 - Máximo $249,000)
        if currency.upper() == "USD":
            if amount < 1000:
                return {
                    "error": "Monto inferior al límite operativo mínimo de $1,000 USD."
                }
            if amount > 249000:
                return {
                    "error": "Monto superior al límite de resguardo diario de $249,000 USD."
                }

        # 3. Ejecución de salida hacia banca tradicional en Capital.com
        endpoint = "withdrawal"
        headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}
        payload = {
            "amount": amount,
            "currency": currency,
            "destination": bank_account_id,
        }

        try:
            response = requests.post(
                f"{self.base_url}/{endpoint}", headers=headers, json=payload
            )
            if response.status_code == 200:
                # Generación de certificado y registro inalterable en GitHub
                commit_message = f"Autorización V.H.R.S. - Retiro validado: {amount} {currency} a {bank_account_id}"
                self.repo.create_file(
                    path=f"logs/liquidation_sovereign_{bank_account_id}.log",
                    message=commit_message,
                    content=str(response.json()),
                    branch="main",
                )
                return {
                    "status": "Sovereign Transfer Executed & Certified",
                    "data": response.json(),
                }
            else:
                return {
                    "error": "Fallo en la terminal de salida hacia banca tradicional."
                }
        except Exception as e:
            return {"error": f"Excepción de sistema: {str(e)}"}
