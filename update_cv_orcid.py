import os
import requests
import json

# Terminal VHRS - Conexión Real ORCID
ORCID_ID = "0009-0002-7831-8433" # ID validado de Víctor Hugo Ramírez Salgado
URL_ORCID = f"https://pub.orcid.org/v3.0/{ORCID_ID}/record"

headers = {
    "Accept": "application/json"
}

def obtener_cv_orcid():
    print(f"> [TERMINAL VHRS] Conectando con servidor real ORCID para {ORCID_ID}...")
    
    try:
        response = requests.get(URL_ORCID, headers=headers)
        
        if response.status_code == 200:
            datos = response.json()
            
            # Filtro Intertopía para estructurar el CV Máster
            cv_data = {
                "identidad": "Víctor Hugo Ramírez Salgado",
                "orcid": ORCID_ID,
                "cvu_conahcyt": "510376",
                "empleos": datos.get("activities-summary", {}).get("employments", {}).get("affiliation-group", []),
                "educacion": datos.get("activities-summary", {}).get("educations", {}).get("affiliation-group", []),
                "publicaciones": datos.get("activities-summary", {}).get("works", {}).get("group", [])
            }
            
            # Actualiza el CV Máster de forma local
            with open("cv_master_intertopia.json", "w", encoding="utf-8") as f:
                json.dump(cv_data, f, indent=4, ensure_ascii=False)
                
            print("[ÉXITO] Datos extraídos correctamente. Archivo 'cv_master_intertopia.json' actualizado y listo para sincronizar.")
        else:
            print(f"[ERROR] No se pudo acceder al registro público. Código: {response.status_code}")
            
    except Exception as e:
         print(f"[ERROR CRÍTICO] Falla de sistema: {e}")

if __name__ == "__main__":
    obtener_cv_orcid()
