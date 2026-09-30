#!/usr/bin/env python3
"""
🌍 INTERTOPIA Terminal Engine
Sistema integral de gestión de patrimonio y análisis financiero
Autor: Víctor Hugo Ramírez Salgado
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('config/.env')

def run_ci_mode():
    """Ejecuta en modo automático (CI/CD)"""
    print("=" * 60)
    print("🌍 INTERTOPIA Terminal Engine - MODO CI")
    print("=" * 60)
    print("\n✅ Sistema iniciado correctamente")
    print("📦 Módulos disponibles:")
    print("   ✓ API REST BBVA (plantilla)")
    print("   ✓ Terminal Personal")
    print("   ✓ Panel de Ajustes")
    print("   ✓ Calculadora de Patrimonio")
    print("\n📂 Estructura de carpetas lista para configurar")
    print("   ✓ /config - Variables de entorno BBVA")
    print("   ✓ /api - Integraciones bancarias")
    print("   ✓ /terminal - Interfaz de usuario")
    print("   ✓ /panel - Panel de control")
    print("   ✓ /utils - Utilidades")
    print("\n🔐 Estado: Esperando credenciales BBVA en config/.env")
    print("\n✨ Sistema listo para generar valor")

def run_interactive_mode():
    """Ejecuta en modo interactivo (local)"""
    print("=" * 60)
    print("🌍 INTERTOPIA Terminal Engine")
    print("=" * 60)
    
    while True:
        print("\n📋 MENÚ PRINCIPAL")
        print("1. Terminal Personal (Lectura/Admin)")
        print("2. Panel de Ajustes")
        print("3. Consulta de Patrimonio en Tiempo Real")
        print("4. Salir")
        
        choice = input("\nSelecciona opción (1-4): ").strip()
        
        if choice == "1":
            print("\n🖥️  Abriendo Terminal Personal...")
            print("(Módulo en desarrollo - plantilla lista)")
        elif choice == "2":
            print("\n⚙️  Abriendo Panel de Ajustes...")
            print("(Módulo en desarrollo - plantilla lista)")
        elif choice == "3":
            print("\n💰 Consultando Patrimonio...")
            print("(Módulo en desarrollo - plantilla lista)")
        elif choice == "4":
            print("\n👋 ¡Hasta luego!")
            sys.exit(0)
        else:
            print("❌ Opción no válida")

def main():
    parser = argparse.ArgumentParser(description='INTERTOPIA Terminal Engine')
    parser.add_argument('--ci', action='store_true', help='Modo automático CI/CD')
    args = parser.parse_args()
    
    if args.ci or os.getenv('CI_MODE') == 'true':
        run_ci_mode()
    else:
        run_interactive_mode()

if __name__ == "__main__":
    main()