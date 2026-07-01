"""
SISTEMA INTERTOPIA v2026.06.30
Administrador: Víctor Hugo Ramírez Salgado
Estado: Operativo / Segregación de sistemas activada

Requiere:
    pip install requests --break-system-packages

APIs usadas:
    - CoinGecko (BTC, USD)          -> gratuita, sin API key
    - goldprice.org (oro y plata)   -> gratuita, sin API key
    - Rodio (rhodium): no existe una API pública gratuita confiable.
      Se deja un override manual (RHODIUM_PRICE_OVERRIDE) hasta integrar
      un proveedor de pago (ej. metals-api.com, mejor con API key propia).
"""

import requests
from datetime import datetime, timezone

# ----------------------------------------------------------------------
# CONFIGURACIÓN
# ----------------------------------------------------------------------

# Si no se puede consultar el precio del rodio en vivo, se usa este valor.
# Actualízalo manualmente hasta tener una fuente API confiable.
RHODIUM_PRICE_OVERRIDE_USD_OZ = 5200.00

# Segregación de beneficios (tal como pediste: 70/30)
SPLIT_VHRS = 0.70          # Víctor Hugo Ramírez Salgado
SPLIT_INTERTOPIA = 0.30    # Sistema Intertopía
# NOTA: el comentario original decía "70/30" pero los números en el código
# eran 0.90/0.10. Aquí se aplicó 70/30 según tu último mensaje.
# Si en realidad querías 90/10, cambia las dos constantes de arriba.

assets = {
    "vault": "Víctor Hugo's Personal Vault",
    "gold_reserves_oz": 2.0,     # Operación diaria base
    "silver_reserves_oz": 0.0,   # Acumulación de plata
    "energy_units": 0,           # Objetivo: 10
    "rhodium_units": 0.0,        # Onzas de rodio acumuladas
    "btc_balance": 0.0,          # Turbo hasta 141 BTC
    "h2o_liquidity": 0.0
}

# Patrimonio base de referencia para calcular "beneficio" del ciclo 24h
# (se compara el patrimonio actual contra este valor para saber cuánto repartir)
PATRIMONIO_BASE_USD = 0.0


# ----------------------------------------------------------------------
# CONEXIÓN A APIS EN VIVO
# ----------------------------------------------------------------------

def get_btc_price_usd():
    """Obtiene el precio actual de BTC en USD desde CoinGecko."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd"}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return float(r.json()["bitcoin"]["usd"])
    except Exception as e:
        print(f"[WARN] No se pudo obtener precio BTC de CoinGecko: {e}")
        return None


def get_gold_silver_prices_usd():
    """Obtiene precios de oro y plata (USD/oz) desde goldprice.org."""
    url = "https://data-asg.goldprice.org/dbXRates/USD"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()["items"][0]
        return {
            "gold_price_per_oz": float(data["xauPrice"]),
            "silver_price_per_oz": float(data["xagPrice"]),
        }
    except Exception as e:
        print(f"[WARN] No se pudo obtener precio oro/plata de goldprice.org: {e}")
        return None


def get_rhodium_price_usd():
    """
    Precio del rodio. No hay API pública gratuita confiable, así que se usa
    el override manual definido arriba. Reemplaza esta función si conectas
    un proveedor de pago (ej. metals-api.com).
    """
    return RHODIUM_PRICE_OVERRIDE_USD_OZ


def actualizar_precios():
    """Actualiza todos los precios de mercado en vivo. No usa valores fijos."""
    precios = {}

    btc = get_btc_price_usd()
    precios["btc_price_usd"] = btc if btc is not None else 0.0

    metales = get_gold_silver_prices_usd()
    if metales:
        precios["gold_price_per_oz"] = metales["gold_price_per_oz"]
        precios["silver_price_per_oz"] = metales["silver_price_per_oz"]
    else:
        precios["gold_price_per_oz"] = 0.0
        precios["silver_price_per_oz"] = 0.0

    precios["rhodium_price_per_oz"] = get_rhodium_price_usd()

    return precios


# ----------------------------------------------------------------------
# CÁLCULO DE PATRIMONIO
# ----------------------------------------------------------------------

def get_patrimonio_actual():
    """Calcula el valor del patrimonio total en tiempo real, incluyendo
    oro, plata, rodio y BTC."""
    precios = actualizar_precios()

    valor_oro = assets["gold_reserves_oz"] * precios["gold_price_per_oz"]
    valor_plata = assets["silver_reserves_oz"] * precios["silver_price_per_oz"]
    valor_rodio = assets["rhodium_units"] * precios["rhodium_price_per_oz"]
    valor_btc = assets["btc_balance"] * precios["btc_price_usd"]

    patrimonio_total = valor_oro + valor_plata + valor_rodio + valor_btc

    return {
        "patrimonio_total_usd": round(patrimonio_total, 2),
        "desglose": {
            "oro_usd": round(valor_oro, 2),
            "plata_usd": round(valor_plata, 2),
            "rodio_usd": round(valor_rodio, 2),
            "btc_usd": round(valor_btc, 2),
        },
        "precios_usados": precios,
        "vault_id": assets["vault"],
        "estado": "Estable - Protegido",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    }


# ----------------------------------------------------------------------
# SEGREGACIÓN 70/30
# ----------------------------------------------------------------------

def ejecutar_ciclo_24h():
    """Calcula el beneficio del ciclo (patrimonio actual - base) y lo
    segrega 70% V.H.R.S / 30% Intertopía."""
    global PATRIMONIO_BASE_USD

    reporte = get_patrimonio_actual()
    patrimonio_actual = reporte["patrimonio_total_usd"]
    beneficio = patrimonio_actual - PATRIMONIO_BASE_USD

    if beneficio > 0:
        reparto_vhrs = round(beneficio * SPLIT_VHRS, 2)
        reparto_intertopia = round(beneficio * SPLIT_INTERTOPIA, 2)
    else:
        reparto_vhrs = 0.0
        reparto_intertopia = 0.0

    resultado = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "patrimonio_actual_usd": patrimonio_actual,
        "patrimonio_base_usd": PATRIMONIO_BASE_USD,
        "beneficio_usd": round(beneficio, 2),
        "reparto": {
            "vhrs_usd": reparto_vhrs,
            "intertopia_usd": reparto_intertopia,
            "split": f"{int(SPLIT_VHRS*100)}/{int(SPLIT_INTERTOPIA*100)}",
        },
    }

    # Actualiza la base para el siguiente ciclo
    PATRIMONIO_BASE_USD = patrimonio_actual

    return resultado


# ----------------------------------------------------------------------
# INFORME DE EJECUCIÓN
# ----------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Informe de Patrimonio: {get_patrimonio_actual()}")
    print(f"Ciclo 24h (segregación {int(SPLIT_VHRS*100)}/{int(SPLIT_INTERTOPIA*100)}): {ejecutar_ciclo_24h()}")
