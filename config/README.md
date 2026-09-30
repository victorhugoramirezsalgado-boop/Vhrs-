# 🏦 Configuración BBVA

## Instrucciones de Configuración

1. **Copia el template:**
   ```bash
   cp .env.template .env
   ```

2. **Completa las credenciales BBVA:**
   - Obtén `BBVA_CLIENT_ID` y `BBVA_CLIENT_SECRET` desde el portal de desarrolladores de BBVA
   - Agrega tu número de cuenta y routing number

3. **Variables adicionales:**
   - `ALPACA_API_KEY_ID` y `ALPACA_API_SECRET_KEY` para trading
   - `GEMINI_API_KEY` para análisis inteligente
   - `GITHUB_TOKEN` para operaciones en GitHub

4. **Seguridad:**
   - ⚠️ **Nunca** comitees `.env` con credenciales reales
   - Usa GitHub Secrets para CI/CD
   - `.env` está en `.gitignore`

## Estructura de Credenciales

```
config/
├── .env.template    ← Plantilla (segura)
├── .env             ← Credenciales (ignorada en git)
└── README.md        ← Esta documentación
```

## Próximos Pasos

- [ ] Registrarse en portal BBVA para desarrolladores
- [ ] Obtener credenciales API
- [ ] Configurar .env localmente
- [ ] Vincular a módulos de API REST
- [ ] Implementar autenticación segura

**Status:** 🟡 Plantilla lista, esperando configuración