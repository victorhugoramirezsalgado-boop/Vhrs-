#!/usr/bin/env python3
"""
🌍 INTERTOPIA Terminal Engine
Sistema integral de gestión de patrimonio y análisis financiero
Autor: Víctor Hugo Ramírez Salgado
"""

import os
import sys
from dotenv import load_dotenv
from api.bbva_api import BBVAAPIClient
from terminal.personal_terminal import PersonalTerminal
from panel.settings_panel import SettingsPanel
from utils.wealth_calculator import WealthCalculator

# Cargar variables de entorno
load_dotenv('config/.env')

def main():
    """Ejecuta el motor de terminal de INTERTOPIA"""
    print("=" * 60)
    print("🌍 INTERTOPIA Terminal Engine")
    print("=" * 60)
    
    # Inicializar componentes
    bbva_client = BBVAAPIClient()
    terminal = PersonalTerminal(bbva_client)
    settings_panel = SettingsPanel()
    wealth_calc = WealthCalculator()
    
    # Menú principal
    while True:
        print("\n📋 MENÚ PRINCIPAL")
        print("1. Terminal Personal (Lectura/Admin)")
        print("2. Panel de Ajustes")
        print("3. Consulta de Patrimonio en Tiempo Real")
        print("4. Salir")
        
        choice = input("\nSelecciona opción (1-4): ").strip()
        
        if choice == "1":
            terminal.run()
        elif choice == "2":
            settings_panel.run()
        elif choice == "3":
            wealth = wealth_calc.get_realtime_wealth()
            print(f"\n💰 Patrimonio Total: ${wealth['total']:,.2f}")
            print(f"📊 Detalles: {wealth['details']}")
        elif choice == "4":
            print("\n👋 ¡Hasta luego!")
            sys.exit(0)
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    main()
