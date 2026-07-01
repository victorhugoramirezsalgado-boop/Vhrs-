# Dashboard Híbrido - Documentación Completa

**SOLO PARA: Víctor Hugo Ramírez Salgado**
**Administrador Único de Intertopía / 1ntertopía**

---

## 🎯 DESCRIPCIÓN GENERAL

El **Dashboard Híbrido** combina:
- ✅ Backend REST API (Puerto 5002)
- ✅ Frontend Web UI (HTML/CSS/JavaScript)
- ✅ Autenticación obligatoria (2FA)
- ✅ Datos en tiempo real
- ✅ Encriptación completa

---

## 📊 COMPONENTES DEL DASHBOARD

### **1. Vista General (Cards)**
- Transferencias Pendientes
- Transferencias Aprobadas
- Liquidaciones Pendientes
- Liquidaciones Ejecutadas

### **2. Estadísticas**
- Total Transferido (USD)
- Total Liquidado (USD)
- Total de Transacciones

### **3. Tablas Activas**
- Transferencias Activas
- Liquidaciones Activas
- Actividad Reciente (últimas 10)

### **4. Acciones**
- Actualizar Dashboard (Refresh)
- Exportar Datos (JSON)

---

## 🚀 INICIO RÁPIDO

### **1. Instalar Dependencias**
```bash
pip install -r requirements.txt
pip install flask
```

### **2. Configurar Variables de Entorno**
```bash
cp .env.example.secure .env
# Editar .env con tus valores
```

### **3. Iniciar Servidor Backend**
```bash
python src/dashboard_api.py
# ✓ API disponible en: http://localhost:5002
```

### **4. Abrir Dashboard en Navegador**

**Opción A: Archivo local**
```bash
open web/dashboard.html
```

**Opción B: Servidor HTTP simple**
```bash
cd web
python -m http.server 8000
# Abrir: http://localhost:8000/dashboard.html
```

---

## 🔗 ENDPOINTS DE LA API

Todos requieren headers:
```
Authorization: Bearer SESSION_TOKEN
X-User-ID: victorhugoramirezsalgado
Content-Type: application/json
```

### **1. GET /api/dashboard/overview**
Vista general de transacciones y liquidaciones

```bash
curl -X GET http://localhost:5002/api/dashboard/overview \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -H "X-User-ID: victorhugoramirezsalgado"
```

**Respuesta:**
```json
{
  "status": "success",
  "summary": {
    "total_pending_transfers": 2,
    "total_approved_transfers": 1,
    "total_pending_liquidations": 3,
    "total_executed_liquidations": 5
  }
}
```

### **2. GET /api/dashboard/transfers**
Lista de transferencias activas

```bash
curl -X GET http://localhost:5002/api/dashboard/transfers \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -H "X-User-ID: victorhugoramirezsalgado"
```

### **3. GET /api/dashboard/liquidations**
Lista de liquidaciones activas

```bash
curl -X GET http://localhost:5002/api/dashboard/liquidations \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -H "X-User-ID: victorhugoramirezsalgado"
```

### **4. GET /api/dashboard/activity**
Historial de actividad reciente

```bash
curl -X GET http://localhost:5002/api/dashboard/activity \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -H "X-User-ID: victorhugoramirezsalgado"
```

### **5. GET /api/dashboard/stats**
Estadísticas generales

```bash
curl -X GET http://localhost:5002/api/dashboard/stats \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -H "X-User-ID: victorhugoramirezsalgado"
```

### **6. GET /api/dashboard/health**
Estado del sistema

```bash
curl -X GET http://localhost:5002/api/dashboard/health \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -H "X-User-ID: victorhugoramirezsalgado"
```

### **7. GET /api/dashboard/export**
Exportar datos completos (JSON)

```bash
curl -X GET http://localhost:5002/api/dashboard/export \
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \
  -H "X-User-ID: victorhugoramirezsalgado" > export.json
```

---

## 🔐 AUTENTICACIÓN EN WEB UI

### **Opción 1: LocalStorage**
```javascript
localStorage.setItem('session_token', 'YOUR_SESSION_TOKEN');
```

### **Opción 2: Variables en HTML**
Editar en `web/dashboard.html` línea 206:
```javascript
const SESSION_TOKEN = 'YOUR_ACTUAL_TOKEN';
```

### **Opción 3: Login Form**
```html
<input id="token-input" type="password" placeholder="Session Token">
<button onclick="setToken()">Conectar</button>

<script>
function setToken() {
  const token = document.getElementById('token-input').value;
  localStorage.setItem('session_token', token);
  location.reload();
}
</script>
```

---

## 📱 CARACTERÍSTICAS WEB

