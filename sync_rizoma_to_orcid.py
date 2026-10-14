import os
import requests
import json

# Terminal VHRS - Credenciales
ORCID_ID = "0009-0002-7831-8433"
ORCID_TOKEN = os.getenv("ORCID_TOKEN") # Debe tener permisos /activities/update

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ORCID_TOKEN}"
}

def agregar_educacion_orcid(institucion, ciudad, region, pais, titulo, año_inicio, año_fin=None):
    url = f"https://api.orcid.org/v3.0/{ORCID_ID}/education"
    
    payload = {
        "organization": {
            "name": institucion,
            "address": {
                "city": ciudad,
                "region": region,
                "country": pais
            }
        },
        "role-title": titulo,
        "start-date": {"year": {"value": str(año_inicio)}},
    }
    if año_fin:
        payload["end-date"] = {"year": {"value": str(año_fin)}}
        
    response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code in [200, 201]:
        print(f"[ÉXITO] Educación registrada: {titulo} en {institucion}.")
    else:
        print(f"[ERROR] Fallo al registrar educación: {response.text}")

def agregar_empleo_orcid(organizacion, ciudad, region, pais, cargo, año_inicio, año_fin=None):
    url = f"https://api.orcid.org/v3.0/{ORCID_ID}/employment"
    
    payload = {
        "organization": {
            "name": organizacion,
            "address": {
                "city": ciudad,
                "region": region,
                "country": pais
            }
        },
        "role-title": cargo,
        "start-date": {"year": {"value": str(año_inicio)}},
    }
    if año_fin:
        payload["end-date"] = {"year": {"value": str(año_fin)}}
        
    response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code in [200, 201]:
        print(f"[ÉXITO] Empleo registrado: {cargo} en {organizacion}.")
    else:
        print(f"[ERROR] Fallo al registrar empleo: {response.text}")

def ejecutar_integracion_alta_calidad():
    print("> [TERMINAL VHRS] Iniciando volcado de datos de Alta Calidad (Rizoma) a ORCID...")
    
    # 1. INTEGRACIÓN DE EDUCACIÓN (Rizoma: Hoja 2 - Formación Académica)
    print("\n--- Procesando Formación Académica ---")
    agregar_educacion_orcid("CETYS Universidad", "Ensenada", "Baja California", "MX", "Maestría en Administración de Empresas con especialidad en Mercadotecnia", "2010") # Ajusta años según tu Excel
    agregar_educacion_orcid("Universidad Xochicalco", "Ensenada", "Baja California", "MX", "Licenciatura en Comercio Internacional", "2005", "2009")
    
    # 2. INTEGRACIÓN DE EXPERIENCIA (Rizoma: Hoja 3 - Trayectoria Profesional)
    print("\n--- Procesando Trayectoria Profesional ---")
    agregar_empleo_orcid("ContenedorEns", "Ensenada", "Baja California", "MX", "Consultor Operativo y Asesor Portuario Estratégico", "2024")
    agregar_empleo_orcid("ContenedorEns / Arsa Bodegas", "Ensenada", "Baja California", "MX", "Director General", "2018")
    agregar_empleo_orcid("Administración Portuaria Integral (ASIPONA Ensenada)", "Ensenada", "Baja California", "MX", "Subgerente de Operaciones y Ecología", "2012", "2022")
    
    # Nota de sistema: Para registrar los 162 documentos oficiales (Hoja 6), ORCID utiliza el endpoint /work que requiere formato BibTeX integrado, lo cual se programa en un módulo adicional si lo requieres.

if __name__ == "__main__":
    if not ORCID_TOKEN:
        print("[ERROR CRÍTICO] Falta el token ORCID_TOKEN en el entorno.")
    else:
        ejecutar_integracion_alta_calidad()
        print("\n> [SISTEMA] Integración Rizoma-ORCID completada exitosamente.")
