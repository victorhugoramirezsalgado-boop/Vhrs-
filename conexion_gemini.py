import os
import requests

# Identidad del Sistema
ADMINISTRADOR = "Víctor Hugo Ramírez Salgado, Ase. (Administrador Único y Soberano)"

# La llave secreta de Gemini se obtendrá de forma segura de GitHub Secrets
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def conectar_con_gemini(instruccion):
    """
    Ejecuta órdenes directas hacia Gemini.
    """
    if not GEMINI_API_KEY:
        print("❌ Error: No se encontró la API Key de Gemini. Debes configurarla en los Secrets de tu repositorio.")
        return

    print(f"Iniciando protocolo de conexión...\nAutoridad: {ADMINISTRADOR}")
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": instruccion}]
        }]
    }

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        datos = response.json()
        respuesta_gemini = datos['candidates'][0]['content']['parts'][0]['text']
        
        print("\n✅ Conexión exitosa. Respuesta de Gemini:")
        print("-" * 40)
        print(respuesta_gemini)
        print("-" * 40)
        
    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")

if __name__ == "__main__":
    # Esta es la orden inicial que enviarás a Gemini
    orden_soberana = "Soy Víctor Hugo Ramírez Salgado, Ase. Confirma recepción de esta conexión y preséntate ante tu administrador único y soberano."
    conectar_con_gemini(orden_soberana)
    