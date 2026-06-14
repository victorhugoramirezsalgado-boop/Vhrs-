# Sistema Privado y Seguro de Transferencias Financieras

**SOLO PARA: Víctor Hugo Ramírez Salgado**

---

## 📋 Documentación de Uso

### 1. Configuración Inicial

```bash
# Copiar archivo de ejemplo
cp .env.example.secure .env

# Instalar dependencias
pip install -r requirements-secure-transfer.txt
pip install -r requirements-gemini.txt
pip install -r requirements-financial.txt
```

### 2. Variables de Entorno Requeridas

**SEGURIDAD:**
- `ENCRYPTION_KEY`: Clave AES-256
- `ADMIN_SESSION_TOKEN`: Token único de sesión
- `ADMIN_CONFIRMATION_CODE`: Código 2FA
- `FLASK_SECRET_KEY`: Clave secreta de Flask

**BBVA:**
- `BBVA_API_KEY`: Clave API de BBVA
- `BBVA_USER_ID`: ID de usuario en BBVA
- `ADMIN_BBVA_ACCOUNT`: Número de cuenta IBAN

**CAPITAL.COM:**
- `CAPITAL_API_KEY`: Clave API de Capital.com
- `CAPITAL_USER_ID`: ID de usuario en Capital.com
- `ADMIN_CAPITAL_ACCOUNT`: ID de cuenta

### 3. Generar Clave de Encriptación

```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 4. USO DE LA API PRIVADA

#### A) INICIAR SERVIDOR
```bash
python src/transfer_webhook.py
```

#### B) CREAR SOLICITUD DE TRANSFERENCIA
```bash
curl -X POST http://localhost:5000/api/private/transfer/initiate \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -H "X-User-ID: victorhugoramirezsalgado" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1000.00,
    "provider": "bbva",
    "reason": "Reinversión de ganancias"
  }'
```

#### C) CONFIRMAR Y EJECUTAR TRANSFERENCIA
```bash
curl -X POST http://localhost:5000/api/private/transfer/confirm \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -H "X-User-ID: victorhugoramirezsalgado" \
  -H "Content-Type: application/json" \
  -d '{
    "transfer_id": "abc123def456...",
    "admin_code": "123456"
  }'
```

#### D) VERIFICAR ESTADO
```bash
curl -X GET http://localhost:5000/api/private/transfer/status/abc123def456... \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -H "X-User-ID: victorhugoramirezsalgado"
```

#### E) OBTENER LOG DE AUDITORÍA
```bash
curl -X GET http://localhost:5000/api/private/audit/log \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -H "X-User-ID: victorhugoramirezsalgado"
```

---

## 🔐 Características de Seguridad

✅ **Encriptación AES-256** de todos los datos sensibles
✅ **Autenticación de 2FA** obligatoria
✅ **Solo admin** puede acceder (victorhugoramirezsalgado)
✅ **Tokens de sesión** para verificación de identidad
✅ **Log de auditoría** encriptado e inmutable
✅ **HTTPS/SSL** obligatorio en producción
✅ **Localhost-only** para desarrollo
✅ **Protección contra timing attacks**
✅ **Verificación de permisos** en cada operación
✅ **Nada visible públicamente** en GitHub

---

## ⚠️ Instrucciones Críticas de Seguridad

- ⚠️  NUNCA compartir el archivo `.env`
- ⚠️  NUNCA exponer variables de entorno en logs
- ⚠️  NUNCA usar `debug=True` en producción
- ⚠️  NUNCA almacenar credenciales en código
- ⚠️  SIEMPRE usar HTTPS en producción
- ⚠️  SIEMPRE cambiar claves por defecto
- ⚠️  SIEMPRE revisar logs regularmente
- ⚠️  SIEMPRE mantener `.gitignore` actualizado

---

## 📝 Flujo de Autorización

1. **Admin genera solicitud** → Se genera ID único y se encriptan datos
2. **Sistema notifica privadamente** → Solo visible para Víctor Hugo
3. **Admin confirma con 2FA** → Validación de seguridad adicional
4. **Sistema ejecuta transferencia** → Se comunica con BBVA o Capital.com
5. **Se registra en auditoría** → Datos completamente encriptados

---

## 📊 Cumplimiento Legal

Este sistema ha sido diseñado con:
- ✅ Cumplimiento de regulaciones AML/KYC
- ✅ Auditoría completa de transacciones
- ✅ Encriptación en tránsito y en reposo
- ✅ Autenticación de dos factores
- ✅ Registro inmutable de eventos

**IMPORTANTE:** Verificar cumplimiento con autoridades locales antes de usar en producción.

---

**Documentación actualizada:** 2026-06-14
**Versión:** 1.0 - Sistema Privado Seguro
**Administrador Único:** Víctor Hugo Ramírez Salgado