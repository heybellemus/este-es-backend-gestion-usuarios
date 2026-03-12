-- Script para crear la tabla PasswordResetTokens en SQL Server
-- Ejecutar este script directamente en SQL Server Management Studio

USE [GestionUsuariosDB];
GO

-- Verificar si la tabla ya existe y eliminarla
IF OBJECT_ID('dbo.PasswordResetTokens', 'U') IS NOT NULL
    DROP TABLE dbo.PasswordResetTokens;
GO

-- Crear la tabla PasswordResetTokens
CREATE TABLE dbo.PasswordResetTokens (
    tokenid INT IDENTITY(1,1) PRIMARY KEY,
    token NVARCHAR(255) NOT NULL UNIQUE,
    email NVARCHAR(255) NOT NULL,
    fecha_creacion DATETIMEOFFSET NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    fecha_expiracion DATETIMEOFFSET NOT NULL,
    utilizado BIT NOT NULL DEFAULT 0,
    fecha_utilizacion DATETIMEOFFSET NULL,
    ip_address NVARCHAR(39) NULL,
    user_agent NVARCHAR(MAX) NULL,
    usuarioid INT NOT NULL
);
GO

-- Crear índice para el token
CREATE INDEX idx_password_reset_token ON dbo.PasswordResetTokens(token);
GO

-- Crear índice para el usuario
CREATE INDEX idx_password_reset_usuario ON dbo.PasswordResetTokens(usuarioid);
GO

-- Crear índice para el email
CREATE INDEX idx_password_reset_email ON dbo.PasswordResetTokens(email);
GO

-- Crear índice compuesto para búsquedas eficientes
CREATE INDEX idx_password_reset_busqueda ON dbo.PasswordResetTokens(utilizado, fecha_expiracion);
GO

PRINT 'Tabla PasswordResetTokens creada exitosamente';
GO
