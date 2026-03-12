# 🔄 APIs Actualizadas con Soft Delete

## **✅ Problema Solucionado**

El error `IntegrityError` ocurría porque intentabas eliminar una pantalla que tenía dependencias en `RolPantallas`. 

**Solución implementada:** Soft Delete (Eliminación Lógica)

---

## **🔧 Comportamiento del DELETE**

### **DELETE /api/pantallas/{id}/**

Ahora funciona de forma inteligente:

#### **1. Si la pantalla TIENE dependencias:**
```json
{
    "message": "Pantalla desactivada correctamente",
    "pantalla_id": 11,
    "nombre": "Clientes",
    "activo": false,
    "dependencias": 3,
    "accion": "soft_delete"
}
```
- **No elimina físicamente**
- **Marca `activo = false`**
- **Mantiene integridad referencial**

#### **2. Si la pantalla NO tiene dependencias:**
```json
{
    "message": "Pantalla eliminada permanentemente",
    "pantalla_id": 11,
    "nombre": "Clientes",
    "accion": "hard_delete"
}
```
- **Elimina físicamente**
- **Solo si no hay registros en RolPantallas**

---

## **🆕 Nuevas APIs Añadidas**

### **1. Reactivar Pantalla**
```http
POST /api/pantallas/{id}/reactivar/
Authorization: Bearer {token}
```

**Respuesta:**
```json
{
    "message": "Pantalla reactivada correctamente",
    "pantalla_id": 11,
    "nombre": "Clientes",
    "activo": true
}
```

### **2. Listar Pantallas Desactivadas**
```http
GET /api/pantallas/eliminadas/
Authorization: Bearer {token}
```

**Respuesta:**
```json
{
    "pantallas_eliminadas": [
        {
            "pantallaid": 11,
            "nombre": "Clientes",
            "codigo": "clientes_list",
            "descripcion": "Listado de clientes",
            "modulo": "Gestión",
            "fecha_creacion": "2024-01-15T10:30:00Z"
        }
    ],
    "total": 1
}
```

---

## **📋 Lista Completa de APIs de Pantallas**

### **CRUD Básico:**
```http
GET    /api/pantallas/                    # Listar todas
GET    /api/pantallas/?activo=true        # Solo activas
GET    /api/pantallas/?activo=false       # Solo inactivas
GET    /api/pantallas/?modulo=Gestión   # Por módulo
POST   /api/pantallas/                    # Crear nueva
GET    /api/pantallas/{id}/               # Obtener específica
PUT    /api/pantallas/{id}/               # Actualizar
DELETE /api/pantallas/{id}/               # Eliminar (Soft Delete)
```

### **Acciones Especiales:**
```http
POST   /api/pantallas/{id}/reactivar/    # Reactivar pantalla
GET    /api/pantallas/eliminadas/          # Listar desactivadas
```

---

## **🧪 Pruebas en Postman**

### **1. Eliminar Pantalla (con dependencias):**
1. **DELETE** `http://127.0.0.1:8000/api/pantallas/11/`
2. **Authorization:** `Bearer Token`
3. **Resultado:** `200 OK` con `"accion": "soft_delete"`

### **2. Ver Pantallas Desactivadas:**
1. **GET** `http://127.0.0.1:8000/api/pantallas/eliminadas/`
2. **Authorization:** `Bearer Token`
3. **Resultado:** Lista de pantallas inactivas

### **3. Reactivar Pantalla:**
1. **POST** `http://127.0.0.1:8000/api/pantallas/11/reactivar/`
2. **Authorization:** `Bearer Token`
3. **Resultado:** `200 OK` con `"activo": true`

### **4. Ver Solo Activas:**
1. **GET** `http://127.0.0.1:8000/api/pantallas/?activo=true`
2. **Authorization:** `Bearer Token`
3. **Resultado:** Solo pantallas activas

---

## **🎯 Beneficios del Soft Delete**

### **✅ Ventajas:**
1. **Integridad Referencial:** No rompe relaciones
2. **Recuperación:** Puede reactivarse fácilmente
3. **Auditoría:** Mantiene histórico
4. **Rendimiento:** Más rápido que eliminar físicamente
5. **Seguridad:** Los datos no se pierden

### **📊 Estadísticas Posibles:**
- Pantallas activas vs inactivas
- Tiempo de desactivación
- Frecuencia de reactivación
- Análisis de uso

---

## **🔄 Flujo Completo**

### **Escenario 1: Desactivar con dependencias**
```
DELETE /api/pantallas/11/ 
→ Soft Delete (activo=false)
→ Mantiene relaciones en RolPantallas
→ No se puede acceder desde frontend
```

### **Escenario 2: Reactivar**
```
POST /api/pantallas/11/reactivar/
→ activo=true
→ Recupera acceso
→ Relaciones intactas
```

### **Escenario 3: Eliminar sin dependencias**
```
DELETE /api/pantallas/99/
→ Hard Delete
→ Elimina físicamente
→ Solo si no hay relaciones
```

---

## **🛠️ Para Frontend**

### **Lógica de Eliminación:**
```javascript
const deletePantalla = async (id) => {
  const response = await fetch(`/api/pantallas/${id}/`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  const result = await response.json();
  
  if (result.accion === 'soft_delete') {
    // Mostrar: "Pantalla desactivada"
    // Ocultar de lista principal
    // Opción de reactivar
  } else if (result.accion === 'hard_delete') {
    // Mostrar: "Pantalla eliminada permanentemente"
    // Remover completamente
  }
};
```

### **Botón de Reactivar:**
```javascript
const reactivarPantalla = async (id) => {
  const response = await fetch(`/api/pantallas/${id}/reactivar/`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  // Actualizar UI: mostrar como activa
};
```

---

## **✅ Resumen**

- **❌ Error anterior:** `IntegrityError` al eliminar
- **✅ Solución:** Soft Delete inteligente
- **🆕 Funciones:** Reactivar y listar eliminadas
- **🔒 Seguridad:** Mantiene integridad de datos
- **📊 Control:** Total visibilidad del estado

**¡Ya puedes eliminar pantallas sin errores!** El sistema decide automáticamente si hacer soft o hard delete según las dependencias.
