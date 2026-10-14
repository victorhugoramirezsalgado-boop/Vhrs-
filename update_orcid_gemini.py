import os
import requests
import json
import google.generativeai as genai

# Variables de entorno seguras (GitHub Secrets)
ORCID_ID = os.getenv("ORCID_ID", "0009-0002-7831-8433")
ORCID_TOKEN = os.getenv("ORCID_TOKEN") # Token OAuth de ORCID con permisos /activities/update
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def procesar_datos_con_gemini():
    print("> [TERMINAL VHRS] Iniciando Inteligencia Gemini para validación de datos Rizoma...")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    # Datos extraídos de tu CV Rizoma (Biografía Máster)
    biografia_cruda = (
        "Licenciado en Comercio Internacional (Universidad Xochicalco) y Maestro en Administración con concentración en Mercadotecnia (CETYS Universidad), con certificación EC0217 del CONOCER, suma 21 años de experiencia profesional en la industria marítimo-portuaria (desde 2005); de ellos, durante 12 años fue servidor público federal en la Administración Portuaria Integral de Ensenada (hoy ASIPONA Ensenada), donde de 2012 a 2022 elaboró la estadística portuaria oficial de Ensenada, El Sauzal y Costa Azul para la Coordinación General de Puertos y Marina Mercante, con más de 162 documentos oficiales generados, validados y emitidos. Fue Subgerente de Operaciones y Ecología, integrante del equipo auditor interno y fundador y coordinador del 1er Simposio Nacional de Recintos Fiscalizados de las API (2013). En 2014 cursó el diplomado de la Universidad de Cantabria en Santander, cuya memoria propone un organismo regulador de estadísticas portuarias para América, y abrió la ruta que llevó a API Ensenada al proyecto del primer puerto verde de México. Fue docente de licenciatura de 2013 a 2017 en la Universidad Xochicalco y en la Universidad Autónoma de Durango. Desde 2018 dirige ContenedorEns y Arsa Bodegas, y desde febrero de 2024 es Consultor Operativo y Asesor Portuario Estratégico, en alianza con ContenedorEns. Su línea de investigación es el segundo uso de contenedores marítimos en México y su registro estadístico, fiscal y sanitario."
    )
    
    # Gemini actúa como filtro de calidad Intertopía
    prompt = f"Como sistema Intertopía, valida la siguiente biografía de Víctor Hugo Ramírez Salgado. Corrige cualquier error ortográfico o de sintaxis para un perfil académico de alto nivel. Devuelve ÚNICAMENTE el texto final, sin comillas ni saludos:\n\n{biografia_cruda}"
    
    respuesta = model.generate_content(prompt)
    return respuesta.text.strip()

def inyectar_en_orcid(texto_validado):
    print(f"> [TERMINAL VHRS] Conectando con API ORCID para actualizar registro: {ORCID_ID}...")
    
    url = f"https://api.orcid.org/v3.0/{ORCID_ID}/person/biography"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ORCID_TOKEN}"
    }
    
    # Esquema estricto JSON requerido por ORCID
    payload = {
        "visibility": "PUBLIC",
        "content": texto_validado
    }
    
    response = requests.put(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code in [200, 201]:
        print("[ÉXITO] Biografía de CV Máster actualizada correctamente en ORCID.")
    else:
        print(f"[ERROR CRÍTICO] Código ORCID: {response.status_code}. Detalles: {response.text}")

if __name__ == "__main__":
    if not ORCID_TOKEN or not GEMINI_API_KEY:
        print("[ERROR] Faltan Credenciales en GitHub Secrets (ORCID_TOKEN o GEMINI_API_KEY).")
        exit(1)
        
    biografia_final = procesar_datos_con_gemini()
    inyectar_en_orcid(biografia_final)
