-- Script SQL para crear tablas de Pantallas y RolPantallas
-- Ejecutar este script en tu base de datos SQL Server

-- Crear tabla Pantallas
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Pantallas' AND xtype='U')
BEGIN
    CREATE TABLE Pantallas (
        PantallaID INT IDENTITY(1,1) PRIMARY KEY,
        Nombre VARCHAR(100) NOT NULL,
        Codigo VARCHAR(50) NOT NULL UNIQUE,
        Descripcion VARCHAR(500) NULL,
        Ruta VARCHAR(200) NULL,
        Modulo VARCHAR(50) NULL,
        Activo BIT DEFAULT 1,
        FechaCreacion DATETIME DEFAULT GETDATE()
    )
END

-- Crear tabla RolPantallas
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='RolPantallas' AND xtype='U')
BEGIN
    CREATE TABLE RolPantallas (
        RolPantallaID INT IDENTITY(1,1) PRIMARY KEY,
        RolID INT NOT NULL,
        PantallaID INT NOT NULL,
        Acceso BIT DEFAULT 1,
        FechaAsignacion DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (RolID) REFERENCES Roles(RolID),
        FOREIGN KEY (PantallaID) REFERENCES Pantallas(PantallaID)
    )
END

-- Insertar pantallas de ejemplo
IF NOT EXISTS (SELECT * FROM Pantallas WHERE Codigo = 'dashboard')
BEGIN
    INSERT INTO Pantallas (Nombre, Codigo, Descripcion, Ruta, Modulo) VALUES
    ('Dashboard', 'dashboard', 'Pantalla principal del sistema', '/dashboard', 'Principal'),
    ('Clientes', 'clientes_list', 'Listado de clientes', '/clientes', 'Gestión'),
    ('Crear Cliente', 'clientes_create', 'Formulario para crear nuevos clientes', '/clientes/nuevo', 'Gestión'),
    ('Editar Cliente', 'clientes_edit', 'Formulario para editar clientes', '/clientes/editar', 'Gestión'),
    ('Usuarios', 'usuarios_list', 'Listado de usuarios del sistema', '/usuarios', 'Administración'),
    ('Crear Usuario', 'usuarios_create', 'Formulario para crear nuevos usuarios', '/usuarios/nuevo', 'Administración'),
    ('Editar Usuario', 'usuarios_edit', 'Formulario para editar usuarios', '/usuarios/editar', 'Administración'),
    ('Roles', 'roles_list', 'Gestión de roles y permisos', '/roles', 'Administración'),
    ('Permisos', 'permisos_list', 'Configuración de permisos del sistema', '/permisos', 'Administración'),
    ('Departamentos', 'departamentos_list', 'Gestión de departamentos', '/departamentos', 'Organización'),
    ('Reportes', 'reportes', 'Generación de reportes', '/reportes', 'Reportes'),
    ('Configuración', 'configuracion', 'Configuración general del sistema', '/configuracion', 'Sistema')
END

-- Asignar pantallas a roles (ejemplo para rol Administrador - ID=1)
-- Nota: Ajusta los IDs según tu base de datos existente
IF EXISTS (SELECT * FROM Roles WHERE RolID = 1)
BEGIN
    -- Eliminar asignaciones existentes para evitar duplicados
    DELETE FROM RolPantallas WHERE RolID = 1
    
    -- Asignar todas las pantallas al rol Administrador
    INSERT INTO RolPantallas (RolID, PantallaID, Acceso)
    SELECT 1, PantallaID, 1 FROM Pantallas WHERE Activo = 1
END

-- Asignar pantallas básicas a rol Usuario estándar (ID=2)
IF EXISTS (SELECT * FROM Roles WHERE RolID = 2)
BEGIN
    -- Eliminar asignaciones existentes
    DELETE FROM RolPantallas WHERE RolID = 2
    
    -- Asignar solo pantallas básicas
    INSERT INTO RolPantallas (RolID, PantallaID, Acceso)
    SELECT 2, PantallaID, 1 FROM Pantallas 
    WHERE Codigo IN ('dashboard', 'clientes_list', 'clientes_create', 'clientes_edit', 'departamentos_list')
END

PRINT 'Tablas de Pantallas y RolPantallas creadas y pobladas correctamente'
