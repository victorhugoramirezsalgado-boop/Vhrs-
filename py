"""
INTERTOPIA Terminal Engine v2026.09.30
Administrador: Víctor Hugo Ramírez Salgado
Estado: Operativo / Segregación de sistemas activada
Soporte de divisas: USD, MXN (Peso Mexicano)

Requiere:
    pip install requests --break-system-packages

APIs usadas:
    - CoinGecko (BTC, USD)                    -> gratuita, sin API key
    - goldprice.org (oro y plata)             -> gratuita, sin API key
    - ExchangeRate-API (USD/MXN)              -> gratuita (1500 req/mes)
    - Rodio (rhodium): override manual hasta integrar metals-api.com
"""

import requests
from datetime import datetime, timezone

# -------------------------------------------------------
# CONFIGURACIÓN
# -------------------------------------------------------

# Precio del rodio (sin API pública gratuita confiable)
RHODIUM_PRICE_OVERRIDE_USD_OZ = 5200.00

# Segregación de beneficios: 70% V.H.R.S / 30% Intertopía
SPLIT_VHRS = 0.70
SPLIT_INTERTOPIA = 0.30

# Activos del Vault (actualizados)
assets = {
    "vault": "Víctor Hugo's Personal Vault",
    "gold_reserves_oz": 5.5,          # Onzas de oro
    "silver_reserves_oz": 12.0,       # Onzas de plata
    "energy_units": 0,                # Objetivo: 10
    "rhodium_units": 2.5,             # Onzas de rodio
    "btc_balance": 0.15,              # Bitcoin (turbo hasta 141 BTC)
    "h2o_liquidity": 0.0              # Agua (reservas de liquidez)
}

# Patrimonio base para calcular beneficio del ciclo 24h
PATRIMONIO_BASE_USD = 0.0

# Tasa de cambio USD a MXN (se actualiza dinámicamente)
EXCHANGE_RATE_USD_MXN = 17.50  # Valor por defecto


# -------------------------------------------------------
# OBTENER TIPOS DE CAMBIO EN VIVO
# -------------------------------------------------------

def get_usd_to_mxn_rate():
    """Obtiene la tasa de cambio USD/MXN actual desde ExchangeRate-API."""
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        rate = float(data["rates"].get("MXN", EXCHANGE_RATE_USD_MXN))
        print(f"[INFO] Tasa USD/MXN actualizada: {rate:.2f}")
        return rate
    except Exception as e:
        print(f"[WARN] No se pudo obtener tasa USD/MXN: {e}. Usando valor por defecto: {EXCHANGE_RATE_USD_MXN}")
        return EXCHANGE_RATE_USD_MXN


# -------------------------------------------------------
# CONEXIÓN A APIs EN VIVO (PRECIOS DE ACTIVOS)
# -------------------------------------------------------

