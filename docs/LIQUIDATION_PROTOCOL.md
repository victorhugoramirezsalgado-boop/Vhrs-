# Protocolo de Liquidación de Activos

**SOLO PARA: Víctor Hugo Ramírez Salgado**
**Administrador Único de Intertopía / 1ntertopía**

---

## 🏗️ ARQUITECTURA DEL SISTEMA

Este sistema liquida **SOLO la cantidad de activos que el administrador solicite explícitamente**.

### Flujo de Operación:

1. **SOLICITUD** - Admin especifica cantidad exacta en USD
2. **APROBACIÓN** - Admin confirma con código 2FA de aprobación
3. **EJECUCIÓN** - Sistema vende activos y convierte a dinero físico
4. **TRANSFERENCIA** - Dinero físico se envía a cuenta especificada
5. **AUDITORÍA** - Todas las acciones se registran encriptadas

---

## 💰 TIPOS DE ACTIVOS SOPORTADOS

- **Acciones** (Stock)
- **Criptomonedas** (Crypto)
- **Fondos de Inversión** (Fund)
- **Bonos** (Bonds)
- **ETFs**
- **Otros activos negociables**

---

## 🏦 PROVEEDORES

- **BBVA** - Inversiones tradicionales, acciones
- **Capital.com** - Trading, criptomonedas

---

## 📋 ENDPOINTS DE LA API

### 1. CREAR SOLICITUD DE LIQUIDACIÓN
```bash
curl -X POST http://localhost:5001/api/private/liquidation/request \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -H "X-User-ID: victorhugoramirezsalgado" \
  -H "Content-Type: application/json" \
  -d '{
    "amount_usd": 5000.00,
    "asset_type": "stock",
    "source_provider": "bbva",
    "destination_account": "ES91_CUENTA_DESTINO",
    "instruction": "Liquidar acciones y convertir a USD"
  }'
```

**Respuesta:**
```json
{
  "status": "success",
  "request_id": "abc123def456...",
  "amount_usd": 5000.00,
  "message": "Solicitud de liquidación creada. Pendiente de aprobación."
}
```

### 2. APROBAR LIQUIDACIÓN
```bash
curl -X POST http://localhost:5001/api/private/liquidation/approve \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -H "X-User-ID: victorhugoramirezsalgado" \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "abc123def456...",
    "approval_code": "123456"
  }'
```

### 3. EJECUTAR LIQUIDACIÓN
```bash
curl -X POST http://localhost:5001/api/private/liquidation/execute \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -H "X-User-ID: victorhugoramirezsalgado" \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "abc123def456...",
    "execution_code": "654321"
  }'
```

### 4. VERIFICAR ESTADO
```bash
curl -X GET http://localhost:5001/api/private/liquidation/status/abc123def456... \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -H "X-User-ID: victorhugoramirezsalgado"
```

### 5. OBTENER AUDITORÍA
```bash
curl -X GET http://localhost:5001/api/private/liquidation/audit \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -H "X-User-ID: victorhugoramirezsalgado"
```

---

## 🔐 SEGURIDAD IMPLEMENTADA

✅ **Encriptación AES-256** de todos los datos
✅ **2FA Dual** - Códigos diferentes para aprobación y ejecución
✅ **Solo Admin** - Solo victorhugoramirezsalgado puede acceder
✅ **Cantidad Exacta** - Se liquida PRECISAMENTE lo solicitado
✅ **Log de Auditoría** - Registro inmutable y encriptado
✅ **Verificación de Permisos** - En cada operación
✅ **Tokens de Sesión** - Verificación de identidad
✅ **Localhost-Only** - En desarrollo
✅ **HTTPS Obligatorio** - En producción
✅ **Nada Público** - Datos privados nunca en GitHub

---

## ⚡ FLUJO COMPLETO DE LIQUIDACIÓN

### Ejemplo:

1. **Admin solicita liquidación**
   ```
   "Liquido 10,000 USD en acciones desde BBVA"
   → Sistema genera request_id: abc123xyz789
   ```

2. **Admin aprueba con 2FA**
   ```
   "Confirmo solicitud abc123xyz789"
   → Ingresa código 2FA: 123456
   → Sistema valida
   ```

3. **Admin ejecuta con 2FA diferente**
   ```
   "Ejecutar liquidación abc123xyz789"
   → Ingresa código 2FA: 654321
   → Sistema vende exactamente 10,000 USD
   → Convierte a dinero físico
   → Transfiere a cuenta destino
   ```

4. **Sistema confirma**
   ```
   "Liquidación completada"
   "USD 10,000 enviados a tu cuenta"
   "Confirmación ID: txn_xyz789..."
   ```

---

## 📊 VARIABLES DE ENTORNO REQUERIDAS

```bash
# SEGURIDAD
ENCRYPTION_KEY=base64_encryption_key
ADMIN_SESSION_TOKEN=session_token_único
ADMIN_APPROVAL_CODE=approval_2fa_code
ADMIN_EXECUTION_CODE=execution_2fa_code
FLASK_SECRET_KEY=flask_secret_key

# BBVA
BBVA_API_KEY=bbva_api_key
BBVA_USER_ID=victorhugoramirezsalgado
ADMIN_BBVA_ACCOUNT=cuenta_destino_bbva

# CAPITAL.COM
CAPITAL_API_KEY=capital_api_key
CAPITAL_USER_ID=victorhugoramirezsalgado
ADMIN_CAPITAL_ACCOUNT=cuenta_destino_capital
```

---

## ⚠️ REGLAS CRÍTICAS

✓ **SOLO SE LIQUIDA LO QUE EL ADMIN SOLICITA EXPLÍCITAMENTE**
✓ La cantidad es EXACTA, no aproximada
✓ Cada operación requiere aprobación Y ejecución separadas
✓ El dinero físico se envía SOLO a la cuenta especificada
✓ No hay liquidaciones automáticas
✓ Todas las acciones quedan registradas
✓ Los datos nunca se exponen públicamente
✓ Cumplimiento total de AML/KYC

---

## 🛡️ PROTECCIONES ADICIONALES

- Validación de cantidad (debe ser positiva)
- Verificación de proveedor soportado
- Verificación de cuenta destino
- Timeouts en solicitudes
- Rate limiting
- Detección de patrones sospechosos
- Alertas automáticas

---

**Versión:** 1.0  
**Fecha:** 2026-06-14  
**Administrador Único:** Víctor Hugo Ramírez Salgado  
**Entidad:** Intertopía / 1ntertopía