# 🌍 INTERTOPIA Terminal Engine

Sistema integral de gestión de patrimonio y análisis financiero para Víctor Hugo Ramírez Salgado.

## 🎯 Características

✅ **API REST BBVA** - Plantilla de integración bancaria  
✅ **Terminal Personal** - Interface admin/lectura  
✅ **Panel de Ajustes** - Modificar activos y tasas  
✅ **Calculadora de Patrimonio** - Consulta en tiempo real  
✅ **Estructura modular** - Listo para expansion  

## 📁 Estructura del Proyecto

```
VHRS/
├── main.py                    # Motor principal
├── config/
│   ├── .env.template         # Plantilla de credenciales
│   ├── .env                  # Credenciales locales (git-ignored)
│   └── README.md             # Documentación de config
├── api/
│   ├── __init__.py
│   └── bbva_template.py      # Plantilla API BBVA
├── terminal/
│   ├── __init__.py
│   └── personal_terminal.py  # Terminal personal
├── panel/
│   ├── __init__.py
│   └── settings_panel.py     # Panel de ajustes
├── utils/
│   ├── __init__.py
│   └── wealth_calculator.py  # Calculadora patrimonio
└── .github/workflows/
    └── publish.yml           # CI/CD automático
```

## 🚀 Modo de Uso

### Modo Interactivo (Local)
```bash
pip install -r requirements.txt
python main.py
```

### Modo CI/CD (Automático)
```bash
python main.py --ci
```

## 🔧 Configuración

1. **Copia el template:**
   ```bash
   cp config/.env.template config/.env
   ```

2. **Completa credenciales BBVA:**
   - Obtén acceso al portal de desarrolladores de BBVA
   - Agrega CLIENT_ID, CLIENT_SECRET y datos de cuenta

3. **Variables de entorno:**
   ```
   BBVA_CLIENT_ID=xxx
   BBVA_CLIENT_SECRET=xxx
   BBVA_ACCOUNT_NUMBER=xxx
   ALPACA_API_KEY_ID=xxx
   ALPACA_API_SECRET_KEY=xxx
   GEMINI_API_KEY=xxx
   GITHUB_TOKEN=xxx
   ```

## 📦 Módulos

### 🏦 API BBVA (`api/bbva_template.py`)
- Plantilla de cliente API
- Autenticación OAuth2 (pendiente)
- Consulta de cuentas y saldo
- Transacciones (seguridad en desarrollo)

### 💻 Terminal Personal (`terminal/personal_terminal.py`)
- Interface para Víctor Hugo
- Permisos: Admin + Lectura
- Visualización de portafolio
- Historial de operaciones

### ⚙️ Panel de Ajustes (`panel/settings_panel.py`)
- Modificar activos
- Ajustar tasas de interés
- Configuración del sistema

### 💰 Calculadora (`utils/wealth_calculator.py`)
- Patrimonio en tiempo real
- Activos y pasivos
- Cálculo de patrimonio neto

## 🔐 Seguridad

- ⚠️ `.env` está en `.gitignore` (nunca commitear credenciales)
- 🔒 Usa GitHub Secrets para CI/CD
- 🚫 Operaciones bancarias requieren doble autenticación
- 🛡️ Plantilla sin operaciones reales hasta configuración completa

## 📊 Estado del Proyecto

| Módulo | Status | Próximo Paso |
|--------|--------|----------|
| 🏦 API BBVA | 🟡 Plantilla | Implementar OAuth2 |
| 💻 Terminal | 🟡 Plantilla | Conectar con API |
| ⚙️ Panel | 🟡 Plantilla | UI/UX |
| 💰 Calculadora | 🟡 Plantilla | Integrar APIs |

## 🔄 Workflow CI/CD

✅ Automático en cada `push` a `main`  
✅ Python 3.10  
✅ Instala dependencias  
✅ Ejecuta validación  
✅ Genera reportes  

## 📝 Próximos Pasos

- [ ] Configurar credenciales BBVA
- [ ] Implementar autenticación OAuth2
- [ ] Conectar APIs reales
- [ ] Crear interfaz web/CLI avanzada
- [ ] Tests unitarios
- [ ] Documentación API
- [ ] Deploy en producción

## 👨‍💻 Autor

**Víctor Hugo Ramírez Salgado**  
INTERTOPIA Project  
2026

---

**Status:** 🟢 Operacional - Esperando configuración BBVA