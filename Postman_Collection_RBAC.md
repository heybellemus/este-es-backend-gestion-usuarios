# Colección Postman - Control de Acceso Basado en Roles (RBAC)

## Configuración Inicial

### Variables de Entorno
- `base_url`: `http://localhost:8000` (o tu URL de servidor)
- `access_token`: Token JWT obtenido del login
- `refresh_token`: Token de refresco JWT

---

## 1. Autenticación

### 1.1 Login de Usuario
```http
POST {{base_url}}/login/
Content-Type: application/json

{
    "email": "admin@ejemplo.com",
    "password": "password123"
}
```

**Respuesta Esperada:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "usuario": {
        "usuarioid": 1,
        "nombre": "Administrador",
        "apellido": "Sistema",
        "email": "admin@ejemplo.com",
        "nombreusuario": "admin",
        "rolid": 1,
        "departamentoid": 1
    }
}
```

---

## 2. Gestión de Pantallas (Solo Administradores)

### 2.1 Listar Todas las Pantallas
```http
GET {{base_url}}/pantallas-list/
Authorization: Bearer {{access_token}}
```

### 2.2 Ver Pantallas de un Rol Específico
```http
GET {{base_url}}/rol-pantallas/2/
Authorization: Bearer {{access_token}}
```

### 2.3 Ver Todas las Asignaciones de Roles-Pantallas
```http
GET {{base_url}}/todos-roles-pantallas/
Authorization: Bearer {{access_token}}
```

---

## 3. Asignación de Permisos (Solo Administradores)

### 3.1 Asignar Pantalla a Rol
```http
POST {{base_url}}/asignar-pantalla-rol/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "rol_id": 2,
    "pantalla_id": 1,
    "acceso": true
}
```

### 3.2 Asignar Múltiples Pantallas a un Rol
```http
POST {{base_url}}/asignar-multiples-pantallas-rol/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "rol_id": 3,
    "pantallas": [
        {"pantalla_id": 1, "acceso": true},
        {"pantalla_id": 2, "acceso": true},
        {"pantalla_id": 3, "acceso": false},
        {"pantalla_id": 4, "acceso": true}
    ]
}
```

---

## 4. Verificación de Acceso

### 4.1 Obtener Pantallas del Usuario Autenticado
```http
GET {{base_url}}/pantallas-usuario/
Authorization: Bearer {{access_token}}
```

**Respuesta Esperada:**
```json
{
    "pantallas": [
        {
            "pantallaid": 1,
            "nombre": "Dashboard",
            "codigo": "dashboard",
            "descripcion": "Pantalla principal del sistema",
            "ruta": "/dashboard",
            "modulo": "Principal"
        },
        {
            "pantallaid": 3,
            "nombre": "Clientes",
            "codigo": "clientes_list",
            "descripcion": "Listado de clientes",
            "ruta": "/clientes",
            "modulo": "Gestión"
        }
    ],
    "total": 2
}
```

### 4.2 Verificar Acceso a Pantallas Específicas
```http
POST {{base_url}}/verificar-acceso-pantalla/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "codigos": ["dashboard", "clientes_list", "usuarios_list"]
}
```

**Alternativa (una sola pantalla):**
```http
POST {{base_url}}/verificar-acceso-pantalla/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "codigo": "clientes_list"
}
```

**Respuesta Esperada:**
```json
{
    "accesos": {
        "dashboard": true,
        "clientes_list": true,
        "usuarios_list": false
    },
    "usuario": "admin"
}
```

---

## 5. ViewSets CRUD

### 5.1 Pantallas
```http
# Listar todas
GET {{base_url}}/api/pantallas/
Authorization: Bearer {{access_token}}

# Obtener pantalla específica
GET {{base_url}}/api/pantallas/1/
Authorization: Bearer {{access_token}}

# Crear nueva pantalla
POST {{base_url}}/api/pantallas/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "nombre": "Nueva Pantalla",
    "codigo": "nueva_pantalla",
    "descripcion": "Descripción de la nueva pantalla",
    "ruta": "/nueva",
    "modulo": "Gestión",
    "activo": true
}

# Actualizar pantalla
PUT {{base_url}}/api/pantallas/1/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "nombre": "Pantalla Actualizada",
    "codigo": "pantalla_actualizada",
    "descripcion": "Descripción actualizada"
}

