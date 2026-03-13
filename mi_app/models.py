# mi_app/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class ComputedDecimalField(models.DecimalField):
    generated = True


class ComputedCharField(models.CharField):
    generated = True


class Clientes(models.Model):
    clienteid = models.AutoField(db_column='ClienteID', primary_key=True)
    tipodocumento = models.CharField(db_column='TipoDocumento', max_length=10, blank=True, null=True)
    numerodocumento = models.CharField(db_column='NumeroDocumento', max_length=20)
    razonsocial = models.CharField(db_column='RazonSocial', max_length=200)
    nombrecomercial = models.CharField(db_column='NombreComercial', max_length=200, blank=True, null=True)
    telefono = models.CharField(db_column='Telefono', max_length=20, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)
    direccion = models.CharField(db_column='Direccion', max_length=500, blank=True, null=True)
    ciudad = models.CharField(db_column='Ciudad', max_length=100, blank=True, null=True)
    pais = models.CharField(db_column='Pais', max_length=100, blank=True, null=True)
    activo = models.BooleanField(db_column='Activo', blank=True, null=True)
    creadopor = models.IntegerField(db_column='CreadoPor', blank=True, null=True)
    fechacreacion = models.DateTimeField(db_column='FechaCreacion', blank=True, null=True)
    modificadopor = models.IntegerField(db_column='ModificadoPor', blank=True, null=True)
    fechamodificacion = models.DateTimeField(db_column='FechaModificacion', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    
    def __str__(self):
        return f"{self.razonsocial} ({self.numerodocumento})"


class Departamentos(models.Model):
    departamentoid = models.AutoField(db_column='DepartamentoID', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100)
    descripcion = models.CharField(db_column='Descripcion', max_length=500, blank=True, null=True)
    activo = models.BooleanField(db_column='Activo', blank=True, null=True)
    fechacreacion = models.DateTimeField(db_column='FechaCreacion', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Departamentos'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return f"{self.nombre}"


class Roles(models.Model):
    rolid = models.AutoField(db_column='RolID', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100)
    descripcion = models.CharField(db_column='Descripcion', max_length=500, blank=True, null=True)
    nivelacceso = models.IntegerField(db_column='NivelAcceso', blank=True, null=True)
    activo = models.BooleanField(db_column='Activo', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return f"{self.nombre}"


# ⚠️ MODELO USUARIOS CORREGIDO ⚠️
class Usuarios(models.Model):
    usuarioid = models.AutoField(db_column='UsuarioID', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100)
    apellido = models.CharField(db_column='Apellido', max_length=100)
    email = models.CharField(db_column='Email', max_length=255)
    nombreusuario = models.CharField(db_column='NombreUsuario', max_length=50)
    passwordhash = models.CharField(db_column='PasswordHash', max_length=255)
    
    # VERIFICA ESTO: ¿Es RollID o RolID en tu BD?
    # Si en tu BD es "RollID" (con doble L), cambia db_column='RolID' por db_column='RollID'
    # Si es "RolID" (con una L), déjalo como está
    
    departamentoid = models.ForeignKey('Departamentos', db_column='DepartamentoID', on_delete=models.DO_NOTHING, blank=True, null=True)
    rolid = models.ForeignKey('Roles', db_column='RolID', on_delete=models.DO_NOTHING, blank=True, null=True)  # ← VERIFICA AQUÍ
    
    activo = models.BooleanField(db_column='Activo', blank=True, null=True)
    fechacreacion = models.DateTimeField(db_column='FechaCreacion', blank=True, null=True)
    ultimoacceso = models.DateTimeField(db_column='UltimoAcceso', blank=True, null=True)
    intentosfallidos = models.IntegerField(db_column='IntentosFallidos', blank=True, null=True)
    bloqueado = models.BooleanField(db_column='Bloqueado', blank=True, null=True)
    fechabloqueo = models.DateTimeField(db_column='FechaBloqueo', blank=True, null=True)

    # Propiedad para compatibilidad con JWT y Django auth
    @property
    def id(self):
        return self.usuarioid

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.activo

    class Meta:
        managed = False
        db_table = 'Usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"


class PasswordResetToken(models.Model):
    tokenid = models.AutoField(primary_key=True)
    usuarioid = models.ForeignKey('Usuarios', on_delete=models.CASCADE, db_column='usuarioid')
    token = models.CharField(max_length=255, unique=True, db_column='token')
    email = models.CharField(max_length=255, db_column='email')
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')
    fecha_expiracion = models.DateTimeField(db_column='fecha_expiracion')
    utilizado = models.BooleanField(default=False, db_column='utilizado')
    fecha_utilizacion = models.DateTimeField(blank=True, null=True, db_column='fecha_utilizacion')
    ip_address = models.GenericIPAddressField(blank=True, null=True, db_column='ip_address')
    user_agent = models.TextField(blank=True, null=True, db_column='user_agent')

    class Meta:
        db_table = 'PasswordResetTokens'
        verbose_name = 'Token de Recuperación'
        verbose_name_plural = 'Tokens de Recuperación'
        managed = False

    def __str__(self):
        return f"Token para {self.email} - {'Utilizado' if self.utilizado else 'Pendiente'}"

    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.fecha_expiracion

    @property
    def is_valid(self):
        return not self.utilizado and not self.is_expired


class Permisos(models.Model):
    permisoid = models.AutoField(db_column='PermisoID', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100)
    codigo = models.CharField(db_column='Codigo', max_length=50)
    descripcion = models.CharField(db_column='Descripcion', max_length=500, blank=True, null=True)
    modulo = models.CharField(db_column='Modulo', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Permisos'
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class RolPermisos(models.Model):
    rolpermisoid = models.AutoField(db_column='RolPermisoID', primary_key=True)
    rolid = models.ForeignKey('Roles', db_column='RolID', on_delete=models.DO_NOTHING)
    permisoid = models.ForeignKey('Permisos', db_column='PermisoID', on_delete=models.DO_NOTHING)
    otorgado = models.BooleanField(db_column='Otorgado', blank=True, null=True)
    fechaasignacion = models.DateTimeField(db_column='FechaAsignacion', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RolPermisos'
        verbose_name = 'Rol Permiso'
        verbose_name_plural = 'Rol Permisos'

    def __str__(self):
        return f"Rol: {self.rolid_id} - Permiso: {self.permisoid_id}"


class Pantallas(models.Model):
    pantallaid = models.AutoField(db_column='PantallaID', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100)
    codigo = models.CharField(db_column='Codigo', max_length=50, unique=True)
    descripcion = models.CharField(db_column='Descripcion', max_length=500, blank=True, null=True)
    ruta = models.CharField(db_column='Ruta', max_length=200, blank=True, null=True)
    modulo = models.CharField(db_column='Modulo', max_length=50, blank=True, null=True)
    activo = models.BooleanField(db_column='Activo', default=True)
    fechacreacion = models.DateTimeField(db_column='FechaCreacion', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'Pantallas'
        verbose_name = 'Pantalla'
        verbose_name_plural = 'Pantallas'

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class RolPantallas(models.Model):
    rolpantallaid = models.AutoField(db_column='RolPantallaID', primary_key=True)
    rolid = models.ForeignKey('Roles', db_column='RolID', on_delete=models.DO_NOTHING)
    pantallaid = models.ForeignKey('Pantallas', db_column='PantallaID', on_delete=models.DO_NOTHING)
    acceso = models.BooleanField(db_column='Acceso', default=True)
    fechaasignacion = models.DateTimeField(db_column='FechaAsignacion', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'RolPantallas'
        verbose_name = 'Rol Pantalla'
        verbose_name_plural = 'Rol Pantallas'

    def __str__(self):
        return f"Rol: {self.rolid_id} - Pantalla: {self.pantallaid_id}"


class SesionesQR(models.Model):
    sesionqrid = models.AutoField(db_column='SesionQRID', primary_key=True)
    codigosesion = models.CharField(db_column='CodigoSesion', max_length=100, unique=True)
    usuarioid = models.ForeignKey('Usuarios', db_column='UsuarioID', on_delete=models.CASCADE, blank=True, null=True)
    dispositivosinfo = models.CharField(db_column='DispositivoInfo', max_length=500, blank=True, null=True)
    estado = models.CharField(db_column='Estado', max_length=20, default='pendiente')
    tokenacceso = models.CharField(db_column='TokenAcceso', max_length=500, blank=True, null=True)
    tokenrefresh = models.CharField(db_column='TokenRefresh', max_length=500, blank=True, null=True)
    fechacreacion = models.DateTimeField(db_column='FechaCreacion', auto_now_add=True)
    fechaexpiracion = models.DateTimeField(db_column='FechaExpiracion')
    fechaaprobacion = models.DateTimeField(db_column='FechaAprobacion', blank=True, null=True)
    fechauso = models.DateTimeField(db_column='FechaUso', blank=True, null=True)
    iporigen = models.CharField(db_column='IPOrigen', max_length=50, blank=True, null=True)
    useragent = models.CharField(db_column='UserAgent', max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SesionesQR'
        verbose_name = 'Sesión QR'
        verbose_name_plural = 'Sesiones QR'

    def __str__(self):
        return f"Sesión QR: {self.codigosesion} - {self.estado}"


class MenuCategorias(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50, unique=True)
    descripcion_categoria = models.CharField(max_length=255, blank=True, null=True)
    activo_categoria = models.BooleanField(blank=True, null=True)
    fecha_creacion_categoria = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "menu_categorias"


class MenuUnidadesMedida(models.Model):
    id_unidad_medida = models.AutoField(primary_key=True)
    codigo_unidad = models.CharField(max_length=10, unique=True)
    nombre_unidad = models.CharField(max_length=50)
    simbolo_unidad = models.CharField(max_length=5, blank=True, null=True)
    descripcion_unidad = models.CharField(max_length=255, blank=True, null=True)
    activo_unidad = models.BooleanField(blank=True, null=True)
    fecha_creacion_unidad = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "menu_unidades_medida"


class MenuProductos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    id_categoria = models.ForeignKey(
        MenuCategorias,
        db_column="id_categoria",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    id_unidad_medida = models.ForeignKey(
        MenuUnidadesMedida,
        db_column="id_unidad_medida",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    nombre_producto = models.CharField(max_length=100)
    sku_producto = models.CharField(max_length=20, unique=True)
    descripcion_producto = models.CharField(max_length=255, blank=True, null=True)
    stock_actual_producto = models.IntegerField(blank=True, null=True)
    stock_minimo_producto = models.IntegerField(blank=True, null=True)
    stock_maximo_producto = models.IntegerField(blank=True, null=True)
    ubicacion_producto = models.CharField(max_length=50, blank=True, null=True)
    imagen_url_producto = models.CharField(max_length=255, blank=True, null=True)
    activo_producto = models.BooleanField(blank=True, null=True)
    fecha_creacion_producto = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion_producto = models.DateTimeField(auto_now_add=True)
    class Meta:
        managed = False
        db_table = "menu_productos"


class MenuLotes(models.Model):
    id_lote = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(
        MenuProductos,
        db_column="id_producto",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    numero_lote = models.CharField(max_length=50, blank=True, null=True)
    cantidad_recibida_lote = models.IntegerField()
    cantidad_disponible_lote = models.IntegerField()
    precio_compra_lote = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta_lote = models.DecimalField(max_digits=10, decimal_places=2)
    porcentaje_ganancia_lote = ComputedDecimalField(
        max_digits=18, decimal_places=6, blank=True, null=True, editable=False
    )
    ganancia_formateada = ComputedCharField(max_length=50, blank=True, null=True, editable=False)
    fecha_vencimiento_lote = models.DateField(blank=True, null=True)
    fecha_ingreso_lote = models.DateTimeField(auto_now_add=True)
    id_proveedor = models.IntegerField(
        db_column="id_proveedor",
        blank=True,
        null=True,
    )
    activo_lote = models.BooleanField(blank=True, null=True)
    observaciones_lote = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "menu_lotes"


class CatTiposMovimiento(models.Model):
    id_tipo_movimiento = models.AutoField(primary_key=True, db_column='id_tipo_movimiento')
    codigo_tipo = models.CharField(max_length=20, db_column='codigo_tipo')
    nombre_tipo = models.CharField(max_length=50, db_column='nombre_tipo')
    descripcion = models.CharField(max_length=255, blank=True, null=True, db_column='descripcion')
    signo = models.CharField(max_length=3, db_column='signo')
    requiere_precio = models.BooleanField(blank=True, null=True, db_column='requiere_precio')
    activo = models.BooleanField(blank=True, null=True, db_column='activo')
    orden = models.IntegerField(blank=True, null=True, db_column='orden')

    class Meta:
        managed = False
        db_table = 'cat_tipos_movimiento'
        verbose_name = 'Tipo de Movimiento'
        verbose_name_plural = 'Tipos de Movimiento'

    def __str__(self):
        return f"{self.nombre_tipo} ({self.codigo_tipo})"


class MenuMovimientos(models.Model):
    id_movimiento = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(
        MenuProductos,
        db_column="id_producto",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    id_lote = models.ForeignKey(
        MenuLotes,
        db_column="id_lote",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    tipo_movimiento = models.CharField(max_length=20, blank=True, null=True, db_column='codigo_tipo_movimiento')
    cantidad_movimiento = models.IntegerField()
    precio_unitario_movimiento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    motivo_movimiento = models.CharField(max_length=255, blank=True, null=True)
    documento_referencia_movimiento = models.CharField(max_length=50, blank=True, null=True)
    observaciones_movimiento = models.TextField(blank=True, null=True)
    id_tipo_movimiento = models.ForeignKey(
        CatTiposMovimiento,
        db_column="id_tipo_movimiento",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    usuario_id = models.ForeignKey(
        Usuarios,
        db_column="usuario_id",
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        managed = False
        db_table = "menu_movimientos"
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'

    def __str__(self):
        return f"Movimiento {self.id_movimiento} - {self.tipo_movimiento}"


class MenuProveedores(models.Model):
    id_proveedor = models.AutoField(primary_key=True, db_column='id_proveedor')
    nombre_comercial = models.CharField(max_length=200, db_column='nombre_comercial')
    rtn = models.CharField(max_length=20, db_column='rtn')
    direccion = models.TextField(blank=True, null=True, db_column='direccion')
    persona_contacto = models.CharField(max_length=150, blank=True, null=True, db_column='persona_contacto')
    telefono = models.CharField(max_length=50, blank=True, null=True, db_column='telefono')
    correo_electronico = models.CharField(max_length=100, blank=True, null=True, db_column='correo_electronico')
    datos_bancarios = models.TextField(blank=True, null=True, db_column='datos_bancarios')
    observaciones = models.TextField(blank=True, null=True, db_column='observaciones')
    activo = models.BooleanField(db_column='activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)


    class Meta:
        managed = False
        db_table = 'menu_proveedores'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return f"{self.nombre_comercial} ({self.rtn})"


class MenuHistorialPrecios(models.Model):
    id_historial_precio = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(
        MenuProductos,
        db_column="id_producto",
        on_delete=models.DO_NOTHING,
    )
    id_lote = models.ForeignKey(
        MenuLotes,
        db_column="id_lote",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    precio_compra_anterior = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precio_compra_nuevo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precio_venta_anterior = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precio_venta_nuevo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_cambio_precio = models.DateTimeField(auto_now_add=True)
    usuario_cambio = models.CharField(max_length=100, blank=True, null=True)
    motivo_cambio = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "menu_historial_precios"
