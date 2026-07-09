"""
alpaca_integration.py
Módulo de integración entre la cuenta de Alpaca (Asesor en Inversiones Plata)
y el motor de ciclos de Intertopía.

Reemplaza la necesidad de leer PDFs manualmente: consulta directamente la
API de Alpaca (Trading API - Account Activities) y transforma las
operaciones ejecutadas en un "ciclo" compatible con historial_ciclos.json.

Requiere las siguientes variables de entorno (configúralas como GitHub
Secrets, igual que hiciste con GEMINI_API_KEY):

    ALPACA_API_KEY_ID
    ALPACA_API_SECRET_KEY
    ALPACA_BASE_URL   -> "https://api.alpaca.markets" (cuenta real)
                          "https://paper-api.alpaca.markets" (paper trading)

Uso típico dentro de main.py:

    from alpaca_integration import obtener_ciclo_del_dia, aplicar_reparto

    ciclo = obtener_ciclo_del_dia()
    resultado = aplicar_reparto(ciclo["ganancia_neta"])
"""

import os
import json
import requests
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

API_KEY_ID = os.environ.get("ALPACA_API_KEY_ID")
API_SECRET_KEY = os.environ.get("ALPACA_API_SECRET_KEY")
BASE_URL = os.environ.get("ALPACA_BASE_URL", "https://api.alpaca.markets")

HISTORIAL_PATH = Path("historial_ciclos.json")
PATRIMONIO_PATH = Path("patrimonio_base.json")

# Parámetros del protocolo Intertopía (confirmados en sesiones previas)
SPLIT_USUARIO = 0.90
SPLIT_INTERTOPIA = 0.10
FONDO_RESPALDO_PCT = 0.30  # 30% de la parte del usuario, va a plata


def _headers():
    if not API_KEY_ID or not API_SECRET_KEY:
        raise EnvironmentError(
            "Faltan credenciales de Alpaca. Define ALPACA_API_KEY_ID y "
            "ALPACA_API_SECRET_KEY como variables de entorno / GitHub Secrets."
        )
    return {
        "APCA-API-KEY-ID": API_KEY_ID,
        "APCA-API-SECRET-KEY": API_SECRET_KEY,
    }


# ---------------------------------------------------------------------------
# Obtención de operaciones desde Alpaca
# ---------------------------------------------------------------------------

def obtener_actividades(fecha: str = None):
    """
    Obtiene las actividades de tipo 'FILL' (operaciones ejecutadas) de la
    cuenta para una fecha dada (formato 'YYYY-MM-DD'). Si no se especifica,
    usa la fecha actual en UTC.

    Documentación: https://docs.alpaca.markets/reference/getaccountactivities
    """
    if fecha is None:
        fecha = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    url = f"{BASE_URL}/v2/account/activities/FILL"
    params = {"date": fecha}

    try:
        resp = requests.get(url, headers=_headers(), params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"[alpaca_integration] Error al consultar Alpaca: {e}")
        return []


def calcular_ganancia_neta(actividades: list) -> float:
    """
    Suma el net_amount de todas las operaciones del día.
    Compras restan (salida de efectivo), ventas suman (entrada de efectivo).
    Esto refleja el flujo de caja neto del ciclo, no la rentabilidad de
    posiciones abiertas que aún no se han vendido.
    """
    total = 0.0
    for act in actividades:
        try:
            total += float(act.get("net_amount", 0))
        except (TypeError, ValueError):
            continue
    return round(total, 2)


def obtener_ciclo_del_dia(fecha: str = None) -> dict:
    """
    Devuelve un diccionario resumen del ciclo, listo para pasarse a
    aplicar_reparto() y para anexarse a historial_ciclos.json.
    """
    actividades = obtener_actividades(fecha)
    ganancia_neta = calcular_ganancia_neta(actividades)

    return {
        "fecha": fecha or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "num_operaciones": len(actividades),
        "ganancia_neta": ganancia_neta,
        "operaciones": [
            {
                "symbol": a.get("symbol"),
                "side": a.get("side"),
                "qty": a.get("qty"),
                "price": a.get("price"),
                "net_amount": a.get("net_amount"),
                "order_id": a.get("order_id"),
            }
            for a in actividades
        ],
    }


# ---------------------------------------------------------------------------
# Lógica de reparto 90/10 + fondo de respaldo
# ---------------------------------------------------------------------------

def aplicar_reparto(ganancia_neta: float) -> dict:
    """
    Aplica el protocolo de reparto de Intertopía sobre una ganancia neta:
      - 90% para Víctor Hugo
      - 10% para Intertopía (reserva en plata)
      - 30% de la parte de Víctor Hugo va al fondo de respaldo (también plata)
    """
    if ganancia_neta <= 0:
        # Lógica de cascada de pérdidas: no hay reparto positivo,
        # se registra la pérdida para el sistema de cascada.
        return {
            "ganancia_neta": ganancia_neta,
            "parte_usuario": 0.0,
            "parte_intertopia": 0.0,
            "fondo_respaldo": 0.0,
            "disponible_usuario": 0.0,
            "perdida_a_cascada": abs(ganancia_neta),
        }

    parte_usuario = round(ganancia_neta * SPLIT_USUARIO, 2)
    parte_intertopia = round(ganancia_neta * SPLIT_INTERTOPIA, 2)
    fondo_respaldo = round(parte_usuario * FONDO_RESPALDO_PCT, 2)
    disponible_usuario = round(parte_usuario - fondo_respaldo, 2)

    return {
        "ganancia_neta": ganancia_neta,
        "parte_usuario": parte_usuario,
        "parte_intertopia": parte_intertopia,
        "fondo_respaldo": fondo_respaldo,
        "disponible_usuario": disponible_usuario,
        "perdida_a_cascada": 0.0,
    }


# ---------------------------------------------------------------------------
# Persistencia (mismo patrón que ya usas en main.py)
# ---------------------------------------------------------------------------

def guardar_ciclo(ciclo: dict, reparto: dict):
    """
    Anexa el ciclo del día a historial_ciclos.json, incluyendo el reparto
    calculado. Compatible con la estructura que ya usa Intertopía.
    """
    historial = []
    if HISTORIAL_PATH.exists():
        with open(HISTORIAL_PATH, "r", encoding="utf-8") as f:
            historial = json.load(f)

    registro = {**ciclo, "reparto": reparto}
    historial.append(registro)

    with open(HISTORIAL_PATH, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

    print(f"[alpaca_integration] Ciclo del {ciclo['fecha']} guardado. "
          f"Ganancia neta: ${ciclo['ganancia_neta']}")


# ---------------------------------------------------------------------------
# Punto de entrada para pruebas manuales / GitHub Actions
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    ciclo = obtener_ciclo_del_dia()
    reparto = aplicar_reparto(ciclo["ganancia_neta"])
    print(json.dumps({"ciclo": ciclo, "reparto": reparto}, indent=2, ensure_ascii=False))
    guardar_ciclo(ciclo, reparto)