# Eliminar pantalla
DELETE {{base_url}}/api/pantallas/1/
Authorization: Bearer {{access_token}}
```

### 5.2 Rol-Pantallas
```http
# Listar todas las asignaciones
GET {{base_url}}/api/rolpantallas/
Authorization: Bearer {{access_token}}

# Filtrar por rol
GET {{base_url}}/api/rolpantallas/?rolid=2
Authorization: Bearer {{access_token}}

# Filtrar por pantalla
GET {{base_url}}/api/rolpantallas/?pantallaid=1
Authorization: Bearer {{access_token}}

# Crear asignación
POST {{base_url}}/api/rolpantallas/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "rolid": 2,
    "pantallaid": 1,
    "acceso": true
}

# Actualizar asignación
PUT {{base_url}}/api/rolpantallas/1/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "acceso": false
}
```

---

## 6. Ejemplos de Uso

### 6.1 Flujo Completo: Asignar Permisos a Supervisor

1. **Login como Administrador:**
```http
POST {{base_url}}/login/
Content-Type: application/json

{
    "email": "admin@ejemplo.com",
    "password": "password123"
}
```

2. **Ver pantallas disponibles:**
```http
GET {{base_url}}/pantallas-list/
Authorization: Bearer {{access_token}}
```

3. **Asignar pantallas al rol Supervisor (ID=2):**
```http
POST {{base_url}}/asignar-multiples-pantallas-rol/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "rol_id": 2,
    "pantallas": [
        {"pantalla_id": 1, "acceso": true},  // Dashboard
        {"pantalla_id": 3, "acceso": true},  // Clientes
        {"pantalla_id": 4, "acceso": true},  // Crear Cliente
        {"pantalla_id": 10, "acceso": true}  // Reportes
    ]
}
```

4. **Verificar asignación:**
```http
GET {{base_url}}/rol-pantallas/2/
Authorization: Bearer {{access_token}}
```

### 6.2 Flujo: Usuario Supervisor Accede a Sistema

1. **Login como Supervisor:**
```http
POST {{base_url}}/login/
Content-Type: application/json

{
    "email": "supervisor@ejemplo.com",
    "password": "password123"
}
```

2. **Obtener pantallas accesibles:**
```http
GET {{base_url}}/pantallas-usuario/
Authorization: Bearer {{access_token}}
```

3. **Verificar acceso específico:**
```http
POST {{base_url}}/verificar-acceso-pantalla/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "codigo": "clientes_list"
}
```

---

## 7. Códigos de Error Comunes

| Código | Descripción | Solución |
|--------|-------------|----------|
| 401 | No autenticado | Iniciar sesión y obtener token válido |
| 403 | Acceso denegado | Verificar que el usuario sea administrador |
| 404 | Rol no encontrado | Verificar que el rol_id exista |
| 400 | Datos requeridos faltantes | Verificar que todos los campos requeridos estén presentes |

---

## 8. Estructura de Roles (Según Base de Datos)

| RolID | Nombre | NivelAcceso | Descripción |
|-------|--------|-------------|-------------|
| 1 | Administrador | 4 | Acceso completo al sistema |
| 2 | Supervisor | 3 | Supervisa departamentos específicos |
| 3 | Usuario | 2 | Usuario estándar |
| 4 | Consulta | 2 | Solo permisos de lectura |

---

## 9. Notas Importantes

1. **Solo los administradores (RolID = 1)** pueden asignar pantallas a roles
2. **Los tokens JWT** deben incluirse en el header `Authorization: Bearer {{access_token}}`
3. **El sistema valida automáticamente** el acceso a cada pantalla basado en el rol del usuario
4. **Las pantallas inactivas** no se consideran en las verificaciones de acceso
5. **Para desarrollo local**, usar `http://localhost:8000` como `base_url`

---

## 10. Pruebas Rápidas

### Test de Acceso por Rol:
```bash
# Como Admin (debe tener acceso a todo)
curl -X POST http://localhost:8000/verificar-acceso-pantalla/ \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"codigos": ["dashboard", "clientes_list", "usuarios_list"]}'

# Como Usuario (debe tener acceso limitado)
curl -X POST http://localhost:8000/verificar-acceso-pantalla/ \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"codigos": ["dashboard", "clientes_list", "usuarios_list"]}'
```

Esta colección proporciona todas las herramientas necesarias para probar y gestionar el sistema de control de acceso basado en roles.
