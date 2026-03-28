/* Fix para error:
   "No se puede insertar el valor NULL en la columna 'usuario_id' ... dbo.menu_movimientos"

   Contexto:
   - Al insertar un lote (menu_lotes) existe un trigger en SQL Server que inserta un movimiento en menu_movimientos.
   - El trigger está enviando usuario_id = NULL y la columna en BD no admite NULL.

   Elige UNA de las opciones:
   A) Permitir NULL (solo si negocio lo permite).
   B) Asignar un usuario por defecto (ej: 1) cuando no se provea (mantiene NOT NULL).
   C) Corregir el trigger para tomar usuario_id desde SESSION_CONTEXT (recomendado si quieres auditoría real).

   Ejecuta primero las consultas de verificación.
*/

-- ============================================
-- Verificación
-- ============================================
SELECT
  c.COLUMN_NAME,
  c.IS_NULLABLE,
  c.DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS c
WHERE c.TABLE_SCHEMA = 'dbo'
  AND c.TABLE_NAME = 'menu_movimientos'
  AND c.COLUMN_NAME = 'usuario_id';

-- (Opcional) Ver constraints/defaults asociados a usuario_id
SELECT
  dc.name AS default_constraint_name,
  dc.definition AS default_definition
FROM sys.default_constraints dc
JOIN sys.columns col
  ON col.default_object_id = dc.object_id
JOIN sys.tables t
  ON t.object_id = col.object_id
WHERE t.name = 'menu_movimientos'
  AND col.name = 'usuario_id';

-- ============================================
-- Opción A (recomendado): permitir NULL
-- ============================================
-- Nota: Ajusta el tipo si tu columna no es INT.
-- ALTER TABLE dbo.menu_movimientos ALTER COLUMN usuario_id INT NULL;

-- ============================================
-- Opción B: default a un usuario (ej: 1)
-- ============================================
-- 1) (Opcional) si ya existe un DEFAULT, elimínalo manualmente antes.
-- 2) Asegúrate de que el usuario exista y sea válido para tus reglas.
-- ALTER TABLE dbo.menu_movimientos
--   ADD CONSTRAINT DF_menu_movimientos_usuario_id DEFAULT (1) FOR usuario_id;

-- ============================================
-- Opción C (recomendado): corregir el trigger
-- ============================================
-- Requisitos:
-- - Debe existir un UsuarioID "sistema" (por ejemplo 1) en dbo.Usuarios.
-- - Tu app debe setear SESSION_CONTEXT('usuario_id') antes de insertar (opcional; si no, usará el fallback).
--
-- ALTER TRIGGER dbo.trg_AfterInsertLote
-- ON dbo.menu_lotes
-- AFTER INSERT
-- AS
-- BEGIN
--     SET NOCOUNT ON;
--
--     -- 1) Actualizar stock
--     UPDATE p
--     SET p.stock_actual_producto = p.stock_actual_producto + i.cantidad_recibida_lote
--     FROM dbo.menu_productos p
--     INNER JOIN inserted i ON p.id_producto = i.id_producto;
--
--     -- 2) Determinar usuario
--     DECLARE @usuario_id INT = TRY_CONVERT(INT, SESSION_CONTEXT(N'usuario_id'));
--     IF @usuario_id IS NULL OR NOT EXISTS (SELECT 1 FROM dbo.Usuarios u WHERE u.UsuarioID = @usuario_id)
--         SET @usuario_id = 1;
--
--     -- 3) Insertar movimiento de entrada
--     INSERT INTO dbo.menu_movimientos (
--         id_producto, id_lote, cantidad_movimiento, fecha_movimiento,
--         motivo_movimiento, id_tipo_movimiento, usuario_id
--     )
--     SELECT
--         id_producto, id_lote, cantidad_recibida_lote, GETDATE(),
--         'Ingreso de nuevo lote: ' + numero_lote, 1, @usuario_id
--     FROM inserted;
-- END;
