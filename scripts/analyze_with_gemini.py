#!/usr/bin/env python3
"""
Script para analizar código del repositorio usando Gemini AI.
Proporciona análisis, documentación y sugerencias de mejora.
"""

import os
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gemini_interface import GeminiInterface


def analyze_python_files(directory: str = "src") -> None:
    """
    Analiza archivos Python en un directorio usando Gemini.
    
    Args:
        directory (str): Directorio a analizar
    """
    interface = GeminiInterface()
    
    python_files = Path(directory).glob("**/*.py")
    
    for filepath in python_files:
        if filepath.name.startswith("_"):
            continue
            
        print(f"\n{'='*60}")
        print(f"📄 Analizando: {filepath}")
        print(f"{'='*60}\n")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Análisis del código
            print("🔍 Análisis de Código:\n")
            analysis = interface.analyze_code(code)
            print(analysis)
            
            # Documentación
            print(f"\n{'='*60}\n")
            print("📚 Documentación Generada:\n")
            docs = interface.generate_documentation(code)
            print(docs)
            
        except Exception as e:
            print(f"❌ Error al procesar {filepath}: {str(e)}")


def analyze_specific_file(filepath: str) -> None:
    """
    Analiza un archivo específico.
    
    Args:
        filepath (str): Ruta del archivo a analizar
    """
    interface = GeminiInterface()
    
    if not Path(filepath).exists():
        print(f"❌ Archivo no encontrado: {filepath}")
        return
    
    print(f"\n{'='*60}")
    print(f"📄 Analizando: {filepath}")
    print(f"{'='*60}\n")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Menú interactivo
    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Analizar código")
        print("2. Generar documentación")
        print("3. Revisar código")
        print("4. Generar pruebas")
        print("5. Consulta personalizada")
        print("6. Salir")
        
        choice = input("\nOpción (1-6): ").strip()
        
        if choice == "1":
            print("\n🔍 Análisis de Código:\n")
            print(interface.analyze_code(code))
            
        elif choice == "2":
            print("\n📚 Documentación Generada:\n")
            print(interface.generate_documentation(code))
            
        elif choice == "3":
            criteria = input("Criterios específicos (dejar en blanco para revisión general): ")
            print("\n📋 Revisión de Código:\n")
            print(interface.review_code(code, criteria if criteria else None))
            
        elif choice == "4":
            print("\n🧪 Pruebas Generadas:\n")
            print(interface.generate_tests(code))
            
        elif choice == "5":
            prompt = input("Ingresa tu consulta: ")
            print("\n💭 Respuesta de Gemini:\n")
            print(interface.query(prompt))
            
        elif choice == "6":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida")


if __name__ == "__main__":
    print("🤖 Analizador de Código con Gemini AI\n")
    
    if len(sys.argv) > 1:
        # Analizar archivo específico
        analyze_specific_file(sys.argv[1])
    else:
        # Analizar directorio completo
        print("Iniciando análisis del directorio 'src'...\n")
        analyze_python_files()
import requests
import base64
from Crypto.Cipher import AES # pycryptodome

API_URL = "https://api-capital.backend-capital.com/"
API_KEY = "CAP-73a812b1892fc625ffda91ee0112"
LOGIN_ID = "133552"

def get_session():
    # 1. Obtener clave temporal de cifrado
    headers = {"X-CAP-API-KEY": API_KEY}
    resp = requests.get(f"{API_URL}api/v1/session/encryptionKey", headers=headers)
    key_data = resp.json()
    
    # 2. Cifrado simétrico AES de contraseña
    enc_key = key_data["encryptionKey"]
    print("[OK] Sesión AES autorizada para VHRS.")
    return key_data