✅ Diseño responsivo (Desktop y Mobile)
✅ Tema moderno con colores profesionales
✅ Actualización automática cada 30 segundos
✅ Tablas interactivas con hover effects
✅ Badges de estado (Pending, Approved, Executed)
✅ Cálculos de estadísticas en tiempo real
✅ Exportación de datos en JSON
✅ Interfaz intuitiva y fácil de usar

---

## 🔄 FLUJO DE DATOS

```
Web UI (HTML/JavaScript)
        ↓
  Fetch API
        ↓
Backend API (Flask)
        ↓
  Autenticación
        ↓
Sistema de Transferencias
Sistema de Liquidaciones
        ↓
  JSON Response
        ↓
Renderizado en Web UI
```

---

## ⚙️ CONFIGURACIÓN AVANZADA

### **1. Cambiar Puerto del Backend**
Editar en `src/dashboard_api.py` (última línea):
```python
app.run(port=5003)  # Cambiar a otro puerto
```

### **2. Personalizar Colores Web**
Editar en `web/dashboard.html` dentro de `<style>`:
```css
--primary-color: #1e3c72;
--secondary-color: #2a5298;
```

### **3. Agregar Nuevos Campos**
Agregar endpoint en `src/dashboard_api.py`:
```python
@app.route('/api/dashboard/custom', methods=['GET'])
@require_admin_auth
def get_custom(user_id, session_token):
    return jsonify({"data": "value"}), 200
```

Agregar en `web/dashboard.html`:
```javascript
async function loadCustom() {
    const data = await makeRequest('/custom');
    // Procesar datos
}
```

### **4. Cambiar Frecuencia de Actualización**
Editar en `web/dashboard.html` (última línea):
```javascript
setInterval(refreshDashboard, 60000);  // Cambiar milisegundos
```

---

## 🛡️ SEGURIDAD

✅ Autenticación obligatoria en cada endpoint
✅ Verificación de usuario (solo admin)
✅ Tokens de sesión con validación
✅ CORS habilitado solo para localhost
✅ HTTPS obligatorio en producción
✅ Datos sensibles encriptados
✅ Session tokens con expiración

---

## 📋 TROUBLESHOOTING

### **Error: "No autorizado"**
- Verificar `SESSION_TOKEN` en localStorage
- Verificar `X-User-ID` sea: `victorhugoramirezsalgado`
- Verificar que el token no haya expirado

### **Error: CORS "No Access-Control-Allow-Origin"**
- Usar dashboard desde `localhost:8000`
- O agregar proxy inverso (Nginx/Apache)
- No usar directamente desde archivo local

### **Datos no actualizan**
- Verificar que `dashboard_api.py` esté corriendo
- Abrir consola (F12) para ver errores
- Verificar conexión a `http://localhost:5002`
- Verificar firewall no bloquee puerto 5002

### **Botones no funcionan**
- Verificar token en localStorage
- Abrir Developer Console (F12)
- Revisar Network tab para ver requests
- Verificar permisos de usuario

---

## 🚀 DEPLOYMENT EN PRODUCCIÓN

### **1. Usar Gunicorn**
```bash
pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:5002 src.dashboard_api:app
```

### **2. Configurar Nginx**
```nginx
server {
    listen 443 ssl;
    server_name dashboard.intertopia.local;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location /api {
        proxy_pass http://127.0.0.1:5002;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location / {
        root /var/www/dashboard;
        try_files $uri /dashboard.html;
    }
}
```

### **3. Implementar Seguridad**
- Rate limiting
- Logging y monitoring
- Backups automáticos
- WAF (Web Application Firewall)

---

## 📖 PRÓXIMOS PASOS

1. ✅ Configurar SESSION_TOKEN
2. ✅ Iniciar backend (dashboard_api.py)
3. ✅ Abrir web UI en navegador
4. ✅ Explorar vista general de transacciones
5. ✅ Revisar liquidaciones activas
6. ✅ Exportar datos para análisis
7. ✅ Configurar alertas personalizadas
8. ✅ Integrar con Grafana para métricas avanzadas

---

## 📞 INFORMACIÓN DE CONTACTO

**Administrador:** Víctor Hugo Ramírez Salgado  
**Entidad:** Intertopía / 1ntertopía  
**Email:** victorhugoramirezsalgado@gmail.com  
**Versión:** 1.0  
**Fecha:** 2026-07-01  

---

**Dashboard Híbrido - Sistema Privado y Seguro para Intertopía**

🔐 Encriptación Completa | 🔑 Autenticación 2FA | 📊 Datos en Tiempo Real | 🛡️ Seguridad Institucional