def get_btc_price_usd():
    """Obtiene el precio actual de BTC en USD desde CoinGecko."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd"}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        price = float(r.json()["bitcoin"]["usd"])
        print(f"[INFO] Precio BTC: ${price:,.2f} USD")
        return price
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
        gold_price = float(data["xauPrice"])
        silver_price = float(data["xagPrice"])
        print(f"[INFO] Oro: ${gold_price:,.2f}/oz | Plata: ${silver_price:,.2f}/oz")
        return {
            "gold_price_per_oz": gold_price,
            "silver_price_per_oz": silver_price,
        }
    except Exception as e:
        print(f"[WARN] No se pudo obtener precio oro/plata de goldprice.org: {e}")
        return None


def get_rhodium_price_usd():
    """Precio del rodio (override manual sin API pública gratuita confiable)."""
    print(f"[INFO] Rodio (override): ${RHODIUM_PRICE_OVERRIDE_USD_OZ:,.2f}/oz")
    return RHODIUM_PRICE_OVERRIDE_USD_OZ


def actualizar_precios():
    """Actualiza todos los precios de mercado en vivo."""
    print("\n[ACTUALIZAR PRECIOS]")
    precios = {}
    
    # Tasa de cambio
    exchange_rate = get_usd_to_mxn_rate()
    precios["usd_to_mxn"] = exchange_rate

    # Bitcoin
    btc = get_btc_price_usd()
    precios["btc_price_usd"] = btc if btc is not None else 0.0
    precios["btc_price_mxn"] = (btc * exchange_rate) if btc is not None else 0.0

    # Metales preciosos
    metales = get_gold_silver_prices_usd()
    if metales:
        precios["gold_price_per_oz_usd"] = metales["gold_price_per_oz"]
        precios["gold_price_per_oz_mxn"] = metales["gold_price_per_oz"] * exchange_rate
        precios["silver_price_per_oz_usd"] = metales["silver_price_per_oz"]
        precios["silver_price_per_oz_mxn"] = metales["silver_price_per_oz"] * exchange_rate
    else:
        precios["gold_price_per_oz_usd"] = 0.0
        precios["gold_price_per_oz_mxn"] = 0.0
        precios["silver_price_per_oz_usd"] = 0.0
        precios["silver_price_per_oz_mxn"] = 0.0

    # Rodio
    rhodium_usd = get_rhodium_price_usd()
    precios["rhodium_price_per_oz_usd"] = rhodium_usd
    precios["rhodium_price_per_oz_mxn"] = rhodium_usd * exchange_rate

    return precios


# -------------------------------------------------------
# CÁLCULO DE PATRIMONIO (USD Y MXN)
# -------------------------------------------------------

def get_patrimonio_actual():
    """Calcula el valor del patrimonio total en tiempo real (USD y MXN)."""
    precios = actualizar_precios()
    exchange_rate = precios["usd_to_mxn"]

    # Valores en USD
    valor_oro_usd = assets["gold_reserves_oz"] * precios["gold_price_per_oz_usd"]
    valor_plata_usd = assets["silver_reserves_oz"] * precios["silver_price_per_oz_usd"]
    valor_rodio_usd = assets["rhodium_units"] * precios["rhodium_price_per_oz_usd"]
    valor_btc_usd = assets["btc_balance"] * precios["btc_price_usd"]

    patrimonio_total_usd = valor_oro_usd + valor_plata_usd + valor_rodio_usd + valor_btc_usd
    
    # Valores en MXN
    valor_oro_mxn = valor_oro_usd * exchange_rate
    valor_plata_mxn = valor_plata_usd * exchange_rate
    valor_rodio_mxn = valor_rodio_usd * exchange_rate
    valor_btc_mxn = valor_btc_usd * exchange_rate
    patrimonio_total_mxn = patrimonio_total_usd * exchange_rate

    return {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "vault_id": assets["vault"],
        "estado": "Estable - Protegido",
        "exchange_rate_usd_mxn": round(exchange_rate, 4),
        "patrimonio_total_usd": round(patrimonio_total_usd, 2),
        "patrimonio_total_mxn": round(patrimonio_total_mxn, 2),
        "desglose_usd": {
            "oro_usd": round(valor_oro_usd, 2),
            "plata_usd": round(valor_plata_usd, 2),
            "rodio_usd": round(valor_rodio_usd, 2),
            "btc_usd": round(valor_btc_usd, 2),
        },
        "desglose_mxn": {
            "oro_mxn": round(valor_oro_mxn, 2),
            "plata_mxn": round(valor_plata_mxn, 2),
            "rodio_mxn": round(valor_rodio_mxn, 2),
            "btc_mxn": round(valor_btc_mxn, 2),
        },
        "activos": {
            "gold_oz": assets["gold_reserves_oz"],
            "silver_oz": assets["silver_reserves_oz"],
            "rhodium_oz": assets["rhodium_units"],
            "btc": assets["btc_balance"],
        },
        "precios_usados": precios,
    }


# -------------------------------------------------------
# SEGREGACIÓN 70/30 (CICLO 24H)
# -------------------------------------------------------

def ejecutar_ciclo_24h():
    """Calcula el beneficio del ciclo y lo segrega 70% V.H.R.S / 30% Intertopía."""
    global PATRIMONIO_BASE_USD

    reporte = get_patrimonio_actual()
    patrimonio_actual_usd = reporte["patrimonio_total_usd"]
    patrimonio_actual_mxn = reporte["patrimonio_total_mxn"]
    exchange_rate = reporte["exchange_rate_usd_mxn"]
    
    beneficio_usd = patrimonio_actual_usd - PATRIMONIO_BASE_USD
    beneficio_mxn = beneficio_usd * exchange_rate

    if beneficio_usd > 0:
        reparto_vhrs_usd = round(beneficio_usd * SPLIT_VHRS, 2)
        reparto_intertopia_usd = round(beneficio_usd * SPLIT_INTERTOPIA, 2)
        reparto_vhrs_mxn = round(beneficio_mxn * SPLIT_VHRS, 2)
        reparto_intertopia_mxn = round(beneficio_mxn * SPLIT_INTERTOPIA, 2)
    else:
        reparto_vhrs_usd = 0.0
        reparto_intertopia_usd = 0.0
        reparto_vhrs_mxn = 0.0
        reparto_intertopia_mxn = 0.0

    resultado = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "patrimonio_actual_usd": patrimonio_actual_usd,
        "patrimonio_actual_mxn": patrimonio_actual_mxn,
        "patrimonio_base_usd": PATRIMONIO_BASE_USD,
        "beneficio_usd": round(beneficio_usd, 2),
        "beneficio_mxn": round(beneficio_mxn, 2),
        "reparto": {
            "vhrs_usd": reparto_vhrs_usd,
            "vhrs_mxn": reparto_vhrs_mxn,
            "intertopia_usd": reparto_intertopia_usd,
            "intertopia_mxn": reparto_intertopia_mxn,
            "split": f"{int(SPLIT_VHRS*100)}/{int(SPLIT_INTERTOPIA*100)}",
        },
        "exchange_rate": exchange_rate,
    }

    # Actualiza la base para el siguiente ciclo
    PATRIMONIO_BASE_USD = patrimonio_actual_usd

    return resultado


# -------------------------------------------------------
# INFORME DE EJECUCIÓN
# -------------------------------------------------------

if __name__ == "__main__":
    print("=" * 90)
    print("INTERTOPIA TERMINAL ENGINE - INFORME DE PATRIMONIO ACTUAL")
    print("=" * 90)
    print()
    
    patrimonio = get_patrimonio_actual()
    print(f"📊 PATRIMONIO TOTAL ACTUAL:")
    print(f"   💵 USD: ${patrimonio['patrimonio_total_usd']:>15,.2f}")
    print(f"   🇲🇽 MXN: ${patrimonio['patrimonio_total_mxn']:>15,.2f}")
    print(f"   📈 Tasa USD/MXN: {patrimonio['exchange_rate_usd_mxn']:.4f}")
    print()
    
    print(f"🏆 DESGLOSE POR ACTIVO (USD):")
    for activo, valor in patrimonio['desglose_usd'].items():
        print(f"   • {activo:15s}: ${valor:>15,.2f}")
    print()
    
    print(f"🏆 DESGLOSE POR ACTIVO (MXN):")
    for activo, valor in patrimonio['desglose_mxn'].items():
        print(f"   • {activo:15s}: ${valor:>15,.2f}")
    print()
    
    print(f"📦 INVENTARIO DE ACTIVOS:")
    for activo, cantidad in patrimonio['activos'].items():
        unidad = "oz" if activo != "btc" else "BTC"
        print(f"   • {activo.upper():20s}: {cantidad:>10.4f} {unidad}")
    print()
    
    ciclo = ejecutar_ciclo_24h()
    print(f"📈 CICLO 24H - SEGREGACIÓN {int(SPLIT_VHRS*100)}/{int(SPLIT_INTERTOPIA*100)}:")
    print(f"   Beneficio USD: ${ciclo['beneficio_usd']:>15,.2f}")
    print(f"   Beneficio MXN: ${ciclo['beneficio_mxn']:>15,.2f}")
    print()
    print(f"   👤 V.H.R.S (70%):")
    print(f"      USD: ${ciclo['reparto']['vhrs_usd']:>18,.2f}")
    print(f"      MXN: ${ciclo['reparto']['vhrs_mxn']:>18,.2f}")
    print()
    print(f"   🌐 Intertopía (30%):")
    print(f"      USD: ${ciclo['reparto']['intertopia_usd']:>18,.2f}")
    print(f"      MXN: ${ciclo['reparto']['intertopia_mxn']:>18,.2f}")
    print()
    print("=" * 90)
